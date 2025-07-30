# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app/backend
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh
ENV FLASK_APP=app.py
ENV PYTHONPATH=/app
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost:8080/healthz || exit 1
ENTRYPOINT ["./entrypoint.sh"]
