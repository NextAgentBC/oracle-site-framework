"""Whole-site industry preview, powered by pre-built, translated demo packs
(backend/app/data/demo_packs.json — generated offline; no LLM at runtime).

A preview is per-visitor and read-only: it returns a complete industry site —
home (localized), nav pages, page bodies, and brand/industry/audience — so the
WHOLE site renders coherently as the chosen industry in the visitor's language,
without ever touching the real site's data.
"""
from __future__ import annotations

import copy
import json
import os
from functools import lru_cache
from typing import Optional

from .design_service import profile_for_industry, normalized_profile

_PACKS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "demo_packs.json")


@lru_cache(maxsize=1)
def _packs() -> dict:
    try:
        with open(_PACKS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def pack(industry: str) -> Optional[dict]:
    return _packs().get((industry or "").strip().lower())


def _loc(locale: Optional[str]) -> str:
    return "zh" if (locale or "").strip().lower().startswith("zh") else "en"


def preview_design(industry: str, locale: Optional[str] = None) -> dict:
    """The home design for an industry preview — the rich template (photos + wide
    layout), with localized copy + brand swapped in from the pack when available."""
    industry = (industry or "").strip().lower()
    prof = profile_for_industry(industry)
    p = pack(industry)
    if p:
        loc = _loc(locale)
        if loc == "zh" and (p.get("home") or {}).get("zh"):
            prof["sections"] = copy.deepcopy(p["home"]["zh"])
        brand = (p.get("brand") or {}).get(loc)
        if brand:
            prof["name"] = brand
    return normalized_profile(prof, prof.get("industry") or industry)


def preview_site(industry: str, locale: Optional[str] = None) -> dict:
    """Site identity for the preview — brand / industry / audience in the visitor's
    locale, so the nav brand + footer + meta all read as the previewed industry."""
    industry = (industry or "").strip().lower()
    p = pack(industry) or {}
    loc = _loc(locale)
    brand = (p.get("brand") or {}).get(loc) or profile_for_industry(industry).get("name", industry)
    return {"name": brand, "industry": industry, "audience": (p.get("audience") or {}).get(loc, "")}


def preview_pages(industry: str, locale: Optional[str] = None) -> list:
    """Nav pages for the preview (replaces the real site's pages so nothing leaks)."""
    p = pack(industry) or {}
    loc = _loc(locale)
    out = []
    for i, pg in enumerate(p.get("pages") or []):
        out.append({
            "slug": pg["slug"],
            "navLabel": (pg.get("navLabel") or {}).get(loc) or pg["slug"],
            "navOrder": (i + 1) * 10,
            "showInNav": True,
        })
    return out


def preview_page(industry: str, slug: str, locale: Optional[str] = None) -> Optional[dict]:
    """One preview page's content (localized Markdown body)."""
    p = pack(industry) or {}
    loc = _loc(locale)
    for pg in p.get("pages") or []:
        if pg.get("slug") == slug:
            label = (pg.get("navLabel") or {}).get(loc) or slug
            return {
                "slug": slug, "title": label, "navLabel": label,
                "bodyMarkdown": (pg.get("body") or {}).get(loc, ""),
                "sections": [], "metaTitle": label, "metaDescription": "",
            }
    return None
