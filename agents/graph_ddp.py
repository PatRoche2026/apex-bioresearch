"""DDP LangGraph pipeline — runs after CEO accepts a GO verdict.

Topology:
    START → ddp_prep
      → [cso_plan, cto_plan, cmo_plan, cbo_plan]   (parallel fan-out)
      → ddp_sync                                     (no-op fan-in sync)
      → ddp_director
      → END

No conditional loop — the DDP is a single-pass plan, not a debate.
"""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from agents.planning import (
    cbo_plan_node,
    cmo_plan_node,
    cso_plan_node,
    cto_plan_node,
    ddp_director_node,
)
from agents.state import APEXState


# ---------------------------------------------------------------------------
# Prep node — extracts gene / indication from query and stores on state
# ---------------------------------------------------------------------------


def _ddp_prep_node(state: APEXState) -> dict[str, Any]:
    """Extract gene and indication from query if not already set.

    Heuristic: first token = gene symbol, remainder = indication.
    Example: "OSMR ulcerative colitis" → gene="OSMR", indication="ulcerative colitis"
    """
    if state.get("gene") and state.get("indication"):
        return {}  # Already extracted (e.g. from a prior run)

    tokens = state["query"].strip().split()
    gene = tokens[0].upper() if tokens else state["query"]
    indication = " ".join(tokens[1:]) if len(tokens) > 1 else state["query"]

    return {"gene": gene, "indication": indication}


# ---------------------------------------------------------------------------
# Build the DDP graph
# ---------------------------------------------------------------------------


def build_ddp_graph() -> StateGraph:
    """Build and compile the DDP planning pipeline.

    Topology:
        START → ddp_prep
          → [cso_plan, cto_plan, cmo_plan, cbo_plan]  (parallel)
          → ddp_sync  (no-op fan-in)
          → ddp_director
          → END
    """
    g = StateGraph(APEXState)

    # Prep node
    g.add_node("ddp_prep", _ddp_prep_node)

    # 4 parallel planning nodes
    g.add_node("cso_plan", cso_plan_node)
    g.add_node("cto_plan", cto_plan_node)
    g.add_node("cmo_plan", cmo_plan_node)
    g.add_node("cbo_plan", cbo_plan_node)

    # Fan-in sync (no-op)
    g.add_node("ddp_sync", lambda state: {})

    # Director synthesis
    g.add_node("ddp_director", ddp_director_node)

    # --- Edges ---
    g.add_edge(START, "ddp_prep")

    # Fan-out: prep → 4 parallel planning nodes
    g.add_edge("ddp_prep", "cso_plan")
    g.add_edge("ddp_prep", "cto_plan")
    g.add_edge("ddp_prep", "cmo_plan")
    g.add_edge("ddp_prep", "cbo_plan")

    # Fan-in: 4 nodes → sync point
    g.add_edge("cso_plan", "ddp_sync")
    g.add_edge("cto_plan", "ddp_sync")
    g.add_edge("cmo_plan", "ddp_sync")
    g.add_edge("cbo_plan", "ddp_sync")

    # Sync → director → end
    g.add_edge("ddp_sync", "ddp_director")
    g.add_edge("ddp_director", END)

    return g.compile()


# ---------------------------------------------------------------------------
# State initialiser — takes a completed APEXState, clears DDP output fields
# ---------------------------------------------------------------------------


def make_ddp_state(eval_state: APEXState) -> APEXState:
    """Prepare a state for the DDP pipeline from a completed evaluation state.

    Carries forward all evaluation outputs (assessments, rebuttals, verdict,
    CEO feedback) so planning nodes have full deliberation context.
    Resets DDP output fields so the graph writes fresh sections.
    """
    state = dict(eval_state)  # shallow copy
    state["gene"] = ""         # let ddp_prep extract from query
    state["indication"] = ""
    state["cso_ddp_section"] = ""
    state["cto_ddp_section"] = ""
    state["cmo_ddp_section"] = ""
    state["cbo_ddp_section"] = ""
    state["ddp_synthesis"] = ""
    return APEXState(**state)  # type: ignore[misc]
