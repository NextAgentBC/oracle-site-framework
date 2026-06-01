---
name: oracle-site-block-section
description: "Custom section (flexible) block — add or edit a custom section (flexible) on any Oracle Site page by natural language. Thin recipe over the compose engine (section). Triggers (zh+en): 加一个自定义板块 / 照着截图做个 section / 柔性板块 / custom section / build from a screenshot / flexible block."
metadata:
  version: 0.1.0
  generated: true
  openclaw:
    category: "website"
    requires:
      bins:
        - curl
---

# Custom section (flexible) block (`section`)

> Auto-generated from the block manifest (`GET /api/blocks`). Full engine, rules,
> and edit/move/remove recipes: `../oracle-site-compose/SKILL.md`.
> Prerequisite: `../oracle-site-shared/SKILL.md` for `$ORACLE_SITE_API` + `$ORACLE_SITE_TOKEN`.

Flexible token-driven section for layouts the fixed blocks don't cover (e.g. captured from a screenshot). Pick a variant (grid/split/stack/banner), set layout.columns 1-4, layout.align left|center, layout.media none|left|right|top, layout.tone plain|tint|inverse. Each item has a 'kind': feature/stat/quote/step/media/text/button. Never copy a source's exact colors — colors come from the site's tokens.

- Variants: `grid` · `split` · `stack` · `banner`
- Content fields: `eyebrow` (text), `heading` (text), `subhead` (textarea), `layout` (object), `items` (list), `cta` (cta)

`target` is `home` or a page slug. Adding scaffolds sensible defaults, so the
block looks complete immediately — pass `content` only to override.

```bash
# Add a custom section (flexible) to the home page
curl -s -X POST "$ORACLE_SITE_API/admin/compose/home/blocks" \
  -H "Authorization: Bearer $ORACLE_SITE_TOKEN" -H "Content-Type: application/json" \
  -d '{"type":"section","position":"end"}'
```

To **edit / move / remove** an existing one: list blocks to get its id, then use
the compose engine (PATCH content, `/move`, DELETE) or a `batch` call. For
multi-step requests prefer `POST /admin/compose/{target}/batch`. See
`../oracle-site-compose/SKILL.md`.
