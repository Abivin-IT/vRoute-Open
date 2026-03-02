# =============================================================
# vFinacc — Dockerfile (Python 3.12 + TypeScript frontend)
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

# Install dependencies (includes grpcio-tools for proto compilation)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Generate Python gRPC stubs from proto (Step 6: IPC)
COPY protos ./protos
RUN mkdir -p app/grpc && \
    python -m grpc_tools.protoc \
        -I./protos \
        --python_out=app/grpc \
        --grpc_python_out=app/grpc \
        protos/kernel.proto && \
    touch app/grpc/__init__.py

# Copy static assets (HTML + bundled JS from frontend build)
COPY static ./static
COPY --from=frontend-build /build/out/app.js ./static/app.js

# Copy manifest
COPY manifest.json .

ENV PYTHONPATH=/app

EXPOSE 8082

# Run: Alembic migrate + Uvicorn
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8082"]
