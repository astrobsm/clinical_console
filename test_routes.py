#!/usr/bin/env python3
"""Test all routes endpoint."""

import requests

def test_routes():
    url = "https://clinicalguru-36y53.ondigitalocean.app/api/routes"
    
    try:
        print(f"🧪 Testing ROUTES: {url}")
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_routes()
