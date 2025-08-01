#!/usr/bin/env python3
"""Create admin user with specific credentials."""

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

def create_admin_user():
    """Create the specific admin user."""
    with app.app_context():
        # Get admin credentials from environment variables or use defaults
        admin_email = os.getenv('ADMIN_EMAIL', 'sylvia4douglas@gmail.com')
        admin_password = os.getenv('ADMIN_PASSWORD', 'natiss_natiss')
        admin_name = os.getenv('ADMIN_NAME', 'Sylvia Douglas')
        
        # Check if admin user already exists
        admin = User.query.filter_by(email=admin_email).first()
        if admin:
            print(f"Admin user {admin_email} already exists. Updating password...")
            # Update the password
            admin.password = generate_password_hash(admin_password)
            admin.role = 'admin'
            admin.name = admin_name
            admin.is_active = True
            db.session.commit()
            print("Admin user updated successfully!")
        else:
            print(f"Creating new admin user {admin_email}...")
            # Create new admin user
            admin = User(
                name=admin_name,
                email=admin_email,
                password=generate_password_hash(admin_password),
                role='admin',
                is_active=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        print(f"Admin credentials:")
        print(f"Email: {admin_email}")
        print(f"Role: admin")

if __name__ == '__main__':
    create_admin_user()
