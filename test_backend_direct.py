#!/usr/bin/env python3
"""Test backend component directly."""

import requests

def test_backend_direct():
    # Try different possible backend URLs
    backend_urls = [
        "https://clinical-console-backend-xxxxx.ondigitalocean.app",  # Replace xxxxx
        "https://clinicalguru-36y53.ondigitalocean.app:8080",
        "https://clinicalguru-36y53.ondigitalocean.app/backend"
    ]
    
    for base_url in backend_urls:
        endpoints = ["/api/healthz", "/api/routes", "/api/auth/login"]
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                print(f"\n🧪 Testing: {url}")
                response = requests.get(url, timeout=5)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text[:100]}...")
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_backend_direct()
