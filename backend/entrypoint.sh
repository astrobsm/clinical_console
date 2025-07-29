#!/bin/sh
# Entrypoint script to run DB migrations and start the Flask app

# Run migrations
flask db upgrade

# Start the Flask server
exec flask run --host=0.0.0.0
