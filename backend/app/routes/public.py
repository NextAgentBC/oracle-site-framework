from datetime import datetime, timezone

import json
from importlib.resources import files

import os

from flask import Blueprint, current_app, jsonify, request, send_from_directory
from sqlalchemy import text

from ..auth import issue_jwt, upsert_google_user, verify_google_token
from ..extensions import db
from ..models import BlockPattern, BlogPost, DesignProfile, NewsletterSubscription, Page, UiMessages
from ..services.design_service import DEFAULT_DESIGN_PROFILE, normalized_profile
from ..services import block_service
from ..services.email_service import send_email

bp = Blueprint("public", __name__)


def request_locale():
    """The validated ?locale= query arg, or None for the default locale (which
    means 'use base columns'). Keeps content selection in one place."""
    loc = (request.args.get("locale") or "").strip().lower()
    if not loc or loc == current_app.config["SITE_DEFAULT_LOCALE"]:
        return None
    if loc not in current_app.config["SITE_LOCALES"]:
        return None
    return loc


@bp.get("/health")
def health():
    db.session.execute(text("select 1"))
    return {"status": "ok", "database": "ok"}


@bp.get("/media/<path:filename>")
def media(filename: str):
    """Serve self-hosted media (blog images, etc.) from MEDIA_DIR — a persistent
    volume so the site owns its images instead of hot-linking an external CDN.
    send_from_directory guards against path traversal."""
    media_dir = current_app.config["MEDIA_DIR"]
    os.makedirs(media_dir, exist_ok=True)
    return send_from_directory(media_dir, filename, max_age=86400)


@bp.get("/site")
def site():
    return {
        "item": {
            "name": current_app.config["SITE_NAME"],
            "url": current_app.config["SITE_URL"],
            "industry": current_app.config["SITE_INDUSTRY"],
            "audience": current_app.config["SITE_AUDIENCE"],
            "region": current_app.config["SITE_REGION"],
            "googleClientId": current_app.config["GOOGLE_CLIENT_ID"],
            "locales": current_app.config["SITE_LOCALES"],
            "defaultLocale": current_app.config["SITE_DEFAULT_LOCALE"],
        }
    }


@bp.get("/design")
def design():
    locale = request_locale()
    profile = DesignProfile.query.filter_by(status="active").order_by(DesignProfile.updated_at.desc()).first()
    if not profile:
        return {"item": DEFAULT_DESIGN_PROFILE}
    return {"item": normalized_profile(profile.to_dict(locale), profile.industry or current_app.config["SITE_INDUSTRY"])}


@bp.get("/i18n/<locale>")
def ui_messages(locale: str):
    """UI chrome strings for a locale (nav/footer/buttons). The frontend ships
    English defaults and overlays whatever is returned here — so even framework
    labels are editable by the agent, no redeploy."""
    locale = (locale or "").strip().lower()
    row = UiMessages.query.filter_by(locale=locale).first()
    return {"item": {"locale": locale, "messages": row.messages if row else {}}}


@bp.get("/patterns")
def patterns():
    """Public catalog of saved section patterns — the growing 'capture' library."""
    items = BlockPattern.query.order_by(BlockPattern.updated_at.desc()).all()
    return {"items": [p.to_card_dict() for p in items], "meta": {"count": len(items)}}


@bp.get("/patterns/<slug>")
def pattern_detail(slug: str):
    pattern = BlockPattern.query.filter_by(slug=slug).first_or_404()
    return {"item": pattern.to_detail_dict()}


@bp.get("/blocks")
def blocks_catalog():
    """Public block catalog — the typed-block library a page can be composed from.
    Lets an agent (or a future visual editor) discover types, variants, fields,
    defaults, and the icon vocabulary, then validate before composing."""
    items = block_service.manifest()
    return {"items": items, "icons": block_service.ICONS, "meta": {"count": len(items)}}


@bp.get("/page-templates")
def page_templates_catalog():
    """Page recipes — the block library organized by page (home/about/services/...).
    Each is a recommended composition; scaffold one with POST /admin/pages {template:"<name>"}."""
    items = block_service.list_page_templates()
    return {"items": items, "meta": {"count": len(items)}}


@bp.get("/openapi.json")
def openapi():
    spec = files("app").joinpath("openapi.json").read_text(encoding="utf-8")
    return jsonify(json.loads(spec))


@bp.post("/auth/google")
def google_auth():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential", "")
    if not credential:
        return jsonify({"error": {"code": "bad_request", "message": "Missing Google credential"}}), 400
    try:
        payload = verify_google_token(credential)
        user = upsert_google_user(payload)
    except ValueError as exc:
        return jsonify({"error": {"code": "bad_request", "message": str(exc)}}), 400
    return {"item": {"user": user.to_public_dict(), "token": issue_jwt(user)}}


@bp.get("/blogs")
def blogs():
    locale = request_locale()
    posts = (
        BlogPost.query.filter_by(status="published")
        .order_by(BlogPost.published_at.desc().nullslast(), BlogPost.created_at.desc())
        .all()
    )
    return {"items": [post.to_card_dict(locale) for post in posts], "meta": {"count": len(posts)}}


@bp.get("/blogs/<slug>")
def blog_detail(slug: str):
    locale = request_locale()
    post = BlogPost.query.filter_by(slug=slug, status="published").first_or_404()
    return {"item": post.to_detail_dict(locale)}


@bp.get("/pages")
def pages():
    locale = request_locale()
    items = (
        Page.query.filter_by(status="published")
        .order_by(Page.nav_order.asc(), Page.title.asc())
        .all()
    )
    return {"items": [page.to_card_dict(locale) for page in items], "meta": {"count": len(items)}}


@bp.get("/pages/<slug>")
def page_detail(slug: str):
    locale = request_locale()
    page = Page.query.filter_by(slug=slug, status="published").first_or_404()
    return {"item": page.to_detail_dict(locale)}


@bp.post("/newsletter/subscribe")
def subscribe():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip().lower()
    name = data.get("name", "").strip()
    if "@" not in email:
        return jsonify({"error": {"code": "bad_request", "message": "Valid email is required"}}), 400
    subscription = NewsletterSubscription.query.filter_by(email=email).first()
    if not subscription:
        subscription = NewsletterSubscription(email=email, name=name)
        db.session.add(subscription)
    else:
        subscription.name = name or subscription.name
        subscription.status = "active"
    db.session.commit()
    send_email(
        email,
        f"Welcome to {current_app.config['SITE_NAME']}",
        "Thanks for subscribing. You will receive practical updates and daily essays from the site.",
    )
    return {"item": {"email": subscription.email, "status": subscription.status}}


@bp.post("/contact")
def contact():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    if not email or not message:
        return jsonify({"error": {"code": "bad_request", "message": "Email and message are required"}}), 400
    admin = next(iter(current_app.config["ADMIN_EMAILS"]), current_app.config["EMAIL_FROM"])
    if admin:
        send_email(admin, "New website contact message", f"From: {email}\n\n{message}")
    return {"item": {"receivedAt": datetime.now(timezone.utc).isoformat()}}
