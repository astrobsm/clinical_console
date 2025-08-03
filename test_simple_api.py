#!/usr/bin/env python3
"""Test simple API endpoint."""

import requests

def test_simple_api():
    url = "https://clinicalguru-36y53.ondigitalocean.app/api/test"
    
    try:
        print(f"🧪 Testing SIMPLE API: {url}")
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_simple_api()
