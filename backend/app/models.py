from datetime import datetime, timezone

from .extensions import db


def _pick(i18n: dict, locale, field, base):
    """Resolve a localized field: i18n[locale][field] if present & non-empty,
    else the base-column value (the default locale). locale=None → base."""
    if not locale:
        return base
    tr = (i18n or {}).get(locale) or {}
    val = tr.get(field)
    if val is None or val == "":
        return base
    return val


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
    # {"<locale>": {"title":..,"excerpt":..,"body_markdown":..,"tags":[..],"meta_title":..,"meta_description":..}}
    i18n = db.Column(db.JSON, nullable=False, default=dict)

    def to_card_dict(self, locale=None) -> dict:
        return {
            "id": self.id,
            "title": _pick(self.i18n, locale, "title", self.title),
            "slug": self.slug,
            "excerpt": _pick(self.i18n, locale, "excerpt", self.excerpt),
            "tags": _pick(self.i18n, locale, "tags", self.tags),
            "author": self.author,
            "publishedAt": self.published_at.isoformat() if self.published_at else None,
            "metaTitle": _pick(self.i18n, locale, "meta_title", self.meta_title),
            "metaDescription": _pick(self.i18n, locale, "meta_description", self.meta_description),
            "canonicalUrl": self.canonical_url,
            "geoRegion": self.geo_region,
            "locales": sorted((self.i18n or {}).keys()),
        }

    def to_detail_dict(self, locale=None) -> dict:
        item = self.to_card_dict(locale)
        item["bodyMarkdown"] = _pick(self.i18n, locale, "body_markdown", self.body_markdown)
        item["status"] = self.status
        return item


class Page(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    body_markdown = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="draft")
    nav_label = db.Column(db.String(255), nullable=False, default="")
    nav_order = db.Column(db.Integer, nullable=False, default=100)
    show_in_nav = db.Column(db.Boolean, nullable=False, default=True)
    sections = db.Column(db.JSON, nullable=False, default=list)
    meta_title = db.Column(db.String(255), nullable=False, default="")
    meta_description = db.Column(db.String(320), nullable=False, default="")
    canonical_url = db.Column(db.Text, nullable=False, default="")
    published_at = db.Column(db.DateTime, nullable=True)
    # {"<locale>": {"title":..,"nav_label":..,"body_markdown":..,"sections":[..],"meta_title":..,"meta_description":..}}
    i18n = db.Column(db.JSON, nullable=False, default=dict)

    def to_card_dict(self, locale=None) -> dict:
        title = _pick(self.i18n, locale, "title", self.title)
        return {
            "id": self.id,
            "title": title,
            "slug": self.slug,
            "navLabel": _pick(self.i18n, locale, "nav_label", self.nav_label) or title,
            "navOrder": self.nav_order,
            "showInNav": self.show_in_nav,
            "metaTitle": _pick(self.i18n, locale, "meta_title", self.meta_title),
            "metaDescription": _pick(self.i18n, locale, "meta_description", self.meta_description),
            "locales": sorted((self.i18n or {}).keys()),
        }

    def to_detail_dict(self, locale=None) -> dict:
        item = self.to_card_dict(locale)
        item["bodyMarkdown"] = _pick(self.i18n, locale, "body_markdown", self.body_markdown)
        item["status"] = self.status
        item["canonicalUrl"] = self.canonical_url
        item["publishedAt"] = self.published_at.isoformat() if self.published_at else None
        item["sections"] = _pick(self.i18n, locale, "sections", self.sections)
        return item


class NewsletterSubscription(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False, default="")
    status = db.Column(db.String(32), nullable=False, default="active")
    source = db.Column(db.String(255), nullable=False, default="website")


class DesignProfile(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(32), nullable=False, default="active", index=True)
    source = db.Column(db.String(255), nullable=False, default="default")
    industry = db.Column(db.String(255), nullable=False, default="")
    personality = db.Column(db.Text, nullable=False, default="")
    competitor_urls = db.Column(db.JSON, nullable=False, default=list)
    tokens = db.Column(db.JSON, nullable=False, default=dict)
    voice = db.Column(db.JSON, nullable=False, default=dict)
    notes = db.Column(db.Text, nullable=False, default="")
    sections = db.Column(db.JSON, nullable=False, default=list)
    # {"<locale>": {"sections": [..localized home blocks..]}}
    i18n = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self, locale=None) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "source": self.source,
            "industry": self.industry,
            "personality": self.personality,
            "competitorUrls": self.competitor_urls,
            "tokens": self.tokens,
            "voice": self.voice,
            "notes": self.notes,
            "sections": _pick(self.i18n, locale, "sections", self.sections),
            "availableLocales": sorted((self.i18n or {}).keys()),
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }


class UiMessages(TimestampMixin, db.Model):
    """UI chrome strings (nav/footer/buttons) per locale, so even the framework
    labels are not hard-coded — the agent can edit them with no redeploy. The
    frontend ships English defaults and overlays whatever this returns."""
    id = db.Column(db.Integer, primary_key=True)
    locale = db.Column(db.String(16), unique=True, nullable=False, index=True)
    messages = db.Column(db.JSON, nullable=False, default=dict)

    def to_dict(self) -> dict:
        return {"locale": self.locale, "messages": self.messages or {}}


class BlockPattern(TimestampMixin, db.Model):
    """A saved, reusable section spec — the 'capture' library. A pattern's `spec`
    is a full block ({type, variant, content}); inserting it scaffolds a new
    instance. Lets the block vocabulary grow from screenshots with no redeploy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    category = db.Column(db.String(64), nullable=False, default="captured")
    tags = db.Column(db.JSON, nullable=False, default=list)
    spec = db.Column(db.JSON, nullable=False, default=dict)
    source = db.Column(db.String(255), nullable=False, default="capture")
    notes = db.Column(db.Text, nullable=False, default="")

    def to_card_dict(self) -> dict:
        spec = self.spec or {}
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "category": self.category,
            "tags": self.tags,
            "type": spec.get("type"),
            "variant": spec.get("variant"),
            "source": self.source,
            "updatedAt": self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_detail_dict(self) -> dict:
        item = self.to_card_dict()
        item["spec"] = self.spec or {}
        item["notes"] = self.notes
        return item
