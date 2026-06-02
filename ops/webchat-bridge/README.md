# Webchat bridge

Host-side glue connecting the (containerized) website backend to the OpenClaw gateway,
so the website's chat widget is answered by 小爪 — safely.

```
visitor → widget → backend /api/chat (container)
                      │  POST http://host.docker.internal:18791/chat  (X-Bridge-Token)
                      ▼
                 webchat-bridge (host, this dir)
                      ├─ openclaw infer model run --gateway   → reply  (TOOL-LESS, sandboxed)
                      └─ openclaw message send --channel telegram → mirror to operator
```

## Why a separate host service

The backend runs in Docker; the `openclaw` CLI + gateway live on the host. The container
can't run `openclaw`, so this tiny stdlib-only HTTP service is the bridge it calls.

## Security model

The chat brain is `openclaw infer model run` — a **one-shot model completion, not the agent
harness**. There is **no tool surface**: no shell, no file access, no message-send, no skills.
A visitor can type anything; the worst case is the model returns some text. The prompt
(assembled by the backend) contains only public site knowledge + this visitor's own
conversation — never private memory or files. The endpoint is gated by a shared bearer token
(`X-Bridge-Token`), and the port is not reachable from the internet (Oracle security list
allows only :22 inbound).

## Install

```bash
cp ops/webchat-bridge/.env.example ops/webchat-bridge/.env   # fill token + TG target
cp ops/webchat-bridge/webchat-bridge.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now webchat-bridge.service
curl -s http://127.0.0.1:18791/health     # {"ok":true,...}
```

`WEBCHAT_BRIDGE_TOKEN` must match `backend/.env` `WEBCHAT_BRIDGE_TOKEN`. Survives reboot via
the user manager (requires `loginctl enable-linger ubuntu`, same as the gateway).

## Config (ops/webchat-bridge/.env)

| var | meaning |
|---|---|
| `WEBCHAT_BRIDGE_TOKEN` | shared bearer token (must match backend) |
| `WEBCHAT_TG_TARGET` | operator Telegram chat id to mirror to (`""` disables) |
| `WEBCHAT_MODEL` | `default` = gateway default model; or an id allowed for the agent |
| `WEBCHAT_THINKING` | thinking level (`minimal` keeps it snappy) |
| `WEBCHAT_BRIDGE_PORT` | listen port (default 18791) |
| `WEBCHAT_TIMEOUT` | per-turn model timeout seconds |
| `WEBCHAT_MIRROR` | `1`/`0` toggle Telegram mirroring |

## API

`POST /chat` (header `X-Bridge-Token`) → `{prompt, sessionId, visitorMessage}` → `{reply, degraded?}`.
The backend owns the persona + prompt assembly; the bridge just runs it and mirrors.

`GET /health` → `{ok, model, mirror}`.

## Ops

```bash
systemctl --user status webchat-bridge
journalctl --user -u webchat-bridge -n 50
systemctl --user restart webchat-bridge     # after editing bridge.py or .env
```
