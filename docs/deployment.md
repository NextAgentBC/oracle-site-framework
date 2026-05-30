# Deployment Guide

## Recommended: Cloudflare Tunnel

Use Cloudflare Tunnel for the lecture framework.

Why:

- Students do not need to expose Oracle VM ports 80/443.
- TLS is handled by Cloudflare.
- The public IP can remain private from normal visitors.
- Domain routing is repeatable: `example.com` -> Next.js, `api.example.com` -> Flask.

Basic shape:

```text
Cloudflare DNS
  example.com      -> tunnel -> localhost:3000
  api.example.com  -> tunnel -> localhost:8000
Oracle VM
  nextjs service on 127.0.0.1:3000
  flask service on 127.0.0.1:8000
```

See `ops/cloudflared/config.yml.example`.

## Fallback: Static IP + Nginx

Use this when you explicitly want students to learn classic DNS and reverse proxy.

```text
Cloudflare DNS A record -> Oracle static IP
Nginx
  /      -> localhost:3000
  /api/  -> localhost:8000
```

See `ops/nginx/oracle-site.conf.example`.

## Daily Blog Job

Run once per day:

```bash
cd /opt/oracle-site/backend
. .venv/bin/activate
flask --app app.main blog generate-daily
```

Use `ops/systemd/oracle-blog.timer` and `ops/systemd/oracle-blog.service`.

