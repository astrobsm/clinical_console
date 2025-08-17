#!/usr/bin/env python3
"""
Debug Frontend Mixed Content Issue
"""
import requests
import json
import re

def debug_mixed_content():
    """Debug the mixed content issue by examining the frontend"""
    print("🔍 Debugging Frontend Mixed Content Issue")
    print("=" * 60)
    
    base_url = "https://clinicalguru-36y53.ondigitalocean.app"
    
    # Test 1: Check if frontend is accessible
    print("\n1. Testing Frontend Accessibility...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend accessible")
            
            # Check if there are any HTTP references in the HTML
            html_content = response.text
            http_matches = re.findall(r'http://[^"\'>\s]+', html_content)
            if http_matches:
                print(f"   ❌ Found HTTP URLs in HTML: {http_matches}")
            else:
                print("   ✅ No HTTP URLs found in HTML")
                
        else:
            print(f"   ❌ Frontend not accessible: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend test failed: {e}")
    
    # Test 2: Check main JavaScript bundle
    print("\n2. Testing JavaScript Bundle...")
    try:
        # Get the index.html to find the JS bundle
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            # Find main JS file references
            js_matches = re.findall(r'/static/js/[^"\'>\s]+\.js', response.text)
            if js_matches:
                for js_file in js_matches[:2]:  # Check first 2 JS files
                    js_url = f"{base_url}{js_file}"
                    print(f"   Checking: {js_file}")
                    
                    js_response = requests.get(js_url, timeout=10)
                    if js_response.status_code == 200:
                        js_content = js_response.text
                        
                        # Check for HTTP references
                        http_matches = re.findall(r'http://clinicalguru-36y53\.ondigitalocean\.app', js_content)
                        localhost_matches = re.findall(r'http://localhost:5000', js_content)
                        
                        if http_matches:
                            print(f"      ❌ Found HTTP clinicalguru URLs: {len(http_matches)} occurrences")
                        if localhost_matches:
                            print(f"      ❌ Found localhost:5000 URLs: {len(localhost_matches)} occurrences")
                        
                        if not http_matches and not localhost_matches:
                            print(f"      ✅ No problematic HTTP URLs found")
                    else:
                        print(f"      ❌ Could not fetch JS file: {js_response.status_code}")
            else:
                print("   ❌ No JS files found in HTML")
    except Exception as e:
        print(f"   ❌ JS bundle test failed: {e}")
    
    # Test 3: Test API endpoint directly
    print("\n3. Testing API Endpoint...")
    try:
        # First test login to get a token
        auth_data = {
            "username": "admin@plasticsurg.com",
            "password": "admin123"
        }
        auth_response = requests.post(f"{base_url}/api/auth/login", 
                                    json=auth_data, timeout=10)
        if auth_response.status_code == 200:
            token = auth_response.json().get('access_token')
            print("   ✅ Authentication successful")
            
            # Test patients endpoint
            headers = {'Authorization': f'Bearer {token}'}
            patients_response = requests.get(f"{base_url}/api/patients/", 
                                           headers=headers, timeout=10)
            print(f"   Patients API Status: {patients_response.status_code}")
            if patients_response.status_code == 200:
                print("   ✅ Patients API working correctly")
            else:
                print(f"   ❌ Patients API failed: {patients_response.text[:200]}")
        else:
            print(f"   ❌ Authentication failed: {auth_response.status_code}")
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
    
    # Test 4: Check for service worker issues
    print("\n4. Checking Service Worker...")
    try:
        sw_response = requests.get(f"{base_url}/service-worker.js", timeout=10)
        if sw_response.status_code == 200:
            sw_content = sw_response.text
            http_matches = re.findall(r'http://[^"\'>\s]+', sw_content)
            if http_matches:
                print(f"   ❌ Found HTTP URLs in service worker: {http_matches}")
            else:
                print("   ✅ Service worker clean of HTTP URLs")
        else:
            print(f"   ⚠️  Service worker not found: {sw_response.status_code}")
    except Exception as e:
        print(f"   ❌ Service worker test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 MIXED CONTENT DEBUG COMPLETE")
    print("\nRecommendations:")
    print("1. Check browser DevTools → Network tab for exact HTTP requests")
    print("2. Clear browser cache and hard refresh (Ctrl+Shift+R)")
    print("3. Check if service worker is caching old HTTP requests")
    print("4. Verify environment variables are properly set during build")
    print("=" * 60)

if __name__ == "__main__":
    debug_mixed_content()
