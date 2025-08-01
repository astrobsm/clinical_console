#!/usr/bin/env python3
"""Initialize the database for local development."""

import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import app
from backend.database import db

def init_db():
    """Initialize the database."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")
        
        # Create an admin user if it doesn't exist
        from backend.models import User
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                name='Administrator',
                email='admin@example.com',
                role='admin',
                password='admin123'  # This should be hashed in a real app
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created (email: admin@example.com, password: admin123)")
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_db()
