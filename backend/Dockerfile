# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app/backend

# Copy only the necessary files first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application files
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONPATH=/app


# Add a healthcheck for the application
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --spider -q http://localhost:8080/healthz || exit 1

# Expose the Flask port
EXPOSE 8080

# Define the entrypoint
ENTRYPOINT ["./entrypoint.sh"]
