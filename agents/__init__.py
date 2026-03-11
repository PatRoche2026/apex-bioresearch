"""APEX agents package — shared configuration and .env loading."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------------------------

# Try local .env first, then fall back to hw4-build/.env
_local_env = Path(__file__).resolve().parent.parent / ".env"
_hw4_env = Path(__file__).resolve().parent.parent.parent / "hw4-build" / ".env"

if _local_env.exists():
    load_dotenv(_local_env)
elif _hw4_env.exists():
    load_dotenv(_hw4_env)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ---------------------------------------------------------------------------
# Shared LLM configuration
# ---------------------------------------------------------------------------

LLM_MODEL = "claude-sonnet-4-20250514"
LLM_TEMPERATURE = 0.3

# ---------------------------------------------------------------------------
# Rate limit protection — asyncio.Semaphore(3) for parallel LLM calls
# ---------------------------------------------------------------------------

llm_semaphore = asyncio.Semaphore(3)
LLM_TIMEOUT_SECONDS = 60

# ---------------------------------------------------------------------------
# PubMed configuration
# ---------------------------------------------------------------------------

ENTREZ_EMAIL = "patroche@mit.edu"
PUBMED_RATE_LIMIT_DELAY = 0.5  # seconds between NCBI API calls
