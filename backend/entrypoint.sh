#!/bin/sh
# Entrypoint script to run DB migrations and start the Flask app

echo "PATH at runtime: $PATH"
which flask
flask --version
python3 -m flask --version

# Run migrations
python3 -m flask db upgrade

# Set environment variables for Flask
export FLASK_APP=app.py
export FLASK_ENV=production
# Start the Flask server for maximum compatibility
exec python3 -m flask run --host=0.0.0.0 --port=8080
