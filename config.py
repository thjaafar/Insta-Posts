"""
Central configuration for the Instagram Advice Agent.
All secrets are loaded from environment variables (see .env.example).
Never hardcode API keys directly in this file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM (content generation) ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-5")

# --- Image hosting (Instagram requires a public image URL) ---
# imgbb is free and simple: https://api.imgbb.com/ (get a free key)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

# --- Instagram Graph API ---
# Requires: Instagram Professional account linked to a Facebook Page,
# a Meta developer app, and a long-lived Page access token.
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN", "")
IG_BUSINESS_ACCOUNT_ID = os.getenv("IG_BUSINESS_ACCOUNT_ID", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v21.0")

# --- Scheduling ---
# 24hr local time, e.g. "09:00"
POST_TIME = os.getenv("POST_TIME", "09:00")

# --- Content settings ---
TOPICS = [
    "mindset", "discipline", "productivity", "confidence",
    "relationships", "money habits", "focus", "self-respect",
    "resilience", "decision-making", "habits", "growth",
]

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
HISTORY_FILE = os.path.join(DATA_DIR, "post_history.json")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated")
