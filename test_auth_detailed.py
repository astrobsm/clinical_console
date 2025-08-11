#!/usr/bin/env python3
"""Test auth route with detailed error info."""

import requests
import json

def test_auth_detailed():
    url = "https://clinicalguru-36y53.ondigitalocean.app/api/auth/login"
    
    # Test data
    test_data = {
        "email": "test@test.com",
        "password": "test123"
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        print(f"🧪 Testing AUTH with detailed error: {url}")
        print(f"📧 Data: {test_data}")
        
        response = requests.post(url, json=test_data, headers=headers, timeout=15)
        
        print(f"Status: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        # Try to parse as JSON
        try:
            json_response = response.json()
            print(f"JSON Response: {json_response}")
        except:
            print("Response is not JSON")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    test_auth_detailed()
