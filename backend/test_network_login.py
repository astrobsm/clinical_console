#!/usr/bin/env python3
"""Test the login endpoint from network IP."""

import requests
import json

def test_network_login():
    """Test login with network IP."""
    url = "http://192.168.0.199:5000/api/auth/login"
    data = {
        "email": "sylvia4douglas@gmail.com",
        "password": "natiss_natiss"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Network login successful!")
            result = response.json()
            print(f"User: {result.get('user', {})}")
        else:
            print("❌ Network login failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_network_login()
