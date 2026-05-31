# API Contract

The backend is intentionally OpenClaw-friendly: resources are grouped by domain, responses are JSON, and the API has a small stable surface.

## Public Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/site` | Public site config |
| `GET` | `/api/design` | Active UI/UX design profile |
| `POST` | `/api/auth/google` | Verify Google ID token and create/login user |
| `GET` | `/api/blogs` | List published blog posts |
| `GET` | `/api/blogs/:slug` | Read one blog post |
| `GET` | `/api/pages` | List published content pages |
| `GET` | `/api/pages/:slug` | Read one content page |
| `POST` | `/api/newsletter/subscribe` | Subscribe an email |
| `POST` | `/api/contact` | Send a contact message |

## Admin Endpoints

Admin endpoints require `Authorization: Bearer <token>` where the token comes from `/api/auth/google` (browser) or, for agents/CI, `flask --app app.main token issue --email <admin>` (non-interactive).

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/admin/blogs/generate` | Generate a draft or published AI blog |
| `POST` | `/api/admin/blogs` | Create a manual blog post |
| `PATCH` | `/api/admin/blogs/:id` | Update a blog post |
| `POST` | `/api/admin/pages` | Create a content page |
| `PATCH` | `/api/admin/pages/:id` | Update a content page |
| `DELETE` | `/api/admin/pages/:id` | Delete a content page |
| `GET` | `/api/admin/design` | Read active UI/UX design profile |
| `PATCH` | `/api/admin/design` | Update design tokens, voice, and notes |
| `POST` | `/api/admin/design/generate` | Generate an industry/competitor-informed design profile |
| `POST` | `/api/admin/design/analyze-competitors` | Fetch competitor signals and update active design profile |

## Design Profile

The frontend must not hard-code industry styling. It reads `GET /api/design` and maps tokens to CSS variables.

```json
{
  "item": {
    "name": "Professional Ledger",
    "source": "generated-from-industry-and-competitors",
    "industry": "accounting",
    "personality": "precise, steady, discreet, professional",
    "competitorUrls": ["https://example-accounting-firm.com"],
    "tokens": {
      "colors": {
        "ink": "#15201d",
        "muted": "#65706d",
        "paper": "#f6f7f4",
        "surface": "#ffffff",
        "line": "#d9dfda",
        "primary": "#1f5f4a",
        "accent": "#8f3f3b",
        "highlight": "#b88a2d",
        "link": "#275f91"
      },
      "typography": {
        "body": "Source Sans 3, Arial, Helvetica, sans-serif",
        "heading": "Source Sans 3, Arial, Helvetica, sans-serif",
        "mono": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
      },
      "radius": {
        "card": "8px",
        "control": "8px",
        "pill": "999px"
      },
      "layout": {
        "contentMaxWidth": "1120px",
        "heroMinHeight": "50vh",
        "density": "compact",
        "cardPadding": "20px",
        "sectionGap": "54px"
      }
    },
    "voice": {
      "headlineStyle": "plain offer or brand name",
      "tone": "precise, plainspoken, risk-aware"
    },
    "notes": "Design rationale and competitor observations."
  }
}
```

## Competitor Analyzer

`POST /api/admin/design/analyze-competitors` accepts competitor URLs and optional OpenClaw visual observations. The backend fetches public HTML/CSS signals such as title, metadata, colors, font-family declarations, and basic content cues, then updates the active design profile.

Request:

```json
{
  "industry": "retail",
  "competitorUrls": [
    "https://example-retailer.com",
    "https://another-local-shop.com"
  ],
  "observations": [
    {
      "url": "https://example-retailer.com",
      "colors": ["#a6422b", "#28666e"],
      "fonts": ["Nunito Sans"],
      "layoutNotes": "Dense product grid, clear sale calls to action, warm editorial imagery."
    }
  ],
  "notes": "Use category conventions without copying brand identity."
}
```

Response:

```json
{
  "item": {
    "name": "Local Retail Signal",
    "source": "competitor-analyzer",
    "tokens": {}
  },
  "analysis": {
    "snapshots": [],
    "observations": [],
    "dominantColors": [],
    "dominantFonts": []
  }
}
```

## Response Shape

Successful list:

```json
{
  "items": [],
  "meta": { "count": 0 }
}
```

Successful object:

```json
{
  "item": {}
}
```

Error:

```json
{
  "error": {
    "code": "bad_request",
    "message": "Human readable message"
  }
}
```
