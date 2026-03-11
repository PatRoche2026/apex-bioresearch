"""Executive agent nodes — assessment and rebuttal for CSO, CTO, CMO, CBO."""

from __future__ import annotations

import asyncio
import re
from datetime import datetime, timezone
from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from agents import (
    ANTHROPIC_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT_SECONDS,
    llm_semaphore,
)
from agents.prompts import (
    ASSESSMENT_USER_TEMPLATE,
    CEO_FEEDBACK_SECTION,
    EXECUTIVE_PROMPTS,
    EXECUTIVE_ROLES,
    REBUTTAL_SYSTEM_TEMPLATE,
    REBUTTAL_USER_TEMPLATE,
    ROLE_TOOL_DESCRIPTIONS,
    SHARPEN_INSTRUCTION,
    TOOL_FOLLOWUP_TEMPLATE,
)
from agents.state import APEXState
from agents.tools import parse_tool_requests, execute_tool_requests

# RAG is optional — gracefully degrade if chromadb/sentence-transformers not installed
try:
    from rag.retriever import retrieve_context as _retrieve_context
except ImportError:
    _retrieve_context = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Shared LLM instance
# ---------------------------------------------------------------------------

_llm = ChatAnthropic(
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    api_key=ANTHROPIC_API_KEY,
    max_tokens=2048,
)

# ---------------------------------------------------------------------------
# Score parsing — regex extraction from structured LLM output
# ---------------------------------------------------------------------------

_SCORE_DIMENSIONS = [
    "SCIENTIFIC_VALIDITY",
    "TECHNICAL_FEASIBILITY",
    "CLINICAL_PATH",
    "COMMERCIAL_POTENTIAL",
]


def parse_scores(text: str) -> dict[str, int]:
    """Extract X/10 scores from executive output text."""
    scores: dict[str, int] = {}
    for dim in _SCORE_DIMENSIONS:
        match = re.search(rf"{dim}:\s*(\d+)\s*/\s*10", text)
        if match:
            scores[dim.lower()] = min(int(match.group(1)), 10)
    return scores


def parse_confidence(text: str) -> int:
    """Extract confidence percentage from executive output text."""
    match = re.search(r"CONFIDENCE:\s*(\d+)", text)
    return min(int(match.group(1)), 100) if match else 50


def parse_verdict(text: str) -> str:
    """Extract GO / CONDITIONAL GO / NO-GO from text."""
    # Check for the most specific first
    if re.search(r"\bCONDITIONAL\s+GO\b", text, re.IGNORECASE):
        return "CONDITIONAL GO"
    if re.search(r"\bNO[\s-]GO\b", text, re.IGNORECASE):
        return "NO-GO"
    if re.search(r"\bGO\b", text):
        return "GO"
    return "CONDITIONAL GO"  # default if parsing fails


# ---------------------------------------------------------------------------
# Safe LLM call with semaphore + timeout
# ---------------------------------------------------------------------------


async def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Call LLM with rate limit semaphore and timeout protection."""
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    async with llm_semaphore:
        try:
            response = await asyncio.wait_for(
                _llm.ainvoke(messages),
                timeout=LLM_TIMEOUT_SECONDS,
            )
            return response.content
        except asyncio.TimeoutError:
            return "[Agent timed out after 60s — proceeding with available assessments]"
        except Exception as e:
            return f"[Agent error: {str(e)[:200]}]"


# ---------------------------------------------------------------------------
# Assessment node factory — creates a node function for each executive
# ---------------------------------------------------------------------------


def _make_assess_node(role: str):
    """Create an assessment node function for the given executive role.

    Args:
        role: One of 'cso', 'cto', 'cmo', 'cbo'
    """
    field_name = f"{role}_assessment"
    system_prompt = EXECUTIVE_PROMPTS[role]
    role_label = EXECUTIVE_ROLES[role]

    async def assess_node(state: APEXState) -> dict[str, Any]:
        ts = datetime.now(timezone.utc).isoformat()

        # Retrieve RAG context (graceful fallback if unavailable)
        rag_context = ""
        if _retrieve_context is not None:
            try:
                rag_context = _retrieve_context(role, state["query"], k=5)
            except Exception:
                pass  # RAG failure should not block assessment

        # CEO feedback section (Feature 4)
        ceo_feedback_section = ""
        ceo_feedback = state.get("ceo_feedback", "")
        if ceo_feedback:
            ceo_feedback_section = CEO_FEEDBACK_SECTION.format(ceo_feedback=ceo_feedback)

        # Role-specific tool descriptions (Feature 5)
        role_tools_section = ROLE_TOOL_DESCRIPTIONS.get(role, "")

        # Build user prompt with optional RAG context injected
        user_prompt = ASSESSMENT_USER_TEMPLATE.format(
            query=state["query"],
            scout_data=state["scout_data"],
            ceo_feedback_section=ceo_feedback_section,
            role_tools_section=role_tools_section,
        )
        if rag_context:
            user_prompt = f"{rag_context}\n\n---\n\n{user_prompt}"

        assessment = await _call_llm(system_prompt, user_prompt)

        # Two-pass: check for TOOL_REQUESTS and execute if found (role-filtered)
        tool_requests = parse_tool_requests(assessment)
        tools_used = []
        if tool_requests:
            try:
                tool_results = await execute_tool_requests(tool_requests, role=role)
                if tool_results:
                    tools_used = [t[0] for t in tool_requests]
                    followup_prompt = TOOL_FOLLOWUP_TEMPLATE.format(
                        query=state["query"],
                        tool_results=tool_results,
                    )
                    assessment = await _call_llm(system_prompt, followup_prompt)
            except Exception:
                pass  # Tool failure should not block assessment

        scores = parse_scores(assessment)

        log_entry = {
            "node": f"{role}_assess",
            "role": role_label,
            "status": "complete",
            "scores": scores,
            "verdict": parse_verdict(assessment),
            "confidence": parse_confidence(assessment),
            "timestamp": ts,
        }
        if tools_used:
            log_entry["tools_used"] = tools_used

        return {
            field_name: assessment,
            "executive_scores": {role: scores},
            "activity_log": [log_entry],
        }

    assess_node.__name__ = f"{role}_assess_node"
    assess_node.__qualname__ = f"{role}_assess_node"
    return assess_node


# ---------------------------------------------------------------------------
# Create all 4 assessment nodes
# ---------------------------------------------------------------------------

cso_assess_node = _make_assess_node("cso")
cto_assess_node = _make_assess_node("cto")
cmo_assess_node = _make_assess_node("cmo")
cbo_assess_node = _make_assess_node("cbo")

# ---------------------------------------------------------------------------
# Rebuttal node factory — creates a rebuttal node for each executive
# ---------------------------------------------------------------------------


def _make_rebuttal_node(role: str):
    """Create a rebuttal node function for the given executive role.

    Args:
        role: One of 'cso', 'cto', 'cmo', 'cbo'
    """
    field_name = f"{role}_rebuttal"
    role_label = EXECUTIVE_ROLES[role]

    async def rebuttal_node(state: APEXState) -> dict[str, Any]:
        ts = datetime.now(timezone.utc).isoformat()
        round_num = state.get("debate_round", 0) + 1

        # Build system prompt with optional sharpen instruction for round 2+
        sharpen = ""
        if round_num >= 2:
            sharpen = SHARPEN_INSTRUCTION.format(round_num=round_num)

        system_prompt = REBUTTAL_SYSTEM_TEMPLATE.format(
            role=role_label,
            round_num=round_num,
            sharpen_instruction=sharpen,
        )

        # CEO feedback section (Feature 4)
        ceo_feedback_section = ""
        ceo_feedback = state.get("ceo_feedback", "")
        if ceo_feedback:
            ceo_feedback_section = CEO_FEEDBACK_SECTION.format(ceo_feedback=ceo_feedback)

        user_prompt = REBUTTAL_USER_TEMPLATE.format(
            query=state["query"],
            ceo_feedback_section=ceo_feedback_section,
            cso_assessment=state["cso_assessment"],
            cto_assessment=state["cto_assessment"],
            cmo_assessment=state["cmo_assessment"],
            cbo_assessment=state["cbo_assessment"],
        )

        rebuttal = await _call_llm(system_prompt, user_prompt)
        scores = parse_scores(rebuttal)

        return {
            field_name: rebuttal,
            "executive_scores": {role: scores},
            "activity_log": [
                {
                    "node": f"{role}_rebuttal",
                    "role": role_label,
                    "status": "complete",
                    "round": round_num,
                    "scores": scores,
                    "verdict": parse_verdict(rebuttal),
                    "confidence": parse_confidence(rebuttal),
                    "timestamp": ts,
                }
            ],
        }

    rebuttal_node.__name__ = f"{role}_rebuttal_node"
    rebuttal_node.__qualname__ = f"{role}_rebuttal_node"
    return rebuttal_node


# ---------------------------------------------------------------------------
# Create all 4 rebuttal nodes
# ---------------------------------------------------------------------------

cso_rebuttal_node = _make_rebuttal_node("cso")
cto_rebuttal_node = _make_rebuttal_node("cto")
cmo_rebuttal_node = _make_rebuttal_node("cmo")
cbo_rebuttal_node = _make_rebuttal_node("cbo")
