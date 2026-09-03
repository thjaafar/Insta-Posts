"""
Instagram's Graph API requires a publicly reachable image URL — it will
not accept a raw file upload. This module pushes the rendered quote card
to imgbb (free tier, no credit card) and returns the public URL.

Swap this out for S3 / Cloudinary / your own storage if you prefer —
just keep the `upload(path) -> url` interface.
"""

import base64
import requests

import config


def upload(image_path: str) -> str:
    if not config.IMGBB_API_KEY:
        raise RuntimeError(
            "IMGBB_API_KEY not set. Get a free key at https://api.imgbb.com/ "
            "and add it to your .env file."
        )

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read())

    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        data={"key": config.IMGBB_API_KEY, "image": encoded},
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    return payload["data"]["url"]
