# ── Stage 1 : build ──────────────────────────────────────────
FROM python:3.12-slim AS builder
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
 
# ── Stage 2 : runtime ────────────────────────────────────────
FROM python:3.12-slim
 
WORKDIR /app
 
# Copier les dépendances installées depuis le stage builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
 
# Copier le code applicatif
COPY app/ ./app/
COPY VERSION .
 
# Variable d'environnement — surchargée par k8s selon l'env
ENV APP_ENV=production
 
EXPOSE 8000
 
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
