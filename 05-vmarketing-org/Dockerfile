# =============================================================
# vMarketing Org — Dockerfile (Python 3.12 + TypeScript frontend)
# =============================================================

# ---- Stage 1: Build frontend (TypeScript -> JS) ----
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/tsconfig.json ./
RUN npm install --no-audit --no-fund
COPY frontend/src ./src
COPY frontend/scripts ./scripts
RUN npx tsc && node scripts/bundle.js

# ---- Stage 2: Python runtime ----
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY static ./static
COPY manifest.json .

# Copy bundled JS from frontend build
COPY --from=frontend-build /build/out/app.js ./static/app.js

ENV PYTHONPATH=/app

EXPOSE 8084

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8084"]
