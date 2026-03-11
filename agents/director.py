"""Portfolio Director node — synthesizes debate and issues final verdict."""

from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from agents import (
    ANTHROPIC_API_KEY,
    LLM_TEMPERATURE,
    LLM_TIMEOUT_SECONDS,
    ROLE_MODELS,
    estimate_cost,
    llm_semaphore,
)
from agents.executives import parse_confidence, parse_scores, parse_verdict
from agents.prompts import CEO_FEEDBACK_SECTION, DIRECTOR_SYSTEM_PROMPT, DIRECTOR_USER_TEMPLATE
from agents.state import APEXState

# ---------------------------------------------------------------------------
# LLM instance — Portfolio Director always uses Sonnet (strong model)
# ---------------------------------------------------------------------------

_DIRECTOR_MODEL = ROLE_MODELS["portfolio_director"]
_llm = ChatAnthropic(
    model=_DIRECTOR_MODEL,
    temperature=LLM_TEMPERATURE,
    api_key=ANTHROPIC_API_KEY,
    max_tokens=3000,
)

# ---------------------------------------------------------------------------
# Weighted composite score calculation
# ---------------------------------------------------------------------------

SCORE_WEIGHTS = {
    "scientific_validity": 0.30,
    "technical_feasibility": 0.25,
    "clinical_path": 0.25,
    "commercial_potential": 0.20,
}


def compute_weighted_score(executive_scores: dict) -> dict:
    """Compute weighted composite from all executives' final scores.

    Args:
        executive_scores: {role: {dimension: score, ...}, ...}

    Returns:
        {"per_dimension": {dim: avg}, "weighted_total": float,
         "per_executive": {role: {dim: score}}}
    """
    dims = list(SCORE_WEIGHTS.keys())

    # Average each dimension across all executives who provided it
    dim_averages: dict[str, float] = {}
    for dim in dims:
        values = [
            scores[dim]
            for scores in executive_scores.values()
            if isinstance(scores, dict) and dim in scores
        ]
        dim_averages[dim] = round(sum(values) / len(values), 1) if values else 5.0

    # Weighted total
    weighted_total = sum(dim_averages[dim] * SCORE_WEIGHTS[dim] for dim in dims)

    return {
        "per_dimension": dim_averages,
        "weighted_total": round(weighted_total, 2),
        "per_executive": executive_scores,
    }


# ---------------------------------------------------------------------------
# Portfolio Director node
# ---------------------------------------------------------------------------


async def portfolio_director_node(state: APEXState) -> dict[str, Any]:
    """Portfolio Director: synthesize all assessments + rebuttals, issue verdict."""
    ts = datetime.now(timezone.utc).isoformat()

    # CEO feedback section (Feature 4)
    ceo_feedback_section = ""
    ceo_feedback = state.get("ceo_feedback", "")
    if ceo_feedback:
        ceo_feedback_section = CEO_FEEDBACK_SECTION.format(ceo_feedback=ceo_feedback)

    user_prompt = DIRECTOR_USER_TEMPLATE.format(
        query=state["query"],
        ceo_feedback_section=ceo_feedback_section,
        cso_assessment=state["cso_assessment"],
        cto_assessment=state["cto_assessment"],
        cmo_assessment=state["cmo_assessment"],
        cbo_assessment=state["cbo_assessment"],
        cso_rebuttal=state["cso_rebuttal"],
        cto_rebuttal=state["cto_rebuttal"],
        cmo_rebuttal=state["cmo_rebuttal"],
        cbo_rebuttal=state["cbo_rebuttal"],
    )

    messages = [
        SystemMessage(content=DIRECTOR_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    call_cost = 0.0
    async with llm_semaphore:
        try:
            response = await asyncio.wait_for(
                _llm.ainvoke(messages),
                timeout=LLM_TIMEOUT_SECONDS,
            )
            verdict_text = response.content
            usage = getattr(response, "usage_metadata", None) or {}
            call_cost = estimate_cost(
                usage.get("input_tokens", 0),
                usage.get("output_tokens", 0),
                model=_DIRECTOR_MODEL,
            )
        except asyncio.TimeoutError:
            verdict_text = "[Portfolio Director timed out — defaulting to CONDITIONAL GO]"
        except Exception as e:
            verdict_text = f"[Portfolio Director error: {str(e)[:200]}]"

    # Parse director's own scores
    director_scores = parse_scores(verdict_text)
    confidence = parse_confidence(verdict_text)
    verdict = parse_verdict(verdict_text)

    # Compute weighted composite from ALL executives' latest scores
    # (executive_scores dict is merged across all parallel nodes)
    exec_scores = dict(state.get("executive_scores", {}))
    exec_scores["director"] = director_scores
    composite = compute_weighted_score(exec_scores)

    # Parse weighted total from director output if present (override computed)
    wt_match = re.search(r"WEIGHTED_TOTAL:\s*([\d.]+)\s*/\s*10", verdict_text)
    if wt_match:
        composite["weighted_total"] = float(wt_match.group(1))

    return {
        "portfolio_verdict": verdict_text,
        "confidence_score": confidence,
        "executive_scores": composite,
        "debate_round": state.get("debate_round", 0) + 1,
        "activity_log": [
            {
                "node": "portfolio_director",
                "status": "complete",
                "verdict": verdict,
                "confidence": confidence,
                "weighted_total": composite["weighted_total"],
                "round": state.get("debate_round", 0) + 1,
                "cost_usd": call_cost,
                "timestamp": ts,
            }
        ],
    }
