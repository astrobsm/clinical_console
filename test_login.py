#!/usr/bin/env python3
"""Test login endpoint specifically."""

import requests
import json

def test_login():
    url = "https://clinicalguru-36y53.ondigitalocean.app/api/auth/login"
    
    # Test data
    test_data = {
        "email": "admin@plasticunit.com",
        "password": "admin123"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"🧪 Testing LOGIN: {url}")
        print(f"📧 Data: {test_data}")
        
        response = requests.post(url, json=test_data, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_login()
