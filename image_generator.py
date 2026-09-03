"""
Renders a quote into a 1080x1080 Instagram-ready quote card.

Rotates through a small set of background/color themes so the feed
doesn't look identical every day. Uses a bundled system font with a
graceful fallback if it's unavailable.
"""

import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

import config

SIZE = 1080

THEMES = [
    {"bg": (18, 18, 20), "text": (245, 245, 245), "accent": (255, 209, 102)},
    {"bg": (250, 247, 242), "text": (30, 30, 30), "accent": (200, 60, 60)},
    {"bg": (24, 42, 43), "text": (240, 240, 235), "accent": (120, 200, 180)},
    {"bg": (36, 30, 60), "text": (240, 235, 250), "accent": (180, 140, 255)},
]

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def _load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _fit_text(draw, text, max_width, start_size=76, min_size=40):
    size = start_size
    while size >= min_size:
        font = _load_font(size)
        wrapped = textwrap.fill(text, width=max(10, int(max_width / (size * 0.55))))
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=14)
        if (bbox[2] - bbox[0]) <= max_width and (bbox[3] - bbox[1]) <= 640:
            return font, wrapped
        size -= 4
    return _load_font(min_size), textwrap.fill(text, width=24)


def render_quote_card(quote, topic, out_path):
    theme = random.choice(THEMES)
    img = Image.new("RGB", (SIZE, SIZE), theme["bg"])
    draw = ImageDraw.Draw(img)

    margin = 110
    max_text_width = SIZE - 2 * margin

    quote_text = f"\u201c{quote}\u201d"
    font, wrapped = _fit_text(draw, quote_text, max_text_width)

    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=14, align="center")
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (SIZE - text_w) / 2
    y = (SIZE - text_h) / 2 - 30

    draw.multiline_text((x, y), wrapped, font=font, fill=theme["text"], spacing=14, align="center")

    # accent rule above the quote
    rule_w = 90
    draw.rectangle(
        [(SIZE / 2 - rule_w / 2, y - 50), (SIZE / 2 + rule_w / 2, y - 44)],
        fill=theme["accent"],
    )

    # small topic tag at the bottom
    tag_font = _load_font(30)
    tag_text = topic.upper()
    tag_bbox = draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = tag_bbox[2] - tag_bbox[0]
    draw.text(((SIZE - tag_w) / 2, SIZE - 130), tag_text, font=tag_font, fill=theme["accent"])

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    path = os.path.join(config.OUTPUT_DIR, "preview.png")
    render_quote_card(
        "Discipline is just choosing what you want most over what you want now.",
        "discipline",
        path,
    )
    print(f"Saved preview to {path}")
