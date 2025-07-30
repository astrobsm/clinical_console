#!/bin/sh
# Entrypoint script to run DB migrations and start the Flask app

# Run migrations
python3 -m flask db upgrade

# Start the Flask server with correct app import
exec python3 -m flask run --app backend.app:app --host=0.0.0.0 --port=8080
