#!/usr/bin/env python3
"""Initialize database for production deployment."""

import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import app
from backend.database import db
from backend.models import User
from werkzeug.security import generate_password_hash

def init_production_db():
    """Initialize database and create admin user for production."""
    try:
        with app.app_context():
            print("Initializing production database...")
            
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Get admin credentials from environment variables
            admin_email = os.getenv('ADMIN_EMAIL', 'sylvia4douglas@gmail.com')
            admin_password = os.getenv('ADMIN_PASSWORD', 'natiss_natiss')
            admin_name = os.getenv('ADMIN_NAME', 'Sylvia Douglas')
            
            # Check if admin user already exists
            admin = User.query.filter_by(email=admin_email).first()
            if admin:
                print(f"Admin user {admin_email} already exists. Updating...")
                admin.password = generate_password_hash(admin_password)
                admin.role = 'admin'
                admin.name = admin_name
                admin.is_active = True
            else:
                print(f"Creating admin user {admin_email}...")
                admin = User(
                    name=admin_name,
                    email=admin_email,
                    password=generate_password_hash(admin_password),
                    role='admin',
                    is_active=True
                )
                db.session.add(admin)
            
            db.session.commit()
            print("✅ Admin user ready!")
            print(f"Email: {admin_email}")
            print(f"Role: admin")
            
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    init_production_db()
