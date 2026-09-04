"""
Publishes a single image post to Instagram via the Graph API.

Requirements (one-time setup, see README.md):
  1. Instagram account converted to a Professional (Business/Creator) account.
  2. That IG account linked to a Facebook Page.
  3. A Meta developer app with instagram_content_publish permission.
  4. A long-lived Page access token + your IG Business Account ID.

Flow: create a media container from the image URL -> publish that container.
"""

import time
import requests

import config

GRAPH_URL = f"https://graph.facebook.com/{config.GRAPH_API_VERSION}"


def _raise_with_body(resp, step_name):
    if not resp.ok:
        try:
            detail = resp.json()
        except ValueError:
            detail = resp.text
        raise RuntimeError(f"Instagram API error during {step_name}: {detail}")


def post_image(image_url: str, caption: str) -> str:
    if not config.IG_ACCESS_TOKEN or not config.IG_BUSINESS_ACCOUNT_ID:
        raise RuntimeError(
            "IG_ACCESS_TOKEN / IG_BUSINESS_ACCOUNT_ID not set. "
            "See README.md for how to obtain these from Meta for Developers."
        )

    # Step 1: create media container
    create_resp = requests.post(
        f"{GRAPH_URL}/{config.IG_BUSINESS_ACCOUNT_ID}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": config.IG_ACCESS_TOKEN,
        },
        timeout=30,
    )
    _raise_with_body(create_resp, "create media container")
    creation_id = create_resp.json()["id"]

    # Step 2: poll container status until it's ready to publish
    status = "IN_PROGRESS"
    for _ in range(10):
        status_resp = requests.get(
            f"{GRAPH_URL}/{creation_id}",
            params={"fields": "status_code", "access_token": config.IG_ACCESS_TOKEN},
            timeout=15,
        )
        _raise_with_body(status_resp, "check container status")
        status = status_resp.json().get("status_code", "IN_PROGRESS")
        if status == "FINISHED":
            break
        time.sleep(3)

    if status != "FINISHED":
        raise RuntimeError(f"Media container never finished processing (status={status})")

    # Step 3: publish
    publish_resp = requests.post(
        f"{GRAPH_URL}/{config.IG_BUSINESS_ACCOUNT_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": config.IG_ACCESS_TOKEN},
        timeout=30,
    )
    _raise_with_body(publish_resp, "publish media")
    return publish_resp.json()["id"]
