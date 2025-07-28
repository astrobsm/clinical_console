import pytest
from backend.app import app

endpoints = [
    '/api/auth/login',
    '/api/auth/register',
    '/api/auth/users?role=consultant',
    '/api/patients/',
    '/api/notifications/',
    '/api/academic-events/',
    # Add more endpoints as needed
]

def test_endpoints_status():
    client = app.test_client()
    for url in endpoints:
        resp = client.get(url)
        assert resp.status_code in (200, 401, 403, 404)  # Acceptable for protected endpoints
