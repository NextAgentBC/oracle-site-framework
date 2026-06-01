from copy import deepcopy
from typing import Optional


# Font faces are loaded once in the frontend layout and exposed as CSS vars.
# Templates choose a face through their typography tokens.
SANS = "var(--font-sans), system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
SERIF = "var(--font-display), Georgia, 'Times New Roman', serif"
GROTESK = "var(--font-grotesk), var(--font-sans), system-ui, sans-serif"
# Warm characterful serif (restaurant / beauty / editorial) and a tall athletic
# condensed (fitness / sport). Loaded once in the frontend layout.
FRAUNCES = "var(--font-fraunces), var(--font-display), Georgia, 'Times New Roman', serif"
CONDENSED = "var(--font-condensed), 'Oswald', 'Arial Narrow', var(--font-sans), system-ui, sans-serif"
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
            # Inverse surface = the deep "contrast band" behind a fullbleed hero
            # and the CTA banner. Tokenized so a template/agent can recolor it
            # instead of it being hard-coded dark in the stylesheet.
            "surfaceInverse": "#0b0f1a",
            "inkInverse": "#f6f9ff",
            # Text/icon color that sits on a primary-filled surface (buttons,
            # checkmarks). Lets light-primary palettes flip to dark on-color.
            "onPrimary": "#ffffff",
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
    "nonprofit": {
        "name": "Community Cause",
        "personality": "warm, hopeful, community-minded, sincere",
        "tokens": {
            "colors": {
                "ink": "#1e2a22", "muted": "#5f6f63", "paper": "#f4f7f1", "surface": "#ffffff",
                "line": "#dde6d8", "primary": "#2f7d4f", "accent": "#d98b3b", "highlight": "#e0b13c", "link": "#2f6f8f",
            },
            "typography": {"body": SANS, "heading": SANS},
            "layout": {"density": "comfortable", "heroMinHeight": "70vh"},
        },
        "voice": {"tone": "warm, hopeful, action-oriented"},
    },
    "hospitality": {
        "name": "Open Door Hospitality",
        "personality": "inviting, relaxed, refined, generous",
        "tokens": {
            "colors": {
                "ink": "#14222b", "muted": "#5b6b73", "paper": "#f3f7f8", "surface": "#ffffff",
                "line": "#d9e6e8", "primary": "#1f7a8c", "accent": "#c98a3e", "highlight": "#e0b15a", "link": "#2f7f9a",
            },
            "typography": {"body": SANS, "heading": SERIF},
            "layout": {"density": "comfortable", "heroMinHeight": "78vh"},
        },
        "voice": {"tone": "inviting, relaxed, gracious"},
    },
    "construction": {
        "name": "Solid Ground Trades",
        "personality": "dependable, straightforward, hardworking, sturdy",
        "tokens": {
            "colors": {
                "ink": "#1d1b16", "muted": "#6f685c", "paper": "#f6f4ef", "surface": "#ffffff",
                "line": "#e4dccd", "primary": "#b5631e", "accent": "#2f4858", "highlight": "#e0a93c", "link": "#2f5f7a",
            },
            "typography": {"body": SANS, "heading": GROTESK},
            "layout": {"density": "compact", "heroMinHeight": "68vh"},
        },
        "voice": {"tone": "dependable, plainspoken, results-first"},
    },
}


# Industry name (and common synonyms) → a full style template key. Lets
# profile_for_industry("dental clinic" → "healthcare") return a complete,
# section-filled template instead of just a recolor. Industries NOT listed here
# (education / accounting / retail / nonprofit / …) keep their token-only preset.
INDUSTRY_STYLE_ALIASES = {
    "tech": "tech", "saas": "tech", "software": "tech", "technology": "tech", "startup": "tech", "ai": "tech",
    "healthcare": "healthcare", "health": "healthcare", "medical": "healthcare", "clinic": "healthcare",
    "dental": "healthcare", "dentist": "healthcare", "wellness": "healthcare", "therapy": "healthcare",
    "restaurant": "restaurant", "food": "restaurant", "cafe": "restaurant", "coffee": "restaurant",
    "bakery": "restaurant", "catering": "restaurant", "bar": "restaurant",
    "realestate": "realestate", "real-estate": "realestate", "real estate": "realestate",
    "property": "realestate", "realty": "realestate", "architecture": "realestate", "interior": "realestate",
    "fitness": "fitness", "gym": "fitness", "sport": "fitness", "sports": "fitness", "trainer": "fitness", "yoga": "fitness",
    "beauty": "beauty", "salon": "beauty", "spa": "beauty", "cosmetics": "beauty", "skincare": "beauty", "hair": "beauty",
    "legal": "legal", "law": "legal", "lawyer": "legal", "attorney": "legal", "advisory": "legal", "consulting": "legal",
    "creative": "creative", "agency": "creative", "studio": "creative", "design": "creative",
    "portfolio": "creative", "marketing": "creative", "photography": "creative",
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
    # If the industry maps to a full style template, use it as the base so the
    # site gets a complete, section-filled design — not just a recolor.
    style_key = INDUSTRY_STYLE_ALIASES.get(normalized)
    if style_key:
        styled = apply_style(style_key)
        if styled:
            styled["industry"] = normalized
            styled["source"] = "industry-preset"
            styled["competitorUrls"] = competitor_urls or []
            return styled
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
    # Nimbus — modern SaaS / tech. Indigo + cyan, geometric grotesk, product-forward.
    "tech": {
        "name": "Nimbus — Tech / SaaS",
        "personality": "modern, precise, product-forward, confident",
        "tokens": {
            "colors": {
                "ink": "#0d1424", "muted": "#5a6478", "paper": "#f7f9fc", "surface": "#ffffff",
                "line": "#e6eaf2", "primary": "#4f46e5", "accent": "#06b6d4", "highlight": "#f59e0b", "link": "#4f46e5",
                "surfaceInverse": "#0b1020", "inkInverse": "#eef2ff", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": GROTESK},
            "radius": {"card": "18px", "control": "12px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "88vh", "sectionGap": "120px", "contentMaxWidth": "1140px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "crisp, benefit-led, product-forward", "tone": "confident and modern"},
        "sections": [
            {"type": "hero", "variant": "centered", "content": {
                "badge": "Ship faster",
                "headline": "The platform your", "headlineAccent": "team will love.",
                "subhead": "Launch, measure, and iterate from one clean workspace — no glue code, no busywork.",
                "cta": {"label": "Start free", "href": "/contact"}, "secondaryCta": {"label": "See how it works", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "10x", "label": "Faster setup"}, {"value": "99.9%", "label": "Uptime"},
                {"value": "<200ms", "label": "API latency"}, {"value": "SOC 2", "label": "Ready"}]}},
            {"type": "logos", "content": {"heading": "Integrates with your stack", "items": [{"label": "Slack"}, {"label": "GitHub"}, {"label": "Stripe"}, {"label": "Zapier"}, {"label": "Notion"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "Everything you need to scale.", "subhead": "Built for teams that move fast and break nothing.", "items": [
                {"icon": "zap", "title": "Fast by default", "body": "Sub-second loads and a snappy API your users feel."},
                {"icon": "shield", "title": "Secure & compliant", "body": "Encryption, audit logs, and SSO out of the box."},
                {"icon": "gauge", "title": "Observable", "body": "Dashboards and alerts so nothing slips by."}]}},
            {"type": "comparison", "content": {"heading": "Why teams switch",
                "left": {"title": "Stitched-together tools", "items": ["Five dashboards, no source of truth", "Brittle integrations", "Per-seat pricing creep", "Slow, generic support"]},
                "right": {"title": "Nimbus", "items": ["One workspace, one truth", "Native integrations", "Predictable pricing", "Engineers on support"]}}},
            {"type": "pricing", "content": {"heading": "Pricing that scales with you", "subhead": "Start free. Upgrade when it pays for itself.",
                "items": [
                    {"name": "Free", "price": "$0", "period": "/mo", "features": ["1 project", "Community support", "Core API"], "cta": {"label": "Get started", "href": "/contact"}},
                    {"name": "Team", "price": "$49", "period": "/mo", "features": ["Unlimited projects", "SSO + audit logs", "Priority support"], "featured": True, "cta": {"label": "Start trial", "href": "/contact"}},
                    {"name": "Enterprise", "price": "Custom", "period": "", "features": ["SLA + SOC 2", "Dedicated infra", "Solutions engineer"], "cta": {"label": "Talk to sales", "href": "/contact"}}]}},
            {"type": "faq", "content": {"heading": "Questions", "items": [
                {"q": "How long does setup take?", "a": "Most teams are live the same day — connect your stack and go."},
                {"q": "Can I self-host?", "a": "Yes — it runs on your own server and domain, fully owned."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Ready to ship faster?", "subhead": "Spin up a workspace in minutes.", "cta": {"label": "Start free", "href": "/contact"}}},
        ],
    },
    # Vitalis — calm, trustworthy healthcare. Teal + soft blue, rounded, patient-first.
    "healthcare": {
        "name": "Vitalis — Health & Care",
        "personality": "reassuring, clean, caring, credible",
        "tokens": {
            "colors": {
                "ink": "#102a2c", "muted": "#566a6b", "paper": "#f1f8f6", "surface": "#ffffff",
                "line": "#d8e8e4", "primary": "#0d7e77", "accent": "#2f6fb0", "highlight": "#f0a838", "link": "#0e7a86",
                "surfaceInverse": "#0c1f21", "inkInverse": "#ecf7f4", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": SANS},
            "radius": {"card": "22px", "control": "14px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "72vh", "sectionGap": "104px", "contentMaxWidth": "1120px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "warm, plain, reassuring", "tone": "caring and clear"},
        "sections": [
            {"type": "hero", "variant": "split", "content": {
                "kicker": "Care you can trust",
                "headline": "Health care that puts", "headlineAccent": "you first.",
                "subhead": "Friendly, modern care with same-week appointments and clinicians who actually listen.",
                "cta": {"label": "Book an appointment", "href": "/contact"}, "secondaryCta": {"label": "Our services", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "30k+", "label": "Patients cared for"}, {"value": "Same-week", "label": "Appointments"},
                {"value": "4.9★", "label": "Patient rating"}, {"value": "15+", "label": "Years of care"}]}},
            {"type": "features", "variant": "cards", "content": {"heading": "Care, the way it should be", "subhead": "Modern medicine with a human touch.", "items": [
                {"icon": "shield", "title": "Trusted clinicians", "body": "Board-certified providers who take the time to listen."},
                {"icon": "gauge", "title": "Short wait times", "body": "Same-week appointments and on-time visits."},
                {"icon": "cloud", "title": "Care anywhere", "body": "Secure telehealth and an easy patient portal."}]}},
            {"type": "problem", "variant": "cards", "content": {"heading": "Tired of the runaround?", "subhead": "Care shouldn't be this hard.", "items": [
                {"icon": "layers", "title": "Long waits", "body": "Weeks for an appointment, hours in the lobby."},
                {"icon": "gauge", "title": "Rushed visits", "body": "Ten minutes and out the door with no answers."},
                {"icon": "shield", "title": "Confusing bills", "body": "Surprise charges and no one to explain them."}]}},
            {"type": "testimonials", "content": {"heading": "What our patients say", "items": [
                {"quote": "They actually listened and explained everything. I felt cared for.", "author": "Maria L.", "role": "Patient"},
                {"quote": "Booked Monday, seen Wednesday. Unheard of.", "author": "James P.", "role": "Patient"},
                {"quote": "The portal makes everything simple — results, refills, messages.", "author": "Aisha K.", "role": "Patient"}]}},
            {"type": "faq", "content": {"heading": "Common questions", "items": [
                {"q": "Do you take my insurance?", "a": "We accept most major plans — call and we'll confirm your coverage in minutes."},
                {"q": "Can I see someone this week?", "a": "Yes — we hold same-week slots for new and existing patients."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Your health, looked after.", "subhead": "Book a visit in under two minutes.", "cta": {"label": "Book now", "href": "/contact"}}},
        ],
    },
    # Saffron — warm, appetizing restaurant / café. Paprika + olive, Fraunces serif.
    "restaurant": {
        "name": "Saffron — Restaurant & Café",
        "personality": "warm, appetizing, inviting, characterful",
        "tokens": {
            "colors": {
                "ink": "#2a1a12", "muted": "#7a685c", "paper": "#fbf3e8", "surface": "#fffaf2",
                "line": "#ecdcc7", "primary": "#c0461f", "accent": "#5c6b3a", "highlight": "#d9a13a", "link": "#a8431f",
                "surfaceInverse": "#20120b", "inkInverse": "#fbeede", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": FRAUNCES},
            "radius": {"card": "14px", "control": "10px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "84vh", "sectionGap": "108px", "contentMaxWidth": "1100px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "warm, sensory, inviting", "tone": "warm and appetizing"},
        "sections": [
            {"type": "hero", "variant": "fullbleed", "content": {
                "badge": "Now taking reservations",
                "headline": "Seasonal plates,", "headlineAccent": "made to gather.",
                "subhead": "A neighborhood kitchen serving honest, market-fresh food and a short, lovely wine list.",
                "cta": {"label": "Reserve a table", "href": "/contact"}, "secondaryCta": {"label": "See the menu", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "Daily", "label": "Market-fresh"}, {"value": "Est. 2014", "label": "Family-run"},
                {"value": "4.8★", "label": "1,200 reviews"}, {"value": "Local", "label": "Sourced"}]}},
            {"type": "features", "variant": "cards", "content": {"heading": "What's cooking", "subhead": "A menu that changes with the season.", "items": [
                {"icon": "sparkles", "title": "Wood-fired", "body": "Blistered crusts and smoky vegetables from the open hearth."},
                {"icon": "book", "title": "Short & seasonal", "body": "A focused menu so every dish is at its peak."},
                {"icon": "mail", "title": "Private events", "body": "Let us host your celebration, dinner, or tasting."}]}},
            {"type": "testimonials", "content": {"heading": "Loved by our regulars", "items": [
                {"quote": "The best meal we've had all year — and we'll be back next week.", "author": "Dana R.", "role": "Regular"},
                {"quote": "Cozy, warm, and the kitchen clearly cares. Our new favorite.", "author": "Marco T.", "role": "Local"},
                {"quote": "Booked it for a birthday — the staff made it unforgettable.", "author": "Priya S.", "role": "Guest"}]}},
            {"type": "faq", "content": {"heading": "Good to know", "items": [
                {"q": "Do you take walk-ins?", "a": "Always — the bar and patio are first-come, and we hold tables for reservations."},
                {"q": "Any dietary options?", "a": "Yes — vegetarian, vegan, and gluten-free dishes change with the season."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Hungry yet?", "subhead": "Reserve your table — we'll save you a seat.", "cta": {"label": "Reserve now", "href": "/contact"}}},
        ],
    },
    # Cornerstone — structured real estate / architecture. Slate + brass, serif, tight grid.
    "realestate": {
        "name": "Cornerstone — Real Estate & Architecture",
        "personality": "assured, premium, grounded, structured",
        "tokens": {
            "colors": {
                "ink": "#1b1d22", "muted": "#6a6f78", "paper": "#f5f5f2", "surface": "#ffffff",
                "line": "#e3e3dd", "primary": "#2b3440", "accent": "#a47e3b", "highlight": "#c9a86a", "link": "#46627e",
                "surfaceInverse": "#14171c", "inkInverse": "#f0efe9", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": SERIF},
            "radius": {"card": "8px", "control": "6px", "pill": "999px"},
            "layout": {"density": "compact", "heroMinHeight": "76vh", "sectionGap": "100px", "contentMaxWidth": "1180px", "cardPadding": "24px"},
        },
        "voice": {"headlineStyle": "assured, location-led", "tone": "polished and grounded"},
        "sections": [
            {"type": "hero", "variant": "split", "content": {
                "kicker": "Property, done properly",
                "headline": "Find the address that", "headlineAccent": "feels like home.",
                "subhead": "Local expertise, honest advice, and a calm hand through every step of the move.",
                "cta": {"label": "Book a viewing", "href": "/contact"}, "secondaryCta": {"label": "Browse listings", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "$2.1B", "label": "Sold to date"}, {"value": "1,400+", "label": "Homes closed"},
                {"value": "21 days", "label": "Avg. to offer"}, {"value": "98%", "label": "Of asking"}]}},
            {"type": "logos", "content": {"heading": "Featured in", "items": [{"label": "Architectural Digest"}, {"label": "Dwell"}, {"label": "The Times"}, {"label": "Mansion Global"}]}},
            {"type": "comparison", "content": {"heading": "A better way to move",
                "left": {"title": "The usual agent", "items": ["Lists and waits", "Generic photos", "Hard to reach", "One-size advice"]},
                "right": {"title": "Cornerstone", "items": ["Priced with real data", "Architectural photography", "Direct line to your agent", "A plan built around you"]}}},
            {"type": "testimonials", "content": {"heading": "From our clients", "items": [
                {"quote": "Sold above asking in under three weeks. Calm, sharp, and honest throughout.", "author": "The Halls", "role": "Sellers"},
                {"quote": "They understood the building's character and found exactly the right buyer.", "author": "L. Moreau", "role": "Architect"},
                {"quote": "First-time buyers and they made it feel effortless.", "author": "Sam & Nia", "role": "Buyers"}]}},
            {"type": "faq", "content": {"heading": "Questions", "items": [
                {"q": "What are your fees?", "a": "A simple, transparent commission agreed up front — no surprises at closing."},
                {"q": "Do you handle rentals too?", "a": "Yes — sales, lettings, and property management across the city."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Thinking of making a move?", "subhead": "Get a free, no-pressure valuation.", "cta": {"label": "Request a valuation", "href": "/contact"}}},
        ],
    },
    # Ignite — high-energy fitness / sport. Dark canvas, condensed display, volt accent.
    "fitness": {
        "name": "Ignite — Fitness & Sport",
        "personality": "high-energy, bold, motivating, athletic",
        "tokens": {
            "colors": {
                "ink": "#eef2f0", "muted": "#9aa6a1", "paper": "#0d1110", "surface": "#161b19",
                "line": "#29302d", "primary": "#e0452a", "accent": "#9ae64d", "highlight": "#c6ff3a", "link": "#ff7d52",
                "surfaceInverse": "#06090a", "inkInverse": "#eef2f0", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": CONDENSED},
            "radius": {"card": "12px", "control": "8px", "pill": "8px"},
            "layout": {"density": "comfortable", "heroMinHeight": "92vh", "sectionGap": "112px", "contentMaxWidth": "1160px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "punchy, imperative, motivating", "tone": "high-energy and direct"},
        "sections": [
            {"type": "hero", "variant": "fullbleed", "content": {
                "badge": "First class free",
                "headline": "Stronger starts", "headlineAccent": "today.",
                "subhead": "Coach-led training, real community, and a plan that meets you where you are.",
                "cta": {"label": "Start free trial", "href": "/contact"}, "secondaryCta": {"label": "See classes", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "120+", "label": "Classes / week"}, {"value": "3,000+", "label": "Members strong"},
                {"value": "24/7", "label": "Gym access"}, {"value": "12", "label": "Expert coaches"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "Train your way", "subhead": "Strength, conditioning, and recovery under one roof.", "items": [
                {"icon": "zap", "title": "Strength", "body": "Coached lifting programs that actually progress."},
                {"icon": "gauge", "title": "Conditioning", "body": "HIIT and endurance classes that push your limits."},
                {"icon": "shield", "title": "Recovery", "body": "Mobility, sauna, and recovery built into your week."}]}},
            {"type": "comparison", "content": {"heading": "Not your average gym",
                "left": {"title": "Big-box gym", "items": ["Rows of empty machines", "No guidance", "Cancel-anytime guilt trip", "Zero community"]},
                "right": {"title": "Ignite", "items": ["Coach-led every session", "A plan built for you", "Flexible, honest membership", "A crew that shows up"]}}},
            {"type": "pricing", "content": {"heading": "Membership", "subhead": "No contracts. Cancel anytime.",
                "items": [
                    {"name": "Day Pass", "price": "$15", "period": "/day", "features": ["All classes", "Full gym floor", "Locker + sauna"], "cta": {"label": "Drop in", "href": "/contact"}},
                    {"name": "Unlimited", "price": "$99", "period": "/mo", "features": ["Unlimited classes", "24/7 access", "Free guest passes"], "featured": True, "cta": {"label": "Join now", "href": "/contact"}},
                    {"name": "Coached", "price": "$199", "period": "/mo", "features": ["Everything in Unlimited", "1:1 coaching", "Custom programming"], "cta": {"label": "Go all in", "href": "/contact"}}]}},
            {"type": "testimonials", "content": {"heading": "Real members, real results", "items": [
                {"quote": "Down 18 pounds and finally strong. The coaches make it stick.", "author": "Tyler M.", "role": "Member, 1 year"},
                {"quote": "I dreaded the gym. Now it's the best hour of my day.", "author": "Renee K.", "role": "Member"},
                {"quote": "The community is unreal. You can't skip when people are waiting for you.", "author": "Devon A.", "role": "Member"}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Your first class is on us.", "subhead": "No pressure. Just show up.", "cta": {"label": "Claim free class", "href": "/contact"}}},
        ],
    },
    # Lumière — elegant beauty / spa. Blush + mauve, Fraunces serif, soft and airy.
    "beauty": {
        "name": "Lumière — Beauty & Spa",
        "personality": "elegant, calming, refined, welcoming",
        "tokens": {
            "colors": {
                "ink": "#2e2230", "muted": "#7d6f7a", "paper": "#fbf3f5", "surface": "#fffafc",
                "line": "#f0e0e6", "primary": "#9d4a62", "accent": "#8a6a9a", "highlight": "#cf9f6a", "link": "#9a5578",
                "surfaceInverse": "#241620", "inkInverse": "#fbeef2", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": FRAUNCES},
            "radius": {"card": "22px", "control": "16px", "pill": "999px"},
            "layout": {"density": "spacious", "heroMinHeight": "80vh", "sectionGap": "116px", "contentMaxWidth": "1100px", "cardPadding": "28px"},
        },
        "voice": {"headlineStyle": "elegant, inviting, sensorial", "tone": "refined and welcoming"},
        "sections": [
            {"type": "hero", "variant": "centered", "content": {
                "badge": "New guest offer — 20% off",
                "headline": "Time to glow,", "headlineAccent": "beautifully you.",
                "subhead": "A calm, modern studio for skin, hair, and the kind of self-care you look forward to.",
                "cta": {"label": "Book your visit", "href": "/contact"}, "secondaryCta": {"label": "View treatments", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "4.9★", "label": "800+ reviews"}, {"value": "Clean", "label": "Beauty only"},
                {"value": "10+", "label": "Expert artists"}, {"value": "Est. 2016", "label": "Loved locally"}]}},
            {"type": "features", "variant": "cards", "content": {"heading": "Treatments", "subhead": "Thoughtful rituals, expert hands.", "items": [
                {"icon": "sparkles", "title": "Signature facials", "body": "Tailored to your skin with clean, effective products."},
                {"icon": "layers", "title": "Hair & color", "body": "Lived-in color and cuts that grow out beautifully."},
                {"icon": "shield", "title": "Spa & massage", "body": "Unwind with restorative bodywork and quiet."}]}},
            {"type": "testimonials", "content": {"heading": "Guests adore us", "items": [
                {"quote": "I left glowing and completely relaxed. My new monthly ritual.", "author": "Hannah W.", "role": "Member"},
                {"quote": "Best color I've ever had — and the studio is gorgeous.", "author": "Sofia D.", "role": "Guest"},
                {"quote": "Calm, clean, and genuinely caring. I never want to leave.", "author": "Mei L.", "role": "Guest"}]}},
            {"type": "pricing", "content": {"heading": "The menu", "subhead": "Memberships save on every visit.",
                "items": [
                    {"name": "Express", "price": "$60", "period": "/visit", "features": ["30-min facial", "Skin consult", "Product samples"], "cta": {"label": "Book", "href": "/contact"}},
                    {"name": "Signature", "price": "$120", "period": "/visit", "features": ["75-min facial", "LED + massage", "Take-home regimen"], "featured": True, "cta": {"label": "Book", "href": "/contact"}},
                    {"name": "Membership", "price": "$99", "period": "/mo", "features": ["One signature / mo", "20% off add-ons", "Priority booking"], "cta": {"label": "Join", "href": "/contact"}}]}},
            {"type": "faq", "content": {"heading": "Before you visit", "items": [
                {"q": "Can I come in for a consult first?", "a": "Of course — complimentary consults help us tailor every treatment to you."},
                {"q": "What products do you use?", "a": "Clean, cruelty-free lines chosen for results and gentleness."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Treat yourself today.", "subhead": "New guests enjoy 20% off the first visit.", "cta": {"label": "Book your visit", "href": "/contact"}}},
        ],
    },
    # Sterling — authoritative law / advisory. Deep navy + gold, serif, conservative.
    "legal": {
        "name": "Sterling — Law & Advisory",
        "personality": "authoritative, precise, discreet, trustworthy",
        "tokens": {
            "colors": {
                "ink": "#0f1a32", "muted": "#5e6a82", "paper": "#f6f7fa", "surface": "#ffffff",
                "line": "#dde2ec", "primary": "#1b3a6b", "accent": "#8a6d3b", "highlight": "#b8924c", "link": "#285a9c",
                "surfaceInverse": "#0b1426", "inkInverse": "#eef2f9", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": SERIF},
            "radius": {"card": "8px", "control": "6px", "pill": "999px"},
            "layout": {"density": "compact", "heroMinHeight": "68vh", "sectionGap": "100px", "contentMaxWidth": "1160px", "cardPadding": "24px"},
        },
        "voice": {"headlineStyle": "authoritative, precise, outcome-led", "tone": "measured and credible"},
        "sections": [
            {"type": "hero", "variant": "split", "content": {
                "kicker": "Counsel you can rely on",
                "headline": "Clear advice when", "headlineAccent": "it matters most.",
                "subhead": "Senior lawyers, straight answers, and a steady hand through every matter — large or small.",
                "cta": {"label": "Request a consultation", "href": "/contact"}, "secondaryCta": {"label": "Practice areas", "href": "/blog"}}},
            {"type": "logos", "content": {"heading": "Recognized by", "items": [{"label": "Chambers"}, {"label": "Legal 500"}, {"label": "Best Lawyers"}, {"label": "Super Lawyers"}]}},
            {"type": "stats", "content": {"items": [
                {"value": "40+", "label": "Years combined"}, {"value": "$500M+", "label": "Recovered"},
                {"value": "95%", "label": "Favorable outcomes"}, {"value": "24h", "label": "Response time"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "How we help", "subhead": "Focused practice areas, senior attention on every file.", "items": [
                {"icon": "shield", "title": "Corporate & commercial", "body": "Formation, contracts, and deals done right."},
                {"icon": "book", "title": "Disputes & litigation", "body": "Prepared, persuasive, and pragmatic in the room."},
                {"icon": "layers", "title": "Private client", "body": "Wills, estates, and the matters closest to home."}]}},
            {"type": "comparison", "content": {"heading": "The Sterling difference",
                "left": {"title": "Big firms", "items": ["Passed to junior staff", "Billed for every email", "Hard to reach", "Jargon over clarity"]},
                "right": {"title": "Sterling", "items": ["Senior lawyer on your file", "Clear, agreed fees", "Direct line to counsel", "Plain-English advice"]}}},
            {"type": "testimonials", "content": {"heading": "Client confidence", "items": [
                {"quote": "Calm, sharp, and completely on top of the detail. The outcome spoke for itself.", "author": "Director", "role": "Manufacturing client"},
                {"quote": "They explained the risk plainly and got us a result fast.", "author": "Founder", "role": "Tech client"},
                {"quote": "Handled a difficult estate with real care and discretion.", "author": "Private client", "role": "Estate matter"}]}},
            {"type": "faq", "content": {"heading": "Common questions", "items": [
                {"q": "How are fees structured?", "a": "Transparently — fixed fees where possible, agreed in writing before we start."},
                {"q": "Is a first consultation free?", "a": "Yes — an initial consultation to understand your matter is complimentary."}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Need clear counsel?", "subhead": "Request a confidential consultation today.", "cta": {"label": "Request a consultation", "href": "/contact"}}},
        ],
    },
    # Kinetic — bold creative studio / agency. Near-black + acid accent, oversized grotesk.
    "creative": {
        "name": "Kinetic — Studio & Agency",
        "personality": "bold, expressive, contemporary, confident",
        "tokens": {
            "colors": {
                "ink": "#0a0a0a", "muted": "#6a6a6a", "paper": "#f4f4f0", "surface": "#ffffff",
                "line": "#e2e2dc", "primary": "#141414", "accent": "#ff4d2e", "highlight": "#d6ff3f", "link": "#ff4d2e",
                "surfaceInverse": "#0a0a0a", "inkInverse": "#f4f4f0", "onPrimary": "#ffffff",
            },
            "typography": {"body": SANS, "heading": GROTESK},
            "radius": {"card": "6px", "control": "4px", "pill": "999px"},
            "layout": {"density": "comfortable", "heroMinHeight": "88vh", "sectionGap": "120px", "contentMaxWidth": "1160px", "cardPadding": "26px"},
        },
        "voice": {"headlineStyle": "bold, oversized, expressive", "tone": "confident and creative"},
        "sections": [
            {"type": "hero", "variant": "centered", "content": {
                "badge": "Studio for hire",
                "headline": "Ideas worth", "headlineAccent": "staring at.",
                "subhead": "A small studio making brands, sites, and campaigns that refuse to blend in.",
                "cta": {"label": "Start a project", "href": "/contact"}, "secondaryCta": {"label": "See the work", "href": "/blog"}}},
            {"type": "logos", "content": {"heading": "Selected clients", "items": [{"label": "Aēsop"}, {"label": "MUBI"}, {"label": "Monzo"}, {"label": "Patagonia"}, {"label": "Frieze"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "What we make", "subhead": "Strategy, identity, and the craft to ship it.", "items": [
                {"icon": "sparkles", "title": "Brand identity", "body": "Names, logos, and systems with a point of view."},
                {"icon": "layers", "title": "Websites", "body": "Fast, distinctive sites built to convert and last."},
                {"icon": "zap", "title": "Campaigns", "body": "Launches and films that earn attention, not buy it."}]}},
            {"type": "comparison", "content": {"heading": "Why work with us",
                "left": {"title": "The big agency", "items": ["Layers of account managers", "Templated thinking", "Slow, costly rounds", "You're one of fifty"]},
                "right": {"title": "Kinetic", "items": ["Founders on every project", "Original every time", "Tight, senior team", "You're the only one"]}}},
            {"type": "testimonials", "content": {"heading": "Kind words", "items": [
                {"quote": "They gave us an identity people actually talk about. Sales followed.", "author": "CEO", "role": "DTC brand"},
                {"quote": "Fast, fearless, and ridiculously talented. Just hire them.", "author": "CMO", "role": "Fintech"},
                {"quote": "The site doubled our conversion and won an award. Both.", "author": "Founder", "role": "Studio"}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Got something to launch?", "subhead": "Tell us what you're building.", "cta": {"label": "Start a project", "href": "/contact"}}},
        ],
    },
    # Onyx — luxe: near-black + gold, Fraunces serif, generous space. Premium/luxury.
    "luxe": {
        "name": "Onyx — Luxe",
        "personality": "elegant, premium, understated, high-contrast",
        "tokens": {
            "colors": {
                "ink": "#f4efe6", "muted": "#a99f8c", "paper": "#0c0b09", "surface": "#16140f",
                "line": "#2a2620", "primary": "#c9a24a", "accent": "#c9a24a", "highlight": "#d9bd6e", "link": "#d9bd6e",
                "surfaceInverse": "#060504", "inkInverse": "#f4efe6", "onPrimary": "#14110c",
            },
            "typography": {"body": SANS, "heading": FRAUNCES},
            "radius": {"card": "4px", "control": "3px", "pill": "999px"},
            "layout": {"density": "spacious", "heroMinHeight": "92vh", "sectionGap": "132px", "contentMaxWidth": "1080px", "cardPadding": "30px"},
        },
        "voice": {"headlineStyle": "elegant, restrained, premium", "tone": "understated luxury"},
        "sections": [
            {"type": "hero", "variant": "centered", "content": {
                "badge": "By design",
                "headline": "Crafted to be", "headlineAccent": "remembered.",
                "subhead": "A quiet, premium presence — considered type, deep contrast, and room to breathe. Nothing shouts; everything lingers.",
                "cta": {"label": "Begin", "href": "/contact"}, "secondaryCta": {"label": "View work", "href": "/blog"}}},
            {"type": "stats", "content": {"items": [
                {"value": "1:1", "label": "Made to order"}, {"value": "Gold", "label": "Standard"},
                {"value": "Quiet", "label": "Luxury"}, {"value": "Yours", "label": "Entirely"}]}},
            {"type": "logos", "content": {"heading": "In good company", "items": [{"label": "Aurum"}, {"label": "Noir"}, {"label": "Maison"}, {"label": "Élan"}]}},
            {"type": "features", "variant": "minimal", "content": {"heading": "Considered, end to end.", "subhead": "Restraint is the luxury.", "items": [
                {"icon": "sparkles", "title": "Refined", "body": "Every detail weighed — type, space, and tone."},
                {"icon": "shield", "title": "Enduring", "body": "Built to age well, not to chase trends."},
                {"icon": "layers", "title": "Bespoke", "body": "Made for you, owned by you, like nothing else."}]}},
            {"type": "comparison", "content": {"heading": "Quiet beats loud.",
                "left": {"title": "Off the shelf", "items": ["Templated and obvious", "Busy and bright", "Built to convert, fast", "Looks like the rest"]},
                "right": {"title": "Onyx", "items": ["Bespoke and discreet", "Calm, deep, gold-touched", "Built to last", "Unmistakably yours"]}}},
            {"type": "testimonials", "content": {"heading": "Quietly admired", "items": [
                {"quote": "It feels expensive in the best way — calm, sure of itself.", "author": "A. Laurent", "role": "Maison"},
                {"quote": "Understated and unforgettable. Exactly the brand we wanted.", "author": "R. Vance", "role": "Atelier"},
                {"quote": "People slow down on it. That's the whole point.", "author": "M. Sole", "role": "Studio"}]}},
            {"type": "cta", "variant": "banner", "content": {"headline": "Make something lasting.", "subhead": "A quiet conversation to begin.", "cta": {"label": "Get in touch", "href": "/contact"}}},
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
