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

**Instagram Graph API (the fiddly one)**
1. Your Instagram account must be a **Professional account** (Business or
   Creator) — Settings → Account type in the Instagram app.
2. Link it to a **Facebook Page** (Instagram settings → Linked accounts).
3. Go to developers.facebook.com → create an app → add the
   **Instagram Graph API** product.
4. Use the Graph API Explorer (or the app's token tool) to generate a
   **Page access token** with these permissions: `instagram_basic`,
   `instagram_content_publish`, `pages_read_engagement`.
5. Exchange it for a **long-lived token** (60 days) using the
   `oauth/access_token` endpoint with `grant_type=fb_exchange_token` —
   Meta's docs walk through this exact call.
6. Find your `IG_BUSINESS_ACCOUNT_ID` by calling:
   `GET /me/accounts` → get your Page ID → then
   `GET /{page-id}?fields=instagram_business_account`.
7. Put the token and account ID into `.env`.

Long-lived tokens expire every ~60 days — you'll need to refresh
`IG_ACCESS_TOKEN` periodically, or build a refresh step if you want this
to run unattended for months.

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
