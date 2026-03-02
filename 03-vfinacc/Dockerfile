# =============================================================
# vFinacc — Dockerfile (Python 3.12, single-stage)
# No TypeScript frontend — uses plain static/index.html.
# gRPC stubs are imported lazily; grpc_client.py degrades gracefully
# if vKernel stubs are not present.
# =============================================================
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY static ./static
COPY manifest.json .

ENV PYTHONPATH=/app

EXPOSE 8082

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8082"]
