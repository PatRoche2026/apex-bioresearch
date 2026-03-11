"""APEX Backend — FastAPI + WebSocket streaming + REST endpoints."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from agents.graph import build_graph, make_initial_state
from agents.prompts import AGENT_PERSONAS
from agents.state import APEXState

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="APEX — Agentic Pipeline for Executive Decisions",
    description=(
        "Multi-agent biotech executive debate system. "
        "5 AI agents evaluate drug targets through parallel assessment, "
        "structured debate, and Portfolio Director synthesis."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory session storage
# ---------------------------------------------------------------------------

sessions: dict[str, dict[str, Any]] = {}

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class EvaluateRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Drug target evaluation query (e.g. 'OSMR ulcerative colitis')",
    )


class FeedbackRequest(BaseModel):
    feedback: str = Field(
        ...,
        min_length=3,
        description="CEO feedback to inject into the next evaluation round",
    )


class SessionSummary(BaseModel):
    session_id: str
    query: str
    status: str
    confidence_score: int
    verdict: str
    debate_rounds: int
    timestamp: str


# ---------------------------------------------------------------------------
# Node name mapping for WebSocket events
# ---------------------------------------------------------------------------

_NODE_AGENT_MAP = {
    "scout": "scout",
    "cso_assess": "cso",
    "cto_assess": "cto",
    "cmo_assess": "cmo",
    "cbo_assess": "cbo",
    "debate_router": "system",
    "cso_rebuttal": "cso",
    "cto_rebuttal": "cto",
    "cmo_rebuttal": "cmo",
    "cbo_rebuttal": "cbo",
    "portfolio_director": "portfolio_director",
}

_NODE_TYPE_MAP = {
    "scout": "scout",
    "cso_assess": "assessment",
    "cto_assess": "assessment",
    "cmo_assess": "assessment",
    "cbo_assess": "assessment",
    "debate_router": "sync",
    "cso_rebuttal": "rebuttal",
    "cto_rebuttal": "rebuttal",
    "cmo_rebuttal": "rebuttal",
    "cbo_rebuttal": "rebuttal",
    "portfolio_director": "verdict",
}


def _parse_verdict_short(text: str) -> str:
    """Extract short verdict from portfolio verdict text. NO-GO checked first."""
    upper = text.upper()
    if "NO-GO" in upper or "NO GO" in upper:
        return "NO-GO"
    if "CONDITIONAL GO" in upper:
        return "CONDITIONAL GO"
    if "GO" in upper:
        return "GO"
    return "CONDITIONAL GO"


def _sum_costs(result: dict) -> float:
    """Sum all cost_usd values from activity_log entries."""
    total = 0.0
    for entry in result.get("activity_log", []):
        total += entry.get("cost_usd", 0.0)
    return round(total, 4)


def _extract_event_data(node_name: str, node_data: dict) -> dict:
    """Extract the relevant content field from a node's output for the frontend."""
    if node_data is None:
        return {}

    # Map node to its primary content field
    field_map = {
        "scout": ("scout_data", "scout_sources"),
        "cso_assess": ("cso_assessment",),
        "cto_assess": ("cto_assessment",),
        "cmo_assess": ("cmo_assessment",),
        "cbo_assess": ("cbo_assessment",),
        "cso_rebuttal": ("cso_rebuttal",),
        "cto_rebuttal": ("cto_rebuttal",),
        "cmo_rebuttal": ("cmo_rebuttal",),
        "cbo_rebuttal": ("cbo_rebuttal",),
        "portfolio_director": ("portfolio_verdict", "confidence_score", "executive_scores", "debate_round"),
    }

    fields = field_map.get(node_name, ())
    data = {}
    for f in fields:
        if f in node_data:
            data[f] = node_data[f]

    # Include parsed scores if present
    if "executive_scores" in node_data and node_name != "portfolio_director":
        data["scores"] = node_data["executive_scores"]

    return data


# ---------------------------------------------------------------------------
# REST Endpoints
# ---------------------------------------------------------------------------


@app.get("/")
def root():
    """App info and available endpoints."""
    return {
        "app": "APEX",
        "tagline": "Agentic Pipeline for Executive Decisions",
        "description": (
            "Multi-agent biotech executive debate system. "
            "5 AI agents (CSO, CTO, CMO, CBO, Portfolio Director) evaluate "
            "drug targets through parallel assessment, structured debate, "
            "and investment committee synthesis."
        ),
        "version": "1.0.0",
        "endpoints": {
            "GET /": "App info",
            "GET /personas": "Agent persona metadata",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "POST /evaluate": "Run full evaluation (synchronous)",
            "POST /feedback/{session_id}": "Submit CEO feedback for re-evaluation",
            "WS /ws/evaluate": "WebSocket streaming evaluation",
            "WS /ws/feedback/{session_id}": "WebSocket streaming re-evaluation with CEO feedback",
            "GET /results/{session_id}": "Fetch completed evaluation results",
            "GET /sessions": "List all completed sessions",
            "GET /export/{session_id}": "Download Markdown report",
        },
        "example_queries": [
            "OSMR ulcerative colitis",
            "GLP-1 receptor agonists Alzheimer's disease",
            "CD47 cancer immunotherapy",
        ],
        "architecture": {
            "agents": ["Research Scout", "CSO", "CTO", "CMO", "CBO", "Portfolio Director"],
            "flow": "Scout -> 4 parallel assessments -> Debate rebuttals -> Portfolio Director verdict",
            "conditional_loop": "If confidence < 60%, agents debate again (max 2 rounds)",
            "ceo_feedback": "Human-in-the-loop: submit CEO feedback to trigger re-evaluation with directives",
            "domain_tools": {
                "CSO": ["PubMed", "UniProt", "STRING-DB"],
                "CTO": ["PubMed", "ChEMBL", "Open Targets Tractability"],
                "CMO": ["ClinicalTrials.gov", "PubMed", "Open Targets Safety"],
                "CBO": ["PubMed", "Open Targets", "ClinicalTrials.gov"],
            },
        },
        "author": "Patrick Roche, MIT Media Lab MAS.664",
    }


@app.get("/personas")
def personas():
    """Return agent persona metadata for frontend rendering."""
    return {"personas": AGENT_PERSONAS}


@app.get("/health")
def health():
    """Health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sessions_completed": len(sessions),
    }


@app.post("/evaluate")
async def evaluate(req: EvaluateRequest):
    """Run a full synchronous evaluation. Returns the complete result."""
    session_id = str(uuid.uuid4())
    graph = build_graph()
    state = make_initial_state(req.query)

    result = await graph.ainvoke(state)

    # Store session
    sessions[session_id] = {
        "session_id": session_id,
        "query": req.query,
        "status": "complete",
        "result": result,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "session_id": session_id,
        "query": req.query,
        "confidence_score": result.get("confidence_score", 0),
        "debate_rounds": result.get("debate_round", 0),
        "verdict": result.get("portfolio_verdict", ""),
        "executive_scores": result.get("executive_scores", {}),
        "scout_sources": result.get("scout_sources", []),
        "assessments": {
            "cso": result.get("cso_assessment", ""),
            "cto": result.get("cto_assessment", ""),
            "cmo": result.get("cmo_assessment", ""),
            "cbo": result.get("cbo_assessment", ""),
        },
        "rebuttals": {
            "cso": result.get("cso_rebuttal", ""),
            "cto": result.get("cto_rebuttal", ""),
            "cmo": result.get("cmo_rebuttal", ""),
            "cbo": result.get("cbo_rebuttal", ""),
        },
        "activity_log": result.get("activity_log", []),
        "estimated_cost_usd": _sum_costs(result),
    }


@app.get("/results/{session_id}")
def get_results(session_id: str):
    """Fetch completed evaluation results by session ID."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    session = sessions[session_id]
    result = session["result"]

    return {
        "session_id": session_id,
        "query": session["query"],
        "status": session["status"],
        "confidence_score": result.get("confidence_score", 0),
        "debate_rounds": result.get("debate_round", 0),
        "verdict": result.get("portfolio_verdict", ""),
        "executive_scores": result.get("executive_scores", {}),
        "scout_sources": result.get("scout_sources", []),
        "assessments": {
            "cso": result.get("cso_assessment", ""),
            "cto": result.get("cto_assessment", ""),
            "cmo": result.get("cmo_assessment", ""),
            "cbo": result.get("cbo_assessment", ""),
        },
        "rebuttals": {
            "cso": result.get("cso_rebuttal", ""),
            "cto": result.get("cto_rebuttal", ""),
            "cmo": result.get("cmo_rebuttal", ""),
            "cbo": result.get("cbo_rebuttal", ""),
        },
        "activity_log": result.get("activity_log", []),
        "estimated_cost_usd": _sum_costs(result),
        "timestamp": session["timestamp"],
    }


@app.get("/sessions")
def list_sessions():
    """List all completed evaluation sessions."""
    summaries = []
    for sid, session in sessions.items():
        result = session["result"]
        verdict_short = _parse_verdict_short(result.get("portfolio_verdict", ""))

        summaries.append({
            "session_id": sid,
            "query": session["query"],
            "status": session["status"],
            "confidence_score": result.get("confidence_score", 0),
            "verdict": verdict_short,
            "debate_rounds": result.get("debate_round", 0),
            "timestamp": session["timestamp"],
        })
    return {"sessions": summaries, "count": len(summaries)}


@app.get("/export/{session_id}")
def export_session(session_id: str):
    """Export a completed evaluation as a downloadable Markdown report."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    session = sessions[session_id]
    result = session["result"]

    report = _generate_markdown_report(session["query"], result, session_id)
    return Response(
        content=report,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=apex-{session_id[:8]}.md"},
    )


def _generate_markdown_report(query: str, result: dict, session_id: str) -> str:
    """Generate a formatted Markdown report of the full debate."""
    lines = [
        f"# APEX Evaluation Report",
        f"**Query:** {query}",
        f"**Session:** {session_id[:8]}",
        f"**Confidence:** {result.get('confidence_score', 'N/A')}%",
        f"**Debate Rounds:** {result.get('debate_round', 'N/A')}",
        "",
        "---",
        "",
        "## Research Scout Summary",
        "",
        f"**Sources:** {len(result.get('scout_sources', []))} papers analyzed",
        "",
    ]

    for src in result.get("scout_sources", []):
        lines.append(f"- **PMID {src['pmid']}**: {src['title']} — {src['journal']} ({src['year']})")
    lines.append("")

    # Assessments
    for role, label in [("cso", "CSO"), ("cto", "CTO"), ("cmo", "CMO"), ("cbo", "CBO")]:
        lines.append(f"---\n\n## {label} Assessment\n")
        lines.append(result.get(f"{role}_assessment", "*No assessment available*"))
        lines.append("")

    # Rebuttals
    lines.append("---\n\n# Debate Rebuttals\n")
    for role, label in [("cso", "CSO"), ("cto", "CTO"), ("cmo", "CMO"), ("cbo", "CBO")]:
        lines.append(f"## {label} Rebuttal\n")
        lines.append(result.get(f"{role}_rebuttal", "*No rebuttal available*"))
        lines.append("")

    # Verdict
    lines.append("---\n\n# Portfolio Director Verdict\n")
    lines.append(result.get("portfolio_verdict", "*No verdict available*"))
    lines.append("")

    # Scores
    scores = result.get("executive_scores", {})
    if "per_dimension" in scores:
        lines.append("\n## Weighted Scores\n")
        for dim, val in scores["per_dimension"].items():
            lines.append(f"- **{dim.replace('_', ' ').title()}:** {val}/10")
        lines.append(f"- **Weighted Total:** {scores.get('weighted_total', 'N/A')}/10")

    lines.append(f"\n---\n\n*Generated by APEX — Agentic Pipeline for Executive Decisions*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CEO Feedback Endpoint — Human-in-the-Loop (Feature 4)
# ---------------------------------------------------------------------------


@app.post("/feedback/{session_id}")
async def submit_feedback(session_id: str, req: FeedbackRequest):
    """Submit CEO feedback on a completed evaluation, triggering a re-evaluation.

    The feedback is injected into agent prompts for the next round.
    Returns a new session_id for the re-evaluation.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    session = sessions[session_id]
    if session["status"] != "complete":
        raise HTTPException(status_code=400, detail="Session is not complete yet")

    original_result = session["result"]
    original_query = session["query"]
    eval_round = original_result.get("evaluation_round", 0) + 1

    # Create new session for re-evaluation
    new_session_id = str(uuid.uuid4())
    graph = build_graph()

    # Build state with CEO feedback + previous scout data (skip re-scouting)
    state = make_initial_state(original_query)
    state["ceo_feedback"] = req.feedback
    state["ceo_feedback_history"] = original_result.get("ceo_feedback_history", []) + [
        {
            "feedback": req.feedback,
            "round": eval_round,
            "from_session": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    ]
    state["evaluation_round"] = eval_round
    # Carry forward scout data to avoid redundant PubMed calls
    state["scout_data"] = original_result.get("scout_data", "")
    state["scout_sources"] = original_result.get("scout_sources", [])

    result = await graph.ainvoke(state)

    sessions[new_session_id] = {
        "session_id": new_session_id,
        "query": original_query,
        "status": "complete",
        "result": result,
        "parent_session": session_id,
        "ceo_feedback": req.feedback,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "session_id": new_session_id,
        "parent_session": session_id,
        "evaluation_round": eval_round,
        "ceo_feedback": req.feedback,
        "confidence_score": result.get("confidence_score", 0),
        "verdict": result.get("portfolio_verdict", "")[:200],
        "debate_rounds": result.get("debate_round", 0),
        "estimated_cost_usd": _sum_costs(result),
    }


# ---------------------------------------------------------------------------
# WebSocket Feedback — streaming re-evaluation with CEO feedback
# ---------------------------------------------------------------------------


@app.websocket("/ws/feedback/{session_id}")
async def ws_feedback(websocket: WebSocket, session_id: str):
    """WebSocket streaming re-evaluation with CEO feedback.

    Client sends: {"feedback": "Focus more on safety profile"}
    Server streams the full re-evaluation with CEO feedback injected.
    """
    await websocket.accept()

    try:
        if session_id not in sessions:
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": f"Session {session_id} not found"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await websocket.close()
            return

        session = sessions[session_id]
        if session["status"] != "complete":
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": "Session is not complete yet"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await websocket.close()
            return

        data = await websocket.receive_json()
        feedback = data.get("feedback", "").strip()

        if not feedback or len(feedback) < 3:
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": "Feedback must be at least 3 characters"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await websocket.close()
            return

        original_result = session["result"]
        original_query = session["query"]
        eval_round = original_result.get("evaluation_round", 0) + 1
        new_session_id = str(uuid.uuid4())

        # Send session start
        await websocket.send_json({
            "type": "session_start",
            "node": "system",
            "data": {
                "session_id": new_session_id,
                "query": original_query,
                "parent_session": session_id,
                "evaluation_round": eval_round,
                "ceo_feedback": feedback,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        graph = build_graph()
        state = make_initial_state(original_query)
        state["ceo_feedback"] = feedback
        state["ceo_feedback_history"] = original_result.get("ceo_feedback_history", []) + [
            {
                "feedback": feedback,
                "round": eval_round,
                "from_session": session_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]
        state["evaluation_round"] = eval_round
        state["scout_data"] = original_result.get("scout_data", "")
        state["scout_sources"] = original_result.get("scout_sources", [])

        current_round = 0
        final_result = dict(state)

        async for event in graph.astream(state, stream_mode="updates"):
            for node_name, node_data in event.items():
                ts = datetime.now(timezone.utc).isoformat()

                if node_data is None:
                    continue

                if node_name == "portfolio_director":
                    current_round += 1

                agent_role = _NODE_AGENT_MAP.get(node_name, "system")
                persona = AGENT_PERSONAS.get(agent_role, {})
                await websocket.send_json({
                    "type": "node_complete",
                    "node": node_name,
                    "agent": agent_role,
                    "persona": persona,
                    "data": _extract_event_data(node_name, node_data),
                    "timestamp": ts,
                })

                for k, v in node_data.items():
                    if k == "activity_log":
                        final_result.setdefault("activity_log", []).extend(v)
                    elif k == "executive_scores" and isinstance(v, dict):
                        final_result.setdefault("executive_scores", {}).update(v)
                    else:
                        final_result[k] = v

        sessions[new_session_id] = {
            "session_id": new_session_id,
            "query": original_query,
            "status": "complete",
            "result": final_result,
            "parent_session": session_id,
            "ceo_feedback": feedback,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        verdict_short = _parse_verdict_short(final_result.get("portfolio_verdict", ""))
        await websocket.send_json({
            "type": "complete",
            "node": "system",
            "data": {
                "session_id": new_session_id,
                "parent_session": session_id,
                "evaluation_round": eval_round,
                "ceo_feedback": feedback,
                "confidence_score": final_result.get("confidence_score", 0),
                "verdict": verdict_short,
                "debate_rounds": final_result.get("debate_round", 0),
                "estimated_cost_usd": _sum_costs(final_result),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": str(e)[:500]},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        except Exception:
            pass
        try:
            await websocket.close()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# WebSocket Endpoint — THE CORE DIFFERENTIATOR
# ---------------------------------------------------------------------------


@app.websocket("/ws/evaluate")
async def ws_evaluate(websocket: WebSocket):
    """WebSocket streaming evaluation.

    Client sends: {"query": "OSMR ulcerative colitis"}
    Server streams events as each node completes.
    """
    await websocket.accept()

    try:
        data = await websocket.receive_json()
        query = data.get("query", "").strip()

        if not query or len(query) < 3:
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": "Query must be at least 3 characters"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await websocket.close()
            return

        session_id = str(uuid.uuid4())

        # Send session start event
        await websocket.send_json({
            "type": "session_start",
            "node": "system",
            "data": {"session_id": session_id, "query": query},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        graph = build_graph()
        state = make_initial_state(query)
        current_round = 0
        final_result = dict(state)

        async for event in graph.astream(state, stream_mode="updates"):
            for node_name, node_data in event.items():
                ts = datetime.now(timezone.utc).isoformat()

                # Skip None data (pass-through nodes)
                if node_data is None:
                    continue

                # Track debate rounds
                if node_name == "portfolio_director":
                    current_round += 1
                    new_round = node_data.get("debate_round", current_round)
                    if new_round > current_round:
                        # Entering a new debate round
                        await websocket.send_json({
                            "type": "debate_round",
                            "node": "system",
                            "data": {"round": new_round},
                            "timestamp": ts,
                        })

                # Send node_complete event with persona metadata
                agent_role = _NODE_AGENT_MAP.get(node_name, "system")
                persona = AGENT_PERSONAS.get(agent_role, {})
                await websocket.send_json({
                    "type": "node_complete",
                    "node": node_name,
                    "agent": agent_role,
                    "persona": persona,
                    "data": _extract_event_data(node_name, node_data),
                    "timestamp": ts,
                })

                # Update final result
                for k, v in node_data.items():
                    if k == "activity_log":
                        final_result.setdefault("activity_log", []).extend(v)
                    elif k == "executive_scores" and isinstance(v, dict):
                        final_result.setdefault("executive_scores", {}).update(v)
                    else:
                        final_result[k] = v

        # Store session
        sessions[session_id] = {
            "session_id": session_id,
            "query": query,
            "status": "complete",
            "result": final_result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Send completion event with parsed verdict
        verdict_short = _parse_verdict_short(final_result.get("portfolio_verdict", ""))
        await websocket.send_json({
            "type": "complete",
            "node": "system",
            "data": {
                "session_id": session_id,
                "confidence_score": final_result.get("confidence_score", 0),
                "verdict": verdict_short,
                "debate_rounds": final_result.get("debate_round", 0),
                "weighted_total": final_result.get("executive_scores", {}).get("weighted_total"),
                "estimated_cost_usd": _sum_costs(final_result),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        sessions[session_id]["result"]["_verdict_short"] = verdict_short

    except WebSocketDisconnect:
        pass  # Client disconnected mid-evaluation
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "node": "system",
                "data": {"message": str(e)[:500]},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        except Exception:
            pass
        try:
            await websocket.close()
        except Exception:
            pass
