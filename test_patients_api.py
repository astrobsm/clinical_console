import requests
import json

def test_api_endpoints():
    """Test the patients API endpoint"""
    
    base_url = "https://plasticunth-z2jbu.ondigitalocean.app"
    
    # Test without authentication first
    print("🔍 TESTING PATIENTS API ENDPOINT")
    print("=" * 50)
    
    try:
        # Test the patients endpoint
        response = requests.get(f"{base_url}/api/patients/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text[:500]}")
        
        if response.status_code == 401:
            print("✅ EXPECTED: API requires authentication (401 Unauthorized)")
        elif response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS: API returned {len(data)} patients")
                if len(data) > 0:
                    print(f"Sample patient: {data[0]}")
            except json.JSONDecodeError:
                print("❌ ERROR: Response is not valid JSON")
        else:
            print(f"❌ UNEXPECTED STATUS: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ NETWORK ERROR: {e}")
    
    # Test the health check endpoint if it exists
    try:
        response = requests.get(f"{base_url}/api/patients/health", timeout=10)
        print(f"\nHealth Check Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed")
    except:
        print("ℹ️  No health check endpoint")
    
    # Test the base API endpoint
    try:
        response = requests.get(f"{base_url}/api/", timeout=10)
        print(f"\nBase API Status: {response.status_code}")
        if response.status_code in [200, 404, 401]:
            print("✅ API server is responding")
    except:
        print("❌ API server not responding")

if __name__ == "__main__":
    test_api_endpoints()
