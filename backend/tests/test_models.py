import pytest
from backend.models import User

def test_user_model():
    user = User(name='Test', email='test@example.com', password='pw', role='admin')
    assert user.name == 'Test'
    assert user.email == 'test@example.com'
