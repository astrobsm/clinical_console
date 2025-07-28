import pytest
from backend.models import db
from backend.app import app

from sqlalchemy import text

def test_db_connection():
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
        except Exception as e:
            pytest.fail(f'Database connection failed: {e}')
