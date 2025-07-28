import os
from flask import Flask
from werkzeug.security import generate_password_hash
from models import db, User
from app import create_app

ADMIN_EMAIL = "sylvia4douglas@gmail.com"
ADMIN_PASSWORD = "natiss_natiss"
ADMIN_ROLE = "admin"
ADMIN_NAME = "Admin User"

def create_admin():
    app = create_app()
    with app.app_context():
        if User.query.filter_by(email=ADMIN_EMAIL).first():
            print("Admin user already exists.")
            return
        hashed_password = generate_password_hash(ADMIN_PASSWORD)
        admin = User(name=ADMIN_NAME, email=ADMIN_EMAIL, password=hashed_password, role=ADMIN_ROLE)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")

if __name__ == "__main__":
    create_admin()
