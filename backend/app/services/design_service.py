from copy import deepcopy
from typing import Optional


# Font faces are loaded once in the frontend layout and exposed as CSS vars.
# Templates choose a face through their typography tokens.
SANS = "var(--font-sans), system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
SERIF = "var(--font-display), Georgia, 'Times New Roman', serif"
GROTESK = "var(--font-grotesk), var(--font-sans), system-ui, sans-serif"
MONO = "var(--font-mono-stack, ui-monospace), SFMono-Regular, Menlo, Monaco, Consolas, monospace"


DEFAULT_STATS_SECTION = {
    "type": "stats",
    "content": {
        "items": [
            {"value": "Daily", "label": "Fresh content"},
            {"value": "1-click", "label": "Publish"},
            {"value": "100%", "label": "Yours to own"},
            {"value": "SEO", "label": "Built in"},
        ]
    },
}

DEFAULT_LOGOS_SECTION = {
    "type": "logos",
    "content": {
        "heading": "Built with",
        "items": [{"label": "Next.js"}, {"label": "Flask"}, {"label": "PostgreSQL"}, {"label": "Cloudflare"}],
    },
}

DEFAULT_SECTIONS = [
    {
        "type": "hero",
        "variant": "split",
        "content": {
            "kicker": "Your site, your rules",
            "headline": "A website you fully own.",
            "headlineAccent": "Publish daily. Grow steadily.",
            "subhead": "A modern site with a daily blog, newsletter, and clean pages — built to grow with you.",
            "cta": {"label": "Read the blog", "href": "/blog"},
            "secondaryCta": {"label": "Contact", "href": "/contact"},
        },
    },
    DEFAULT_STATS_SECTION,
    DEFAULT_LOGOS_SECTION,
    {
        "type": "problem",
        "variant": "cards",
        "content": {
            "heading": "Sound familiar?",
            "subhead": "The usual website setup gets in the way more than it helps.",
            "items": [
                {"icon": "layers", "title": "Scattered tools", "body": "Content, email, and your site live in three different places."},
                {"icon": "gauge", "title": "Slow to update", "body": "Every small change means waiting on someone else."},
                {"icon": "shield", "title": "Not really yours", "body": "Your audience and data sit on someone else's platform."},
            ],
        },
    },
    {
        "type": "features",
        "variant": "cards",
        "content": {
            "heading": "What we do",
            "items": [
                {"icon": "sparkles", "title": "Fresh content", "body": "A steady stream of useful, on-brand articles."},
                {"icon": "mail", "title": "Stay in touch", "body": "Grow an audience with a simple newsletter."},
                {"icon": "shield", "title": "Yours to own", "body": "Your domain, your data, your design."},
            ],
        },
    },
    {
        "type": "comparison",
        "content": {
            "heading": "Why this framework",
            "left": {"title": "The usual way", "items": ["Locked into a platform", "Pay per seat, forever", "Hard to customize", "Your data is theirs"]},
            "right": {"title": "Oracle Site", "items": ["Your own server + domain", "One-time setup, no rent", "Fully yours to restyle", "You own everything"]},
        },
    },
    {
        "type": "testimonials",
        "content": {
            "heading": "What people say",
            "items": [
                {"quote": "Set up our whole site in an afternoon — and it looks the part.", "author": "A. Founder", "role": "Small studio"},
                {"quote": "The daily posts keep coming without me lifting a finger.", "author": "M. Writer", "role": "Creator"},
                {"quote": "Finally a site I actually own end to end.", "author": "J. Owner", "role": "Local business"},
            ],
        },
    },
    {
        "type": "pricing",
        "content": {
            "heading": "Simple to run",
            "subhead": "Example tiers — make them your own.",
            "items": [
                {"name": "Starter", "price": "$0", "period": "/forever", "features": ["1 site", "Daily blog", "Newsletter"], "cta": {"label": "Get started", "href": "/contact"}},
                {"name": "Pro", "price": "$99", "period": "/one-time", "features": ["Custom design", "Unlimited pages", "Priority support"], "featured": True, "cta": {"label": "Choose Pro", "href": "/contact"}},
                {"name": "Agency", "price": "Custom", "period": "", "features": ["Multiple sites", "White-label", "Dedicated help"], "cta": {"label": "Contact us", "href": "/contact"}},
            ],
        },
    },
    {
        "type": "faq",
        "content": {
            "heading": "Questions",
            "items": [
                {"q": "Do I need to know how to code?", "a": "No — manage pages, blog, and design by chatting with your agent. Code is there if you want it."},
                {"q": "Is it really mine?", "a": "Yes. It runs on your server and domain; your content and audience are yours."},
                {"q": "Can I change the whole look?", "a": "Yes — switch a style preset or fine-tune colors, fonts, and sections anytime."},
            ],
        },
    },
    {
        "type": "cta",
        "variant": "banner",
        "content": {
            "headline": "Ready to get started?",
            "subhead": "Have a question or want to work together?",
            "cta": {"label": "Get in touch", "href": "/contact"},
        },
    },
]


DEFAULT_DESIGN_PROFILE = {
    "name": "Editorial Operator",
    "source": "default",
    "industry": "education",
    "personality": "clear, useful, trustworthy, modern",
    "competitorUrls": [],
    "tokens": {
        "colors": {
            "ink": "#18211f",
            "muted": "#66736f",
            "paper": "#faf8f3",
            "surface": "#ffffff",
            "line": "#e2e6dd",
            "primary": "#216e5f",
            "accent": "#b54945",
            "highlight": "#c79b3b",
            "link": "#356b9f",
        },
        "typography": {
            "body": SANS,
            "heading": SANS,
            "mono": MONO,
        },
        "radius": {
            "card": "16px",
            "control": "11px",
            "pill": "999px",
        },
        "layout": {
            "contentMaxWidth": "1120px",
            "heroMinHeight": "72vh",
            "density": "comfortable",
            "cardPadding": "24px",
            "sectionGap": "104px",
        },
    },
    "voice": {
        "headlineStyle": "plain offer or brand name",
        "tone": "practical and calm",
    },
    "notes": "Default profile. Replace this with an industry- and competitor-informed profile.",
    "sections": DEFAULT_SECTIONS,
}


INDUSTRY_PRESETS = {
    "education": {
        "name": "Focused Learning",
        "personality": "credible, encouraging, structured, aspirational",
        "tokens": {
            "colors": {
                "ink": "#14213d",
                "muted": "#627084",
                "paper": "#f7f8fb",
                "surface": "#ffffff",
                "line": "#dde3ee",
                "primary": "#22577a",
                "accent": "#c44536",
                "highlight": "#f3b23c",
                "link": "#2f6fbb",
            },
            "typography": {"body": SANS, "heading": SANS},
            "layout": {"density": "comfortable", "heroMinHeight": "70vh"},
        },
        "voice": {"tone": "clear, supportive, evidence-minded"},
    },
    "accounting": {
        "name": "Professional Ledger",
        "personality": "precise, steady, discreet, professional",
        "tokens": {
            "colors": {
                "ink": "#15201d",
                "muted": "#65706d",
                "paper": "#f6f7f4",
                "surface": "#ffffff",
                "line": "#dde2dc",
                "primary": "#1f5f4a",
                "accent": "#8f3f3b",
                "highlight": "#b88a2d",
                "link": "#275f91",
            },
            "typography": {"body": SANS, "heading": SANS},
            "layout": {"density": "compact", "heroMinHeight": "62vh"},
        },
        "voice": {"tone": "precise, plainspoken, risk-aware"},
    },
    "retail": {
        "name": "Local Retail Signal",
        "personality": "warm, direct, visual, conversion-minded",
        "tokens": {
            "colors": {
                "ink": "#221b17",
                "muted": "#766b64",
                "paper": "#fbf7f0",
                "surface": "#ffffff",
                "line": "#ece1d4",
                "primary": "#a6422b",
                "accent": "#28666e",
                "highlight": "#d79a2b",
                "link": "#2f6b8f",
            },
            "typography": {"body": SANS, "heading": SANS},
            "layout": {"density": "comfortable", "heroMinHeight": "66vh"},
        },
        "voice": {"tone": "friendly, concrete, product-aware"},
    },
}


def deep_merge(base: dict, override: dict) -> dict:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def profile_for_industry(industry: str, competitor_urls: Optional[list[str]] = None) -> dict:
    normalized = (industry or "education").strip().lower()
    preset = INDUSTRY_PRESETS.get(normalized, {})
    profile = deep_merge(DEFAULT_DESIGN_PROFILE, preset)
    profile["industry"] = normalized
    profile["source"] = "industry-preset"
    profile["competitorUrls"] = competitor_urls or []
    return profile


def normalized_profile(data: dict, industry: str = "education") -> dict:
    base = profile_for_industry(industry)
    profile = deep_merge(base, data or {})
    profile["tokens"] = deep_merge(base["tokens"], profile.get("tokens") or {})
    profile["voice"] = deep_merge(base["voice"], profile.get("voice") or {})
    if not isinstance(profile.get("competitorUrls"), list):
        profile["competitorUrls"] = []
    if not isinstance(profile.get("sections"), list) or not profile.get("sections"):
        profile["sections"] = base.get("sections") or DEFAULT_SECTIONS
    return profile


# =====================================================================
# Named style families — switchable templates. Each = a full palette
# (+ radius / layout / typography) and a section composition. The frontend
# derives light/dark mode from the palette and a [data-theme] hook from the
# preset key, so each template renders with its own depth and typographic
# character — not just a recolor. "Inspired-by" curated looks, never clones.
# =====================================================================
STYLE_PRESETS = {
    # Aurora — calm, spacious, premium. Apple / Linear / Stripe energy.
    "minimal": {
        "name": "Aurora — Minimal",
        "personality": "calm, spacious, premium, confident",
        "tokens": {
            "colors": {
                "ink": "#0b1220", "muted": "#5b6573", "paper": "#fbfcfe", "surface": "#ffffff",
                "line": "#e7e9f0", "primary": "#2563eb", "accent": "#6366f1", "highlight": "#f59e0b", "link": "#2563eb",
            },
            "typography": {"body": SANS, "heading": SANS},
            "radius": {"card": "20px", "control": "13px", "pill": "999px"},
            "layout": {"density": "spacious", "heroMinHeight": "88vh", "sectionGap": "128px", "contentMaxWidth": "1120px", "cardPadding": "28px"},
        },
        "voice": {"headlineStyle": "short, bold, benefit-led", "tone": "calm and premium"},
        "sections": [
            {"type": "hero", "variant": "centered", "content": {
                "badge": "Premium by default",
                "headline": "Clean, fast,", "headlineAccent": "made to last.",
                "subhead": "A refined site that loads fast, reads beautifully, and stays out of the way — so your work is the thing people notice.",
                "cta": {"label": "Get started", "href": "/contact"}, "secondaryCta": {"label": "Read the blog", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "100", "label": "Lighthouse-ready"}, {"value": "Daily", "label": "Fresh writing"},
                {"value": "SEO", "label": "Built in"}, {"value": "0", "label": "Platform lock-in"}]}},
            DEFAULT_LOGOS_SECTION,
            {"type": "features", "variant": "minimal", "content": {"heading": "Everything needed, nothing extra.", "subhead": "A calmer stack for publishing and keeping your audience close.", "items": [
                {"icon": "gauge", "title": "Fast", "body": "Built for speed and clarity on every device."},
                {"icon": "layers", "title": "Refined", "body": "Considered type, spacing, and color — no clutter."},
                {"icon": "shield", "title": "Yours", "body": "Your domain, your data, your brand."}]}},
            {"type": "comparison", "content": {"heading": "Simple beats scattered.",
                "left": {"title": "Before", "items": ["Separate site and newsletter tools", "Monthly platform rent", "Hard-to-edit templates", "Data spread across services"]},
                "right": {"title": "This site", "items": ["One clean publishing workflow", "Runs on your own stack", "Design updates instantly", "Content stays portable"]}}},
            {"type": "faq", "content": {"heading": "Questions", "items": [
                {"q": "Do I need to code?", "a": "No — manage pages, posts, and design by chatting with your agent."},
                {"q": "Can I change the whole look?", "a": "Yes — switch a template or fine-tune colors, fonts, and sections anytime."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Start today.", "subhead": "Spin up a clean site and grow from there.", "cta": {"label": "Get started", "href": "/contact"}}},
        ],
    },
    # Eclipse — dramatic dark, high-contrast, modern. Tesla / Vercel energy.
    "bold-dark": {
        "name": "Eclipse — Bold Dark",
        "personality": "dramatic, high-contrast, confident, modern",
        "tokens": {
            "colors": {
                "ink": "#f4f6fb", "muted": "#9aa6bd", "paper": "#0b0d14", "surface": "#14171f",
                "line": "#272c3a", "primary": "#7c5cff", "accent": "#ff5d8f", "highlight": "#f2c14e", "link": "#a899ff",
            },
            "typography": {"body": SANS, "heading": GROTESK},
            "radius": {"card": "16px", "control": "11px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "94vh", "sectionGap": "118px", "contentMaxWidth": "1140px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "bold, declarative", "tone": "confident and bold"},
        "sections": [
            {"type": "hero", "variant": "fullbleed", "content": {
                "badge": "Bold by design",
                "headline": "Power. Presence.", "headlineAccent": "Performance.",
                "subhead": "A dramatic, high-contrast presence that commands attention the moment it loads.",
                "cta": {"label": "Explore", "href": "/blog"}, "secondaryCta": {"label": "Contact", "href": "/contact"}}},
            {"type": "stats", "content": {"items": [
                {"value": "60fps", "label": "Smooth by default"}, {"value": "Dark", "label": "Native mode"},
                {"value": "AA", "label": "Contrast-checked"}, {"value": "1", "label": "Site you own"}]}},
            DEFAULT_LOGOS_SECTION,
            {"type": "features", "variant": "minimal", "content": {"heading": "Built different.", "subhead": "High contrast, high clarity, hard to ignore.", "items": [
                {"icon": "zap", "title": "Bold", "body": "Deep canvas, electric accents, real hierarchy."},
                {"icon": "gauge", "title": "Fast", "body": "Performance you can feel on first paint."},
                {"icon": "sparkles", "title": "Modern", "body": "A look that feels current, not templated."}]}},
            {"type": "comparison", "content": {"heading": "Stand out, on purpose.",
                "left": {"title": "Generic theme", "items": ["Looks like everyone else", "Flat, low contrast", "Light-only", "Slow, heavy assets"]},
                "right": {"title": "Eclipse", "items": ["A presence of its own", "Dramatic depth & glow", "Dark-native design", "Fast, considered build"]}}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Experience it.", "subhead": "See the difference a real design makes.", "cta": {"label": "Get in touch", "href": "/contact"}}},
        ],
    },
    # Atelier — warm, editorial, content-first. Serif display + drop-cap long-form.
    "editorial": {
        "name": "Atelier — Editorial",
        "personality": "warm, literary, considered, trustworthy",
        "tokens": {
            "colors": {
                "ink": "#241d18", "muted": "#6f655c", "paper": "#f7f2ea", "surface": "#fffdf9",
                "line": "#e7dccc", "primary": "#a14d2a", "accent": "#3f6f63", "highlight": "#bb8a36", "link": "#9c4a22",
            },
            "typography": {"body": SANS, "heading": SERIF},
            "radius": {"card": "12px", "control": "9px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "72vh", "sectionGap": "108px", "contentMaxWidth": "1080px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "editorial, human, specific", "tone": "warm and considered"},
        "sections": [
            {"type": "hero", "variant": "split", "content": {
                "kicker": "Words that carry",
                "headline": "Writing worth", "headlineAccent": "returning to.",
                "subhead": "A warm, editorial home for essays, notes, and a newsletter — designed to be read, not just scrolled past.",
                "cta": {"label": "Read the blog", "href": "/blog"}, "secondaryCta": {"label": "Say hello", "href": "/contact"}}},
            {"type": "stats", "content": {"items": [
                {"value": "Daily", "label": "New writing"}, {"value": "1", "label": "Calm home"},
                {"value": "0", "label": "Ads or trackers"}, {"value": "100%", "label": "Yours"}]}},
            {"type": "problem", "variant": "cards", "content": {"heading": "Most sites fight the reader.", "subhead": "Cramped measures, restless layouts, borrowed identities.", "items": [
                {"icon": "layers", "title": "Cluttered", "body": "Ten things shouting before the first sentence lands."},
                {"icon": "gauge", "title": "Restless", "body": "Pop-ups and motion that pull attention away."},
                {"icon": "book", "title": "Forgettable", "body": "Nothing that feels like a place of its own."}]}},
            {"type": "features", "variant": "cards", "content": {"heading": "Made for reading.", "items": [
                {"icon": "book", "title": "Real typography", "body": "A serif display and a generous measure, set with care."},
                {"icon": "mail", "title": "A quiet newsletter", "body": "Let readers follow without another platform."},
                {"icon": "shield", "title": "A place of your own", "body": "Your words, your domain, your design."}]}},
            {"type": "testimonials", "content": {"heading": "Readers notice.", "items": [
                {"quote": "It finally reads like a magazine, not a dashboard.", "author": "R. Ellison", "role": "Essayist"},
                {"quote": "People actually finish the posts now.", "author": "D. Marsh", "role": "Newsletter writer"},
                {"quote": "It feels like mine — not a template.", "author": "P. Quan", "role": "Studio owner"}]}},
            {"type": "faq", "content": {"heading": "Good to know", "items": [
                {"q": "Can I write in Markdown?", "a": "Yes — posts and pages are Markdown, rendered into this editorial type system."},
                {"q": "Is the look fixed?", "a": "No — switch templates or fine-tune type, color, and sections whenever you like."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Start writing.", "subhead": "A calm, beautiful home for your words.", "cta": {"label": "Get in touch", "href": "/contact"}}},
        ],
    },
    # Meridian — structured, trustworthy, B2B. Denser navy/teal corporate look.
    "corporate": {
        "name": "Meridian — Professional",
        "personality": "trustworthy, structured, credible, precise",
        "tokens": {
            "colors": {
                "ink": "#101828", "muted": "#586172", "paper": "#f4f7fb", "surface": "#ffffff",
                "line": "#dce3ef", "primary": "#1c4e8a", "accent": "#0f766e", "highlight": "#b7791f", "link": "#1c5fb0",
            },
            "typography": {"body": SANS, "heading": SANS},
            "radius": {"card": "12px", "control": "9px", "pill": "999px"},
            "layout": {"density": "compact", "heroMinHeight": "70vh", "sectionGap": "100px", "contentMaxWidth": "1180px", "cardPadding": "24px"},
        },
        "voice": {"headlineStyle": "clear, credible, outcome-led", "tone": "professional and precise"},
        "sections": [
            {"type": "hero", "variant": "split", "content": {
                "kicker": "Built for serious work",
                "headline": "A credible home for", "headlineAccent": "your business.",
                "subhead": "Clear structure, trustworthy design, and the pages your customers expect — set up once, fully owned.",
                "cta": {"label": "Book a call", "href": "/contact"}, "secondaryCta": {"label": "See the blog", "href": "/blog"}}},
            {"type": "logos", "content": {"heading": "A dependable stack", "items": [{"label": "Next.js"}, {"label": "Flask"}, {"label": "PostgreSQL"}, {"label": "Cloudflare"}]}},
            {"type": "stats", "content": {"items": [
                {"value": "99.9%", "label": "Uptime-ready"}, {"value": "<1s", "label": "Typical load"},
                {"value": "SEO", "label": "Built in"}, {"value": "24/7", "label": "Always on"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "What you get", "subhead": "The essentials, done properly.", "items": [
                {"icon": "shield", "title": "Trust by design", "body": "Clean structure and accessible contrast throughout."},
                {"icon": "gauge", "title": "Fast & reliable", "body": "Lightweight pages that load quickly, everywhere."},
                {"icon": "layers", "title": "Easy to extend", "body": "Add pages, services, and posts as you grow."}]}},
            {"type": "comparison", "content": {"heading": "Why teams choose this",
                "left": {"title": "Page builders", "items": ["Monthly per-seat pricing", "Heavy, slow pages", "Generic look", "Locked-in content"]},
                "right": {"title": "Meridian", "items": ["One-time setup", "Fast, lean delivery", "A credible identity", "Portable, owned data"]}}},
            {"type": "testimonials", "content": {"heading": "Trusted by operators", "items": [
                {"quote": "It looks like a company we'd hire.", "author": "S. Patel", "role": "Founder, consultancy"},
                {"quote": "Set up once, runs itself since.", "author": "K. Brooks", "role": "Ops lead"},
                {"quote": "Fast, clean, and clearly ours.", "author": "L. Romano", "role": "Managing director"}]}},
            {"type": "pricing", "content": {"heading": "Straightforward pricing", "subhead": "Example tiers — adapt to your offer.",
                "items": [
                    {"name": "Starter", "price": "$0", "period": "/forever", "features": ["1 site", "Blog + newsletter", "Core pages"], "cta": {"label": "Get started", "href": "/contact"}},
                    {"name": "Business", "price": "$99", "period": "/one-time", "features": ["Custom design", "Unlimited pages", "Priority support"], "featured": True, "cta": {"label": "Choose Business", "href": "/contact"}},
                    {"name": "Enterprise", "price": "Custom", "period": "", "features": ["Multiple sites", "White-label", "Dedicated help"], "cta": {"label": "Contact sales", "href": "/contact"}}]}},
            {"type": "faq", "content": {"heading": "Common questions", "items": [
                {"q": "Can we use our own domain?", "a": "Yes — it runs on your domain and server, behind Cloudflare."},
                {"q": "Can you match our brand?", "a": "Yes — colors, fonts, and sections are all adjustable."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Ready to look the part?", "subhead": "Set up a credible site you fully own.", "cta": {"label": "Book a call", "href": "/contact"}}},
        ],
    },
}


def apply_style(name: str) -> dict:
    """Return a full design-profile dict for a named style preset (empty dict if unknown)."""
    preset = STYLE_PRESETS.get((name or "").strip().lower())
    if not preset:
        return {}
    overrides = {k: v for k, v in preset.items() if k != "name"}
    profile = deep_merge(DEFAULT_DESIGN_PROFILE, overrides)
    profile["name"] = preset.get("name", profile.get("name"))
    profile["source"] = f"style-preset:{(name or '').strip().lower()}"
    profile["tokens"] = deep_merge(DEFAULT_DESIGN_PROFILE["tokens"], preset.get("tokens") or {})
    profile["sections"] = preset.get("sections") or DEFAULT_SECTIONS
    return profile
