#!/usr/bin/env python3
"""
Comprehensive test script for the Clinical Console API endpoints.
Tests both authentication and core functionality.
"""

import requests
import json
import sys

class APITester:
    def __init__(self, base_url="https://clinicalguru-36y53.ondigitalocean.app"):
        self.base_url = base_url
        self.token = None
        self.headers = {}
        
    def login(self, email="admin@plasticsurg.com", password="admin123"):
        """Authenticate and get JWT token"""
        try:
            response = requests.post(f"{self.base_url}/api/auth/login", 
                json={'email': email, 'password': password}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data['access_token']
                self.headers = {'Authorization': f'Bearer {self.token}'}
                print(f"✓ Login successful! User: {data.get('user', {}).get('username', 'Unknown')}")
                return True
            else:
                print(f"✗ Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"✗ Login error: {e}")
            return False
    
    def test_endpoint(self, endpoint, method="GET", data=None):
        """Test a specific API endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)
            else:
                response = requests.request(method, url, headers=self.headers, json=data, timeout=10)
            
            status = "✓ SUCCESS" if response.status_code < 400 else "✗ FAILED"
            print(f"   {endpoint}: {status} ({response.status_code})")
            
            if response.status_code >= 400:
                print(f"     Error: {response.text[:200]}")
                
            return response.status_code < 400
            
        except Exception as e:
            print(f"   {endpoint}: ✗ ERROR - {e}")
            return False
    
    def test_mixed_content(self):
        """Test for mixed content issues in frontend"""
        try:
            # Test main page
            response = requests.get(self.base_url, timeout=10)
            if response.status_code == 200:
                content = response.text
                
                # Check for HTTP references in HTML
                import re
                http_refs = re.findall(r'http://[^"\s]+', content)
                if http_refs:
                    print(f"⚠ Found {len(http_refs)} HTTP references in HTML")
                    for ref in http_refs[:3]:
                        print(f"   - {ref}")
                    return False
                else:
                    print("✓ No HTTP references found in HTML")
                
                # Check JavaScript for API base
                js_pattern = r'static/js/main\.[a-f0-9]+\.js'
                js_match = re.search(js_pattern, content)
                if js_match:
                    js_url = f"{self.base_url}/{js_match.group()}"
                    js_response = requests.get(js_url, timeout=10)
                    js_content = js_response.text
                    
                    https_refs = len(re.findall(r'https://clinicalguru-36y53\.ondigitalocean\.app', js_content))
                    http_refs = len(re.findall(r'http://clinicalguru-36y53\.ondigitalocean\.app', js_content))
                    
                    print(f"✓ JavaScript HTTPS API refs: {https_refs}")
                    if http_refs > 0:
                        print(f"⚠ JavaScript HTTP API refs: {http_refs}")
                        return False
                    else:
                        print("✓ No HTTP API references in JavaScript")
                
                return True
            else:
                print(f"✗ Frontend not accessible: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Mixed content test error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🔐 Clinical Console API & Frontend Test")
        print("=" * 50)
        
        # Test 1: Authentication
        if not self.login():
            print("❌ Authentication failed - cannot continue")
            return False
        
        # Test 2: Mixed Content Check
        print("\n📱 Testing Frontend Mixed Content...")
        mixed_content_ok = self.test_mixed_content()
        
        # Test 3: Core API Endpoints
        print("\n🏥 Testing Core API Endpoints...")
        endpoints = [
            "/api/patients/",
            "/api/patients/health",
            "/api/notifications/",
            "/api/dashboard/summary",
            "/api/dashboard/recent_activity",
            "/api/dashboard/patient_trends",
            "/api/cbt/weekly-diagnoses",
            "/api/academic-events/",
            "/api/assessments/",
            "/api/scores/",
            "/api/discharges/",
            "/api/discharge-summaries/"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            if self.test_endpoint(endpoint):
                success_count += 1
        
        # Test 4: Database Health Check
        print("\n💾 Testing Database Connectivity...")
        db_ok = self.test_endpoint("/api/patients/health")
        
        # Summary
        print(f"\n📊 Test Summary:")
        print(f"   API Endpoints: {success_count}/{len(endpoints)} working")
        print(f"   Mixed Content: {'✓ Resolved' if mixed_content_ok else '✗ Issues found'}")
        print(f"   Database: {'✓ Connected' if db_ok else '✗ Issues'}")
        
        overall_success = success_count == len(endpoints) and mixed_content_ok and db_ok
        
        if overall_success:
            print("\n🎉 ALL TESTS PASSED! System is ready for production.")
        else:
            print("\n⚠ Some issues found. Check the details above.")
            
        return overall_success

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)
