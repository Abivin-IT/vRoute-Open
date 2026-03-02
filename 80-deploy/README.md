# 80-deploy — Deployment Guide

## Environments

| Env | Branch | Domain | Method |
|-----|--------|--------|--------|
| **Local** | any | `localhost:8080` | `make up` |
| **Staging** | `staging` | `$STAGING_DOMAIN` | `make up-staging` |
| **Production** | `main` | `$PROD_DOMAIN` (primary) + aliases | Helm |

> Actual domains and server addresses are kept outside this repo.
> Set them as environment variables or pass via `--set` at deploy time.

## Architecture

```
Internet
  │
  ├─ $STAGING_DOMAIN ──→ Nginx (staging server) ──→ 127.0.0.1:8080
  │                    TLS via Let's Encrypt      Docker Compose
  │
  └─ $PROD_DOMAIN    ──→ K8s Ingress (nginx) ──→ vkernel Service
     $PROD_DOMAIN_2       cert-manager TLS       Helm chart (HA)
     $PROD_DOMAIN_3
```

## Local Development

```bash
make up          # start all services
make test        # run all tests
make down        # stop
```

## Staging

Single-server deployment using Docker Compose with a staging overlay.

```bash
# 1. SSH into staging server
ssh <staging-server>

# 2. Clone & switch to staging branch
git clone https://github.com/AbivinOrg/vRoute-Open.git
cd vRoute-Open
git checkout staging

# 3. Configure (NEVER commit .env)
cp .env.example .env
# Edit .env: DB_PASS, JWT_SECRET, OIDC keys, OIDC_REDIRECT_BASE

# 4. Start
make up-staging

# 5. Set up reverse proxy (Nginx/Caddy)
# See "Reverse Proxy" section below
```

### Reverse Proxy (Nginx)

Configure Nginx on the staging server to terminate TLS and proxy to Docker:

```nginx
server {
    listen 443 ssl http2;
    server_name staging.example.com;        # replace with $STAGING_DOMAIN

    ssl_certificate     /etc/letsencrypt/live/staging.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/staging.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (for future live events)
        proxy_http_version 1.1;
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

server {
    listen 80;
    server_name staging.example.com;
    return 301 https://$host$request_uri;
}
```

Obtain TLS cert:
```bash
certbot --nginx -d <STAGING_DOMAIN>
```

## Production (Kubernetes / Helm)

4-node cluster deployment with HA, auto-TLS via cert-manager.

```bash
# Install
helm upgrade --install vroute ./80-deploy/helm/vroute \
  -f ./80-deploy/helm/vroute/values-prod.yaml \
  --set ingress.host="$PROD_DOMAIN" \
  --set "ingress.extraHosts={$PROD_DOMAIN_2,$PROD_DOMAIN_3}" \
  --set postgresql.password="$DB_PASS" \
  --set vkernel.env.JWT_SECRET="$JWT_SECRET" \
  -n vroute --create-namespace

# Verify
kubectl -n vroute get pods
kubectl -n vroute get ingress

# Upgrade (after new image push)
helm upgrade vroute ./80-deploy/helm/vroute \
  -f ./80-deploy/helm/vroute/values-prod.yaml \
  --set ingress.host="$PROD_DOMAIN" \
  --set postgresql.password="$DB_PASS" \
  --set vkernel.env.JWT_SECRET="$JWT_SECRET" \
  -n vroute
```

## CI/CD Pipeline

```
push to staging  →  CI tests  →  push :staging images  →  deploy to staging server
push to main     →  CI tests  →  push :latest  images  →  deploy to prod cluster
```

Image tags (GHCR):
- `:staging`     — from `staging` branch
- `:latest`      — from `main` branch
- `:sha-abc1234` — every push (immutable, use for rollback)

## Secret Management

| Secret | Staging | Production |
|--------|---------|------------|
| `DB_PASS` | `.env` file on server | `helm --set` / Vault |
| `JWT_SECRET` | `.env` file (min 32 chars) | `helm --set` / Vault |
| OIDC client keys | `.env` file | K8s Secret / SOPS |
| `OIDC_REDIRECT_BASE` | `.env` file | `helm --set` |
| TLS certificate | Certbot (auto-renew) | cert-manager (auto) |
| Domain names | `.env` → `STAGING_DOMAIN` | `--set ingress.host` |

> **Rule**: This is an open-source repo. Never commit `.env`, secrets, IP
> addresses, domain names, or server hostnames. Use `.env` files (gitignored),
> `--set` flags, or an external secret manager (Vault, SOPS, sealed-secrets).

## File Layout

```
80-deploy/
├── docker-compose.yml           # Base (local dev)
├── docker-compose.staging.yml   # Staging overlay (single-server)
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
