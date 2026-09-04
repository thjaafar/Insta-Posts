# Instagram Daily Advice Agent

A fully automated agent that generates a daily advice quote card and posts
it to Instagram on its own.

**Pipeline:** generate quote + caption (Claude) → render quote card (Pillow)
→ upload image (imgbb) → publish to Instagram (Graph API).

## 1. Install

```bash
cd ig_advice_agent
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with the keys below.

## 2. Get your API keys

**Google Gemini (content generation)**
- aistudio.google.com → sign in with a Google account → create an API key
  → `GEMINI_API_KEY`
- No credit card or ID verification required, and the free tier
  (Gemini Flash) comfortably covers one post a day.
- If you skip this, the agent still runs using a built-in fallback quote
  bank, just with less variety.

**imgbb (image hosting)**
- api.imgbb.com → free account → API key → `IMGBB_API_KEY`
- Instagram's API requires a public image URL, not a file upload — this
  is what makes that possible without you running your own server.

**Instagram API (the fiddly one — but simpler than it used to be)**

You're using **"Instagram API with Instagram Login"** — Meta's newer, simpler
setup that doesn't require linking a Facebook Page.

1. Your Instagram account must be a **Professional account** (Business or
   Creator) — Settings → Account type in the Instagram app.
2. Go to developers.facebook.com → create an app (or use your existing one)
   → add the **Instagram** product.
3. On the app's Instagram setup page, under "Generate access tokens", click
   **Add account** and add your Instagram account (you may need to assign
   it the Instagram Tester role under the Roles tab first, and accept the
   invite from the Instagram app itself).
4. Click **"Generate token"** next to your account. Copy that value —
   this is your `IG_ACCESS_TOKEN`.
5. The numeric ID shown right under your Instagram username on that same
   page (e.g. `178414...`) is your `IG_BUSINESS_ACCOUNT_ID`.
6. Leave `GRAPH_HOST` as the default (`graph.instagram.com`) — this is
   what this login flow uses; the old Facebook-linked flow used
   `graph.facebook.com` instead, if you ever switch approaches.

This token type doesn't need the long-lived-token exchange step the
Facebook-linked flow requires — the token from "Generate token" is
already usable directly, though it will still expire eventually and need
regenerating.

## 3. Test it (no posting yet)

```bash
python3 main.py --dry-run
```

This generates a quote and saves the image to `generated/` without
touching imgbb or Instagram. Open the image to check it looks right.

## 4. Run it for real

```bash
python3 main.py
```

This generates, uploads, and publishes a live Instagram post.

## 5. Automate it to run daily

Simplest option — cron (Linux/Mac), runs every day at 9am:

```bash
crontab -e
# add this line:
0 9 * * * cd /path/to/ig_advice_agent && /usr/bin/python3 main.py >> run.log 2>&1
```

If you want this running 24/7 without your own machine, deploy the
folder to a small always-on host (Railway, Render, a $5 VPS, etc.) and
set up their scheduled-job / cron feature to run `python3 main.py` once
a day.

## Files

| File | Purpose |
|---|---|
| `config.py` | Loads all settings/keys from `.env` |
| `generate_content.py` | Generates the quote, caption, hashtags; avoids repeating recent topics/quotes |
| `image_generator.py` | Renders the quote as a 1080x1080 quote card (Pillow) |
| `image_host.py` | Uploads the image to imgbb for a public URL |
| `instagram_poster.py` | Publishes the post via the Instagram Graph API |
| `main.py` | Orchestrates the full pipeline; `--dry-run` skips posting |
| `data/post_history.json` | Tracks recent quotes/topics so content stays varied |

## Notes on "going viral"

No tool can guarantee virality — that depends on hook quality, timing,
and audience fit as much as content. To improve odds over time:
- Check Instagram Insights weekly and feed your best-performing topics
  back into `config.TOPICS` (weight them higher).
- Post consistently — daily cadence matters more to the algorithm than
  any single post's polish.
- Consider adding Reels (short video) later; quote cards are a solid,
  low-effort starting format but video generally reaches further on IG.
