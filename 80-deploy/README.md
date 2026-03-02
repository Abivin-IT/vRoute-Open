# 80-deploy — Deployment Guide

## Environments

| Env | Server | Branch | Domain | Method |
|-----|--------|--------|--------|--------|
| **Local** | localhost | any | `localhost:8080` | `make up` |
| **Staging** | cotest2026 | `staging` | `vroute-5.abivin.com.vn` | `make up-staging` |
| **Production** | 4-node cluster | `main` | `vroute-5.abivin.com` `.vn` `.sg` | Helm |

## Architecture

```
Internet
  │
  ├─ vroute-5.abivin.com.vn ──→ Nginx (cotest2026) ──→ 127.0.0.1:8080
  │                              TLS termination        Docker Compose
  │
  └─ vroute-5.abivin.com    ──→ K8s Ingress (nginx) ──→ vkernel Service
     vroute-5.abivin.vn          cert-manager TLS        Helm chart
     vroute-5.abivin.sg
```

## Local Development

```bash
make up          # start all services
make test        # run all tests
make down        # stop
```

## Staging (cotest2026)

Single-server deployment using Docker Compose with a staging overlay.

```bash
# 1. SSH into cotest2026
ssh cotest2026

# 2. Clone & switch to staging branch
git clone https://github.com/AbivinOrg/vRoute-Open.git
cd vRoute-Open
git checkout staging

# 3. Configure secrets (NEVER commit .env)
cp .env.example .env
# Edit .env:  DB_PASS, JWT_SECRET, OIDC keys

# 4. Start
make up-staging

# 5. Set up reverse proxy (Nginx/Caddy)
# See "Reverse Proxy" section below
```

### Reverse Proxy (Nginx)

On cotest2026, configure Nginx to terminate TLS and proxy to Docker:

```nginx
server {
    listen 443 ssl http2;
    server_name vroute-5.abivin.com.vn;

    ssl_certificate     /etc/letsencrypt/live/vroute-5.abivin.com.vn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vroute-5.abivin.com.vn/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (for future live events)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name vroute-5.abivin.com.vn;
    return 301 https://$host$request_uri;
}
```

## Production (Kubernetes / Helm)

4-node cluster deployment with HA, auto-TLS via cert-manager.

```bash
# Install
helm upgrade --install vroute ./80-deploy/helm/vroute \
  -f ./80-deploy/helm/vroute/values-prod.yaml \
  --set postgresql.password="$DB_PASS" \
  --set vkernel.env.JWT_SECRET="$JWT_SECRET" \
  -n vroute --create-namespace

# Verify
kubectl -n vroute get pods
kubectl -n vroute get ingress

# Upgrade (after new image push)
helm upgrade vroute ./80-deploy/helm/vroute \
  -f ./80-deploy/helm/vroute/values-prod.yaml \
  --set postgresql.password="$DB_PASS" \
  --set vkernel.env.JWT_SECRET="$JWT_SECRET" \
  -n vroute
```

## CI/CD Pipeline

```
push to staging  →  CI tests  →  push :staging images  →  deploy to cotest2026
push to main     →  CI tests  →  push :latest images   →  deploy to prod cluster
```

Image tags:
- `ghcr.io/abivin/vkernel:staging` — from `staging` branch
- `ghcr.io/abivin/vkernel:latest` — from `main` branch
- `ghcr.io/abivin/vkernel:sha-abc1234` — every push (immutable)

## Secret Management

| Secret | Where | How |
|--------|-------|-----|
| `DB_PASS` | .env (staging) / Helm `--set` (prod) | Never in repo |
| `JWT_SECRET` | .env (staging) / Helm `--set` (prod) | min 32 chars |
| OIDC keys | .env (staging) / K8s Secret (prod) | Per provider |
| TLS certs | Let's Encrypt (auto via certbot/cert-manager) | Auto-renewed |

> **IMPORTANT**: This is an open-source repo. Never commit secrets, `.env` files,
> private keys, or server credentials. Use `--set` flags, env vars, or external
> secret managers (Vault, SOPS, sealed-secrets).

## File Layout

```
80-deploy/
├── docker-compose.yml           # Base (local dev)
├── docker-compose.staging.yml   # Staging overlay (cotest2026)
├── README.md                    # This file
└── helm/vroute/
    ├── Chart.yaml
    ├── values.yaml              # Base defaults
    ├── values-staging.yaml      # Staging overrides
    ├── values-prod.yaml         # Production overrides
    └── templates/
        ├── deployment-vkernel.yaml
        ├── deployment-vstrategy.yaml
        ├── deployment-redis.yaml
        ├── statefulset-postgresql.yaml
        ├── services.yaml
        ├── ingress.yaml          # Multi-host (extraHosts)
        ├── secrets.yaml
        └── servicemonitor.yaml
```
