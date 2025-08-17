import requests
import json

def test_clinical_console():
    base_url = "https://clinicalguru-36y53.ondigitalocean.app"
    
    print("🏥 Clinical Console - Final System Verification")
    print("=" * 60)
    
    # Test 1: Frontend accessibility
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend: Accessible and serving content")
        else:
            print(f"❌ Frontend: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")
    
    # Test 2: API Health Check
    try:
        response = requests.get(f"{base_url}/api/healthz", timeout=10)
        if response.status_code == 200:
            print("✅ API Health: Backend responding")
            data = response.json()
            print(f"   Database: {data.get('database', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
        else:
            print(f"❌ API Health: Status {response.status_code}")
    except Exception as e:
        print(f"❌ API Health: Error - {e}")
    
    # Test 3: Authentication Endpoint
    try:
        auth_data = {
            "username": "admin@plasticsurg.com",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/api/auth/login", 
                               json=auth_data, 
                               timeout=10)
        if response.status_code == 200:
            print("✅ Authentication: Login working")
            token = response.json().get('access_token')
            if token:
                print("   JWT Token: Generated successfully")
            else:
                print("   JWT Token: Missing in response")
        else:
            print(f"❌ Authentication: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Authentication: Error - {e}")
    
    # Test 4: Patients Endpoint (previously problematic)
    try:
        # First get auth token
        auth_response = requests.post(f"{base_url}/api/auth/login", 
                                    json={"username": "admin@plasticsurg.com", "password": "admin123"})
        if auth_response.status_code == 200:
            token = auth_response.json().get('access_token')
            headers = {'Authorization': f'Bearer {token}'}
            
            # Test patients endpoint
            response = requests.get(f"{base_url}/api/patients/", headers=headers, timeout=10)
            if response.status_code == 200:
                print("✅ Patients API: Working correctly")
                patients = response.json()
                print(f"   Patients count: {len(patients) if isinstance(patients, list) else 'N/A'}")
            else:
                print(f"❌ Patients API: Status {response.status_code}")
        else:
            print("❌ Patients API: Auth failed, cannot test")
    except Exception as e:
        print(f"❌ Patients API: Error - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 VERIFICATION COMPLETE")
    print("📱 Frontend URL: https://clinicalguru-36y53.ondigitalocean.app/")
    print("🔐 Admin Login: admin@plasticsurg.com / admin123")
    print("=" * 60)

if __name__ == "__main__":
    test_clinical_console()
