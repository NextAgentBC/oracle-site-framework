from datetime import datetime, timezone

from .extensions import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class User(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, default="")
    picture = db.Column(db.Text, nullable=False, default="")
    google_sub = db.Column(db.String(255), unique=True, nullable=False, index=True)
    role = db.Column(db.String(32), nullable=False, default="user")

    def to_public_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
            "role": self.role,
        }


class BlogPost(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    excerpt = db.Column(db.Text, nullable=False, default="")
    body_markdown = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="draft")
    author = db.Column(db.String(255), nullable=False, default="Editorial")
    tags = db.Column(db.JSON, nullable=False, default=list)
    meta_title = db.Column(db.String(255), nullable=False, default="")
    meta_description = db.Column(db.String(320), nullable=False, default="")
    canonical_url = db.Column(db.Text, nullable=False, default="")
    geo_region = db.Column(db.String(255), nullable=False, default="")
    published_at = db.Column(db.DateTime, nullable=True)

    def to_card_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "excerpt": self.excerpt,
            "tags": self.tags,
            "author": self.author,
            "publishedAt": self.published_at.isoformat() if self.published_at else None,
            "metaTitle": self.meta_title,
            "metaDescription": self.meta_description,
            "canonicalUrl": self.canonical_url,
            "geoRegion": self.geo_region,
        }

    def to_detail_dict(self) -> dict:
        item = self.to_card_dict()
        item["bodyMarkdown"] = self.body_markdown
        item["status"] = self.status
        return item


class NewsletterSubscription(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, default="")
    status = db.Column(db.String(32), nullable=False, default="active")
    source = db.Column(db.String(255), nullable=False, default="website")

