from datetime import datetime, timezone
from typing import Optional

import click
from flask import current_app

from .extensions import db
from .models import BlogPost
from .routes.admin import _create_post
from .services.ai_service import generate_blog_post

@click.group("blog")
def blog_cli():
    """Blog operations."""


@blog_cli.command("generate-daily")
@click.option("--topic", default=None)
@click.option("--draft", is_flag=True)
def generate_daily(topic: Optional[str], draft: bool):
    generated = generate_blog_post(topic)
    publish = current_app.config["DAILY_BLOG_AUTOPUBLISH"] and not draft
    post = _create_post(generated, publish=publish)
    if not publish:
        post.status = "draft"
        post.published_at = None
        db.session.commit()
    click.echo(f"{post.status}: {post.title} ({post.slug}) at {datetime.now(timezone.utc).isoformat()}")
