import re
from collections import Counter
from html.parser import HTMLParser
from typing import Optional
from urllib.parse import urlparse

import requests

from .design_service import deep_merge, profile_for_industry

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?\b")
FONT_RE = re.compile(r"font-family\s*:\s*([^;}{]+)", re.IGNORECASE)


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta = {}
        self.styles = []
        self.links = []
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = {key.lower(): value for key, value in attrs if key and value}
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            name = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if name and content:
                self.meta[name.lower()] = content
        if tag == "style":
            self.styles.append("")
        if tag == "link":
            href = attrs_dict.get("href", "")
            rel = attrs_dict.get("rel", "")
            if "stylesheet" in rel and href:
                self.links.append(href)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif self.styles:
            self.styles[-1] += data


def _normalize_hex(value: str) -> str:
    value = value.lower()
    if len(value) == 4:
        return "#" + "".join(ch * 2 for ch in value[1:])
    return value


def _rgb(hex_color: str) -> tuple[int, int, int]:
    value = _normalize_hex(hex_color).lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def _luminance(hex_color: str) -> float:
    r, g, b = _rgb(hex_color)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255


def _saturation(hex_color: str) -> float:
    r, g, b = [channel / 255 for channel in _rgb(hex_color)]
    return max(r, g, b) - min(r, g, b)


def _safe_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _top_colors(text: str) -> list[str]:
    colors = [_normalize_hex(match) for match in HEX_COLOR_RE.findall(text)]
    ignored = {"#000000", "#ffffff", "#fff", "#000"}
    counts = Counter(color for color in colors if color not in ignored)
    return [color for color, _ in counts.most_common(12)]


def _top_fonts(text: str) -> list[str]:
    fonts = []
    for match in FONT_RE.findall(text):
        first = match.split(",")[0].strip().strip("\"'")
        if first and first.lower() not in {"inherit", "initial", "unset", "sans-serif", "serif"}:
            fonts.append(first)
    return [font for font, _ in Counter(fonts).most_common(6)]


def fetch_competitor_snapshot(url: str) -> dict:
    if not _safe_url(url):
        return {"url": url, "error": "Only http and https URLs are supported"}

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "OracleSiteCompetitorAnalyzer/0.1"},
            timeout=12,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"url": url, "error": str(exc)}

    html = response.text[:500000]
    parser = MetadataParser()
    parser.feed(html)
    style_text = "\n".join(parser.styles) + "\n" + html
    return {
        "url": url,
        "title": parser.title[:160],
        "description": parser.meta.get("description", "")[:320],
        "ogTitle": parser.meta.get("og:title", "")[:160],
        "colors": _top_colors(style_text),
        "fonts": _top_fonts(style_text),
        "signals": {
            "hasPricing": "pricing" in html.lower(),
            "hasBooking": any(term in html.lower() for term in ["book", "appointment", "schedule"]),
            "hasNewsletter": "newsletter" in html.lower(),
            "hasShop": any(term in html.lower() for term in ["shop", "cart", "checkout"]),
        },
    }


def _pick_palette(base: dict, colors: list[str]) -> dict:
    if not colors:
        return {}

    dark = [color for color in colors if _luminance(color) < 0.35]
    light = [color for color in colors if _luminance(color) > 0.82]
    saturated = sorted(colors, key=lambda color: _saturation(color), reverse=True)

    palette = {}
    if dark:
        palette["ink"] = dark[0]
    if light:
        palette["paper"] = light[0]
    if saturated:
        palette["primary"] = saturated[0]
    if len(saturated) > 1:
        palette["accent"] = saturated[1]
    if len(saturated) > 2:
        palette["link"] = saturated[2]
    if "primary" in palette and "line" not in palette:
        palette["line"] = base["tokens"]["colors"]["line"]
    return palette


def analyze_competitors(
    industry: str,
    competitor_urls: list[str],
    observations: Optional[list[dict]] = None,
    notes: str = "",
) -> dict:
    snapshots = [fetch_competitor_snapshot(url) for url in competitor_urls]
    observation_items = observations or []
    observed_colors = []
    observed_fonts = []

    for item in snapshots + observation_items:
        observed_colors.extend(item.get("colors", []) or [])
        observed_fonts.extend(item.get("fonts", []) or [])

    base = profile_for_industry(industry, competitor_urls)
    color_counts = [color for color, _ in Counter(observed_colors).most_common(12)]
    font_counts = [font for font, _ in Counter(observed_fonts).most_common(4)]

    token_override = {"colors": _pick_palette(base, color_counts)}
    if font_counts:
        token_override["typography"] = {
            "body": f"{font_counts[0]}, Arial, Helvetica, sans-serif",
            "heading": f"{font_counts[0]}, Arial, Helvetica, sans-serif",
        }

    has_shop = any((item.get("signals") or {}).get("hasShop") for item in snapshots)
    has_booking = any((item.get("signals") or {}).get("hasBooking") for item in snapshots)
    layout = {"density": "compact" if industry == "accounting" else "comfortable"}
    if has_shop:
        layout["heroMinHeight"] = "60vh"
    if has_booking:
        layout["cardPadding"] = "18px"
    token_override["layout"] = layout

    profile = deep_merge(base, {"tokens": token_override})
    profile["source"] = "competitor-analyzer"
    profile["competitorUrls"] = competitor_urls
    profile["notes"] = (
        notes
        or "Generated from public competitor HTML/CSS signals and optional OpenClaw visual observations. "
        "Use category conventions, but keep the final identity distinct."
    )
    profile["analysis"] = {
        "snapshots": snapshots,
        "observations": observation_items,
        "dominantColors": color_counts,
        "dominantFonts": font_counts,
    }
    return profile

