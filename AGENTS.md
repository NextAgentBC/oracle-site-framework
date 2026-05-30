# Codex Agent Instructions

Use this file when operating inside this repository.

- Prefer PostgreSQL for all real tests.
- Keep frontend and backend separated.
- Keep public API changes documented in `docs/api-contract.md` and `backend/app/openapi.json`.
- Do not commit `.env`, `.env.local`, `.venv`, `.next`, `node_modules`, or local databases.
- Before saying the project works, run backend route/migration checks and frontend typecheck/build.
- For deployment, target `oracle-server:/home/ubuntu/projects/oracle-site` unless the human gives another path.
- Prefer Cloudflare Tunnel over direct public Nginx exposure.

