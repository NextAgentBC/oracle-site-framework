# OpenClaw Competitor Analyzer Workflow

This workflow is for OpenClaw or a local Codex agent with browser access.

Goal: inspect competitor websites, produce a distinct design profile, and update the project through `/api/admin/design/analyze-competitors`.

## Inputs

- `industry`: education, accounting, retail, healthcare, real estate, etc.
- `competitorUrls`: 2-5 public websites in the same category or local market.
- `adminToken`: JWT from Google login for an admin user.
- `apiBase`: usually `https://api.student-domain.example/api`.

## Browser Inspection

For each competitor URL:

1. Open the homepage.
2. Capture visible first-viewport observations:
   - main colors
   - typeface impression or CSS font names if visible in dev tools
   - nav density
   - hero style
   - button shape
   - card/grid patterns
   - imagery style
   - trust signals
3. Visit one service/product/blog page if available.
4. Do not copy logos, exact brand palettes, proprietary illustrations, slogans, or page copy.

## API Update

Send observations to the backend:

```bash
curl -X POST "$API_BASE/admin/design/analyze-competitors" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "accounting",
    "competitorUrls": [
      "https://example-accounting.com",
      "https://another-firm.com"
    ],
    "observations": [
      {
        "url": "https://example-accounting.com",
        "colors": ["#123f35", "#d8d2c7"],
        "fonts": ["Source Sans 3"],
        "layoutNotes": "Compact professional layout, service cards, strong consultation CTA."
      }
    ],
    "notes": "Create a distinct local accounting identity. Use professional density and calm contrast."
  }'
```

## Verification

After the update:

```bash
curl "$API_BASE/design"
```

Then rebuild or reload the frontend and verify:

- Colors changed through CSS variables.
- Font stacks changed through design tokens.
- Layout density fits the industry.
- The result does not resemble any one competitor too closely.

