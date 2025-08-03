#!/usr/bin/env python3
"""Test production API endpoints."""

import requests
import json

def test_api_endpoints():
    base_url = "https://clinicalguru-36y53.ondigitalocean.app"
    
    endpoints = [
        "/healthz",
        "/api/healthz", 
        "/api/auth/login"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\n🧪 Testing: {url}")
            
            if endpoint == "/api/auth/login":
                # Test POST request for login
                data = {"email": "test@test.com", "password": "test"}
                response = requests.post(url, json=data, timeout=10)
            else:
                # Test GET request
                response = requests.get(url, timeout=10)
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_api_endpoints()
