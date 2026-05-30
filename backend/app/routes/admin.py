from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request
from slugify import slugify

from ..auth import require_auth
from ..extensions import db
from ..models import BlogPost
from ..services.ai_service import generate_blog_post

bp = Blueprint("admin", __name__)


def _unique_slug(slug: str) -> str:
    base = slugify(slug) or "post"
    candidate = base
    index = 2
    while BlogPost.query.filter_by(slug=candidate).first():
        candidate = f"{base}-{index}"
        index += 1
    return candidate


def _create_post(data: dict, publish: bool) -> BlogPost:
    status = "published" if publish else data.get("status", "draft")
    post = BlogPost(
        title=data["title"],
        slug=_unique_slug(data.get("slug") or data["title"]),
        excerpt=data.get("excerpt", ""),
        body_markdown=data["body_markdown"],
        status=status,
        tags=data.get("tags", []),
        meta_title=data.get("meta_title", data["title"][:60]),
        meta_description=data.get("meta_description", data.get("excerpt", ""))[:320],
        geo_region=data.get("geo_region", current_app.config["SITE_REGION"]),
        published_at=datetime.now(timezone.utc) if status == "published" else None,
    )
    post.canonical_url = f"{current_app.config['SITE_URL']}/blog/{post.slug}"
    db.session.add(post)
    db.session.commit()
    return post


@bp.post("/blogs/generate")
@require_auth(admin=True)
def generate_blog():
    data = request.get_json(silent=True) or {}
    generated = generate_blog_post(data.get("topic"))
    post = _create_post(generated, publish=bool(data.get("publish", False)))
    return {"item": post.to_detail_dict()}


@bp.post("/blogs")
@require_auth(admin=True)
def create_blog():
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("body_markdown"):
        return jsonify({"error": {"code": "bad_request", "message": "title and body_markdown are required"}}), 400
    post = _create_post(data, publish=data.get("status") == "published")
    return {"item": post.to_detail_dict()}, 201


@bp.patch("/blogs/<int:post_id>")
@require_auth(admin=True)
def update_blog(post_id: int):
    post = db.session.get(BlogPost, post_id)
    if not post:
        return jsonify({"error": {"code": "not_found", "message": "Blog post not found"}}), 404
    data = request.get_json(silent=True) or {}
    for key in ["title", "excerpt", "body_markdown", "status", "tags", "meta_title", "meta_description", "geo_region"]:
        if key in data:
            setattr(post, key, data[key])
    if data.get("status") == "published" and not post.published_at:
        post.published_at = datetime.now(timezone.utc)
    db.session.commit()
    return {"item": post.to_detail_dict()}

