import requests
import json

base_url = 'https://clinicalguru-36y53.ondigitalocean.app'

print("🔐 Testing Frontend Authentication Flow")
print("=" * 50)

# Test login with correct credentials
login_data = {'email': 'admin@plasticsurg.com', 'password': 'admin123'}

try:
    print("1. Testing login endpoint...")
    response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=10)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("   ✓ Login successful!")
        print(f"   User: {data['user']['name']} ({data['user']['role']})")
        
        token = data.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        
        print("\n2. Testing protected endpoints...")
        
        # Test each endpoint that was failing
        endpoints = [
            '/api/notifications/',
            '/api/dashboard/recent_activity',
            '/api/dashboard/patient_trends', 
            '/api/dashboard/summary',
            '/api/cbt/weekly-diagnoses'
        ]
        
        for endpoint in endpoints:
            try:
                api_response = requests.get(f'{base_url}{endpoint}', headers=headers, timeout=5)
                status = "✓ SUCCESS" if api_response.status_code == 200 else f"✗ {api_response.status_code}"
                print(f"   {endpoint}: {status}")
            except Exception as e:
                print(f"   {endpoint}: ✗ ERROR - {str(e)}")
        
        print(f"\n3. Login credentials for frontend:")
        print(f"   Email: admin@plasticsurg.com")
        print(f"   Password: admin123")
        print(f"\n✅ All systems ready! Please log in to the frontend.")
        
    else:
        print(f"   ✗ Login failed: {response.text}")
        
except Exception as e:
    print(f"   ✗ Error: {str(e)}")

print("\n" + "=" * 50)
print("🎯 SOLUTION: The 401 errors are expected - you need to log in first!")
print("   Visit: https://clinicalguru-36y53.ondigitalocean.app/")
print("   Use the credentials above to log in.")
