"""APEX LangGraph pipeline — full wiring with fan-out/fan-in + conditional loop."""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agents.director import portfolio_director_node
from agents.executives import (
    cbo_assess_node,
    cbo_rebuttal_node,
    cmo_assess_node,
    cmo_rebuttal_node,
    cso_assess_node,
    cso_rebuttal_node,
    cto_assess_node,
    cto_rebuttal_node,
)
from agents.scout import scout_node
from agents.state import APEXState


# ---------------------------------------------------------------------------
# Conditional edge: should we loop back for another debate round?
# ---------------------------------------------------------------------------


def _should_continue(state: APEXState) -> str:
    """Decide whether to end or loop back for another rebuttal round.

    Ends if:
      - confidence_score >= 60  (sufficient consensus)
      - debate_round >= 2       (max loops reached)
    Otherwise loops back to rebuttal fan-out for a sharper debate.
    """
    if state.get("confidence_score", 0) >= 60:
        return "end"
    if state.get("debate_round", 0) >= 2:
        return "end"
    return "continue"


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------


def build_graph() -> StateGraph:
    """Build and compile the full APEX debate pipeline.

    Topology:
        START -> scout
          -> [cso_assess, cto_assess, cmo_assess, cbo_assess]   (parallel)
          -> debate_router  (no-op sync point)
          -> [cso_rebuttal, cto_rebuttal, cmo_rebuttal, cbo_rebuttal]  (parallel)
          -> portfolio_director
          -> consensus_check
              ├── "end"      -> END
              └── "continue" -> debate_router (loop back)
    """
    g = StateGraph(APEXState)

    # --- Add all nodes ---
    g.add_node("scout", scout_node)

    # Assessment nodes (stage 2 — parallel)
    g.add_node("cso_assess", cso_assess_node)
    g.add_node("cto_assess", cto_assess_node)
    g.add_node("cmo_assess", cmo_assess_node)
    g.add_node("cbo_assess", cbo_assess_node)

    # Debate router — no-op pass-through for fan-in / fan-out sync
    g.add_node("debate_router", lambda state: {})

    # Rebuttal nodes (stage 3 — parallel)
    g.add_node("cso_rebuttal", cso_rebuttal_node)
    g.add_node("cto_rebuttal", cto_rebuttal_node)
    g.add_node("cmo_rebuttal", cmo_rebuttal_node)
    g.add_node("cbo_rebuttal", cbo_rebuttal_node)

    # Portfolio Director (stage 4 — synthesis)
    g.add_node("portfolio_director", portfolio_director_node)

    # --- Stage 1: START -> Scout ---
    g.add_edge(START, "scout")

    # --- Stage 2: Scout -> 4 parallel assessments (fan-out) ---
    g.add_edge("scout", "cso_assess")
    g.add_edge("scout", "cto_assess")
    g.add_edge("scout", "cmo_assess")
    g.add_edge("scout", "cbo_assess")

    # --- Fan-in: 4 assessments -> debate_router ---
    g.add_edge("cso_assess", "debate_router")
    g.add_edge("cto_assess", "debate_router")
    g.add_edge("cmo_assess", "debate_router")
    g.add_edge("cbo_assess", "debate_router")

    # --- Stage 3: debate_router -> 4 parallel rebuttals (fan-out) ---
    g.add_edge("debate_router", "cso_rebuttal")
    g.add_edge("debate_router", "cto_rebuttal")
    g.add_edge("debate_router", "cmo_rebuttal")
    g.add_edge("debate_router", "cbo_rebuttal")

    # --- Fan-in: 4 rebuttals -> portfolio_director ---
    g.add_edge("cso_rebuttal", "portfolio_director")
    g.add_edge("cto_rebuttal", "portfolio_director")
    g.add_edge("cmo_rebuttal", "portfolio_director")
    g.add_edge("cbo_rebuttal", "portfolio_director")

    # --- Conditional: portfolio_director -> END or loop back ---
    g.add_conditional_edges(
        "portfolio_director",
        _should_continue,
        {
            "end": END,
            "continue": "debate_router",
        },
    )

    return g.compile()


# ---------------------------------------------------------------------------
# Default empty state for initializing a run
# ---------------------------------------------------------------------------


def make_initial_state(query: str) -> APEXState:
    """Create a fresh initial state for a given query."""
    return APEXState(
        query=query,
        scout_data="",
        scout_sources=[],
        cso_assessment="",
        cto_assessment="",
        cmo_assessment="",
        cbo_assessment="",
        cso_rebuttal="",
        cto_rebuttal="",
        cmo_rebuttal="",
        cbo_rebuttal="",
        portfolio_verdict="",
        confidence_score=0,
        executive_scores={},
        ceo_feedback="",
        ceo_feedback_history=[],
        evaluation_round=0,
        debate_round=0,
        activity_log=[],
    )
