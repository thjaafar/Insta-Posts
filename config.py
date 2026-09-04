"""
Central configuration for the Instagram Advice Agent.
All secrets are loaded from environment variables (see .env.example).
Never hardcode API keys directly in this file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- LLM (content generation) ---
# Get a free key with no card/ID required at https://aistudio.google.com/
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-flash-latest")

# --- Image hosting (Instagram requires a public image URL) ---
# imgbb is free and simple: https://api.imgbb.com/ (get a free key)
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")

# --- Instagram API (using "Instagram API with Instagram Login") ---
# Get these from your Meta app dashboard's Instagram > API setup page:
# the "Generate token" button gives you IG_ACCESS_TOKEN, and the account ID
# shown next to your Instagram account (e.g. 178414...) is IG_BUSINESS_ACCOUNT_ID.
IG_ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN", "")
IG_BUSINESS_ACCOUNT_ID = os.getenv("IG_BUSINESS_ACCOUNT_ID", "")
GRAPH_API_VERSION = os.getenv("GRAPH_API_VERSION", "v21.0")
# graph.instagram.com for Instagram Login apps (no Facebook Page needed);
# graph.facebook.com for the older Facebook-Login-linked-Page flow.
GRAPH_HOST = os.getenv("GRAPH_HOST", "graph.instagram.com")

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
