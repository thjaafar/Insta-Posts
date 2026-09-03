"""
Generates one piece of daily advice content:
  - a short, punchy quote (for the image)
  - an Instagram caption (with a hook + hashtags)
  - a topic tag (for history/variety tracking)

Uses the Anthropic API. Falls back to a local template bank if no
API key is configured, so the agent still runs end-to-end for testing.
"""

import json
import os
import random
import requests

import config


def _load_history():
    os.makedirs(config.DATA_DIR, exist_ok=True)
    if os.path.exists(config.HISTORY_FILE):
        with open(config.HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"quotes": [], "topics_used": []}


def _save_history(history):
    with open(config.HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def _pick_topic(history):
    # Favor topics used least recently
    recent = history["topics_used"][-5:]
    candidates = [t for t in config.TOPICS if t not in recent] or config.TOPICS
    return random.choice(candidates)


def _call_claude(topic, past_quotes):
    if not config.ANTHROPIC_API_KEY:
        return None

    avoid = "\n".join(f"- {q}" for q in past_quotes[-15:]) or "(none yet)"
    prompt = f"""Write one piece of short daily-advice content for an Instagram
quote-card account about "{topic}".

Avoid repeating the spirit of these previous quotes:
{avoid}

Return ONLY valid JSON, no markdown fences, in this exact shape:
{{
  "quote": "the punchy quote/advice line, under 18 words, no hashtags, no quotation marks",
  "caption": "a 2-4 sentence Instagram caption expanding on the quote, conversational, ends with a question to drive comments",
  "hashtags": ["#tag1", "#tag2", "... 8-12 relevant hashtags mixing broad and niche"]
}}"""

    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": config.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": config.LLM_MODEL,
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    resp.raise_for_status()
    text = resp.json()["content"][0]["text"].strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)


_FALLBACK_BANK = {
    "mindset": "Your mindset is the one thing that scales every other skill you have.",
    "discipline": "Discipline is just choosing what you want most over what you want now.",
    "productivity": "You don't need more hours. You need fewer distractions.",
    "confidence": "Confidence is built in the moments you almost quit and didn't.",
    "relationships": "The people who ask about your goals twice actually care.",
    "money habits": "Track it before you grow it.",
    "focus": "One task done beats five tasks started.",
    "self-respect": "Say less about your plans. Let the results talk.",
    "resilience": "You're not behind. You're just early in a story you can't see the end of.",
    "decision-making": "A decided life feels lighter than an open one.",
    "habits": "You don't rise to your goals, you fall to your habits.",
    "growth": "Comfort and growth don't share a room.",
}


def generate():
    history = _load_history()
    topic = _pick_topic(history)

    data = None
    try:
        data = _call_claude(topic, history["quotes"])
    except Exception as e:
        print(f"[generate_content] LLM call failed, using fallback: {e}")

    if not data:
        quote = _FALLBACK_BANK.get(topic, "Small daily discipline beats big rare effort.")
        data = {
            "quote": quote,
            "caption": f"{quote}\n\nWhat's one small habit that changed your {topic}? Tell me below.",
            "hashtags": ["#dailyadvice", "#motivation", "#mindset", f"#{topic.replace(' ', '')}",
                         "#selfimprovement", "#growthmindset", "#discipline", "#successhabits"],
        }

    data["topic"] = topic
    history["quotes"].append(data["quote"])
    history["topics_used"].append(topic)
    history["quotes"] = history["quotes"][-100:]
    history["topics_used"] = history["topics_used"][-30:]
    _save_history(history)

    return data


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2))
