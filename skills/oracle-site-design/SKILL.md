---
name: oracle-site-design
description: "Read or change the Oracle Site UI/UX design profile (colors, fonts, radius, layout) over its API. Triggers: '改主题色 / 换配色 / 改颜色', 'change site colors/theme', '改字体', '生成设计风格 / 换风格', 'generate design profile', '分析竞品设计', 'competitor design', '看当前设计'."
metadata:
  version: 0.1.0
  openclaw:
    category: "website"
    requires:
      bins:
        - curl
---

# Oracle Site — Design Profile

> Prerequisite: read `../oracle-site-shared/SKILL.md` for `$ORACLE_SITE_API`, auth, and `$ORACLE_SITE_TOKEN`.

The frontend maps these tokens to CSS variables. Change the look-and-feel through this API, not by hardcoding colors/fonts in components.

## Public (no auth)

```bash
curl -s "$ORACLE_SITE_API/design"        # active profile: tokens.colors / typography / radius / layout, voice, notes
```

## Admin (Bearer token)

```bash
# Read full admin view
curl -s -H "Authorization: Bearer $ORACLE_SITE_TOKEN" "$ORACLE_SITE_API/admin/design"

# Update specific tokens (merged into the profile)
curl -s -X PATCH "$ORACLE_SITE_API/admin/design" \
  -H "Authorization: Bearer $ORACLE_SITE_TOKEN" -H "Content-Type: application/json" \
  -d '{"tokens": {"colors": {"primary": "#174f7a", "accent": "#b85c38"}}}'

# Generate a fresh profile for an industry (uses competitor URLs as references only)
curl -s -X POST "$ORACLE_SITE_API/admin/design/generate" \
  -H "Authorization: Bearer $ORACLE_SITE_TOKEN" -H "Content-Type: application/json" \
  -d '{"industry": "accounting", "competitorUrls": ["https://a.example","https://b.example"], "notes": "Distinct identity, not a copy."}'

# Feed observed competitor signals to inform a distinct profile
curl -s -X POST "$ORACLE_SITE_API/admin/design/analyze-competitors" \
  -H "Authorization: Bearer $ORACLE_SITE_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "industry": "retail",
    "competitorUrls": ["https://shop.example"],
    "observations": [{"url":"https://shop.example","colors":["#a6422b"],"fonts":["Nunito Sans"],"layoutNotes":"warm, product-forward"}],
    "notes": "Use category conventions, create a distinct identity."
  }'
```

Never copy a competitor's exact brand — infer category conventions and produce a distinct profile.
