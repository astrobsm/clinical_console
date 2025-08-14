#!/usr/bin/env python3
"""Test the login endpoint"""

import requests
import json

try:
    response = requests.post(
        'http://localhost:8080/api/auth/login',
        headers={'Content-Type': 'application/json'},
        json={'email': 'admin@plasticsurg.com', 'password': 'admin123'}
    )
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')
    
    if response.status_code == 200:
        data = response.json()
        print('✅ LOGIN SUCCESSFUL!')
        print(f'Access Token: {data.get("access_token", "N/A")[:50]}...')
        print(f'User: {data.get("user", {})}')
    else:
        print(f'❌ Login failed: {response.text}')
        
except Exception as e:
    print(f'❌ Error: {e}')
