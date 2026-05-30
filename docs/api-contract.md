# API Contract

The backend is intentionally OpenClaw-friendly: resources are grouped by domain, responses are JSON, and the API has a small stable surface.

## Public Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/site` | Public site config |
| `POST` | `/api/auth/google` | Verify Google ID token and create/login user |
| `GET` | `/api/blogs` | List published blog posts |
| `GET` | `/api/blogs/:slug` | Read one blog post |
| `POST` | `/api/newsletter/subscribe` | Subscribe an email |
| `POST` | `/api/contact` | Send a contact message |

## Admin Endpoints

Admin endpoints require `Authorization: Bearer <token>` where the token comes from `/api/auth/google`.

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/admin/blogs/generate` | Generate a draft or published AI blog |
| `POST` | `/api/admin/blogs` | Create a manual blog post |
| `PATCH` | `/api/admin/blogs/:id` | Update a blog post |

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

