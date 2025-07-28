import pytest
from backend.app import app

def test_root():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code in (200, 404)

# Add more endpoint tests as needed
