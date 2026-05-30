# OpenClaw Maintenance Notes

Maintain the project by respecting these boundaries:

- `frontend/` may call only documented backend endpoints from `docs/api-contract.md`.
- `backend/app/models.py` is the database source of truth.
- `backend/app/services/` contains replaceable integrations: AI, email, auth verification.
- `backend/app/routes/` contains HTTP behavior only.
- Do not put API secrets in source files. Use `.env`.
- Blog generation must keep SEO fields: `title`, `slug`, `excerpt`, `meta_title`, `meta_description`, `canonical_url`, `tags`.

Common tasks:

- Add an industry: update `backend/app/config.py` defaults and `.env`.
- Change newsletter provider: implement a new service in `backend/app/services/email_service.py`.
- Add admin UI: create frontend pages that call `/api/admin/*`.
- Add approval workflow: generate blog posts with `status=draft`, then publish later.

