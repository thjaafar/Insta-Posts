"""
Full daily pipeline:
  1. Generate advice quote + caption + hashtags
  2. Render quote card image
  3. Upload image to get a public URL
  4. Post to Instagram

Run this once per day (via cron / a hosting platform's scheduler — see
README.md for setup options). Use --dry-run to test steps 1-2 only,
without needing IG/imgbb credentials.
"""

import argparse
import os
import sys
import traceback
from datetime import datetime

import config
import generate_content
import image_generator
import image_host
import instagram_poster


def run(dry_run: bool = False):
    print(f"[{datetime.now().isoformat()}] Starting daily advice post run "
          f"(dry_run={dry_run})")

    content = generate_content.generate()
    print(f"  Topic: {content['topic']}")
    print(f"  Quote: {content['quote']}")

    filename = f"advice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    out_path = os.path.join(config.OUTPUT_DIR, filename)
    image_generator.render_quote_card(content["quote"], content["topic"], out_path)
    print(f"  Image saved: {out_path}")

    if dry_run:
        print("  [dry-run] Skipping upload + Instagram post.")
        return

    image_url = image_host.upload(out_path)
    print(f"  Image hosted: {image_url}")

    caption = content["caption"] + "\n\n" + " ".join(content["hashtags"])
    post_id = instagram_poster.post_image(image_url, caption)
    print(f"  Posted to Instagram. Media ID: {post_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Instagram advice agent")
    parser.add_argument("--dry-run", action="store_true",
                         help="Generate content + image only, skip posting")
    args = parser.parse_args()

    try:
        run(dry_run=args.dry_run)
    except Exception:
        print("ERROR: pipeline failed", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
