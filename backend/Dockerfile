# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh
ENV FLASK_APP=app.py
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost:5000/healthz || exit 1
ENTRYPOINT ["./entrypoint.sh"]
