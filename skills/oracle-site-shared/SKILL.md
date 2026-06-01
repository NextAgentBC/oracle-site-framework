---
name: oracle-site-shared
description: "Oracle Site API basics + auth — READ FIRST. Base URL, admin token issuance, conventions, plus site config, health, OpenAPI, and Google login. Triggers: 'oracle 网站 / 网站 API', 'site health 状态', '拿/签发 admin token', 'admin token', '网站信息 / site info', 'openapi 契约'."
metadata:
  version: 0.1.0
  openclaw:
    category: "website"
    requires:
      bins:
        - curl
---

# Oracle Site — Shared Reference (read first)

Wraps the framework's HTTP API (full contract: `GET $ORACLE_SITE_API/openapi.json`).
Public endpoints need no auth; admin endpoints need an admin bearer token.

## Configure

```bash
export ORACLE_SITE_API="https://oracle-api.nextagent.ca/api"   # this deployment's API base
```

Public routes: `$ORACLE_SITE_API/...` (e.g. `/blogs`). Admin routes: `$ORACLE_SITE_API/admin/...`.

## Auth (admin token)

Admin routes require `Authorization: Bearer <jwt>`. Two ways to get one:

1. **Interactive (browser):** Google Sign-In on the site (`POST /auth/google`).
2. **Non-interactive (agents — no browser):** run where the backend runs:

```bash
export ORACLE_SITE_TOKEN="$(docker compose -f /home/ubuntu/projects/oracle-site/docker-compose.yml \
  exec -T backend flask --app app.main token issue --email you@example.com)"
```

The email must be in the backend's `ADMIN_EMAILS`. `--days N` overrides lifetime (default 168h).

## Conventions

- JSON in/out. Single object → `{"item": {...}}`, list → `{"items": [...]}`.
- Errors → `{"error": {"code","message"}}` (401 missing/bad token, 403 not admin, 404 not found).
- Send `-H "Content-Type: application/json"` on POST/PATCH.
- **Locales (i18n):** `GET /site` → `locales` + `defaultLocale`. Read localized content with
  `?locale=zh` on `/design`, `/pages*`, `/blogs*`; write it with `?locale=zh` on the matching
  admin routes (content goes into that locale's overlay, default columns untouched). UI chrome
  strings: `GET /i18n/<locale>`, `PATCH /admin/i18n/<locale>`. Full guide: `../oracle-site-i18n`.

## Skill map

- `oracle-site-blog` · `…-pages` · `…-newsletter` — content over the API.
- `oracle-site-design` — theme/tokens + the 12 style templates. `…-compose` — block-level page editing.
- `oracle-site-capture` — rebuild a section from a screenshot (flexible `section` block + `/patterns` library).
- `oracle-site-i18n` — translate content + chrome (path-based `/zh`). `…-ops` — deploy/status.

## Site basics & login (public, no token)

```bash
curl -s "$ORACLE_SITE_API/health"        # {"database":"ok","status":"ok"} — readiness
curl -s "$ORACLE_SITE_API/site"          # name, industry, audience, region, url
curl -s "$ORACLE_SITE_API/openapi.json"  # full machine-readable contract

# Exchange a Google ID token (browser sign-in) for the site JWT:
curl -s -X POST "$ORACLE_SITE_API/auth/google" -H "Content-Type: application/json" \
  -d '{"credential": "<google-id-token>"}'   # -> {"item":{"user":{...},"token":"<jwt>"}}
```
