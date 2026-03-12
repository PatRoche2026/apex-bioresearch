"""APEXState — shared state schema for the multi-agent debate pipeline."""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


def _merge_dicts(left: dict, right: dict) -> dict:
    """Reducer that merges dicts (right overwrites left on key conflict).

    Used for executive_scores so parallel nodes can each write their own
    role's scores without overwriting other roles' scores.
    """
    merged = dict(left)
    merged.update(right)
    return merged


class APEXState(TypedDict):
    """Full state flowing through the APEX LangGraph pipeline."""

    # --- Input ---
    query: str

    # --- Scout stage ---
    scout_data: str                                          # Prose summary of PubMed findings
    scout_sources: list[dict]                                # [{pmid, title, journal, year, abstract_snippet}]

    # --- Assessment stage (parallel) ---
    cso_assessment: str
    cto_assessment: str
    cmo_assessment: str
    cbo_assessment: str

    # --- Debate / Rebuttal stage (parallel) ---
    cso_rebuttal: str
    cto_rebuttal: str
    cmo_rebuttal: str
    cbo_rebuttal: str

    # --- Portfolio Director ---
    portfolio_verdict: str
    confidence_score: int                                    # 0-100, parsed from director output

    # MUST use Annotated + _merge_dicts so parallel nodes merge scores instead of overwriting
    executive_scores: Annotated[dict, _merge_dicts]          # {cso: {scientific_validity: X, ...}, ...}

    # --- CEO Feedback (Human-in-the-Loop) ---
    ceo_feedback: str                                        # Latest CEO feedback text
    ceo_feedback_history: Annotated[list[dict], operator.add]  # All CEO feedback entries
    evaluation_round: int                                    # How many full evaluations (0=first, 1=re-eval after feedback)

    # --- Control ---
    debate_round: int                                        # Current round (for conditional loop)

    # --- Audit trail ---
    # MUST use Annotated + operator.add so parallel nodes merge logs instead of overwriting
    activity_log: Annotated[list[dict], operator.add]

    # --- Drug Development Plan (DDP) — populated after CEO accepts a GO verdict ---
    gene: str                                                # Extracted from query (e.g. "OSMR")
    indication: str                                          # Extracted from query (e.g. "ulcerative colitis")
    cso_ddp_section: str                                     # Elena's Target Validation Strategy (graph_ddp.py)
    cto_ddp_section: str                                     # Marcus's Modality & Manufacturing Strategy (graph_ddp.py)
    cmo_ddp_section: str                                     # Sarah's Clinical Development Strategy (graph_ddp.py)
    cbo_ddp_section: str                                     # James's Commercial & Strategic Assessment (graph_ddp.py)
    ddp_synthesis: str                                       # Amara's Executive Summary (graph_ddp.py)

    # --- Planning pipeline (compiled_planning_graph in graph.py) ---
    planning_triggered: bool                                 # True once CEO clicks "Accept" on a GO verdict
    cso_plan: str                                            # Elena's Target Validation Strategy
    cto_plan: str                                            # Marcus's Modality & Manufacturing Strategy
    cmo_plan: str                                            # Sarah's Clinical Development Strategy
    cbo_plan: str                                            # James's Commercial & Strategic Assessment
    director_synthesis: str                                  # Amara's Executive Summary & Integrated Timeline
    ddp_status: str                                          # "pending" | "in_progress" | "complete" | "skipped"
