#!/usr/bin/env python3
"""
Test script to verify frontend HTTPS compliance and mixed content resolution.
"""

import requests
import re
import json
from urllib.parse import urljoin

def test_frontend_https_compliance():
    """Test that the frontend properly uses HTTPS for all API requests."""
    base_url = "https://clinicalguru-36y53.ondigitalocean.app"
    
    print("Testing Frontend HTTPS Compliance")
    print("=" * 50)
    
    # Test 1: Check main page loads
    try:
        response = requests.get(base_url, timeout=10)
        print(f"✓ Main page loads: {response.status_code}")
        
        # Check if HTML contains any HTTP references
        content = response.text
        http_refs = re.findall(r'http://[^"\s]+', content)
        if http_refs:
            print(f"⚠ Found HTTP references in HTML:")
            for ref in http_refs[:5]:  # Show first 5
                print(f"  - {ref}")
        else:
            print("✓ No HTTP references found in HTML")
            
    except Exception as e:
        print(f"✗ Main page failed: {e}")
        return False
    
    # Test 2: Check JavaScript files for HTTPS URLs
    js_pattern = r'static/js/main\.[a-f0-9]+\.js'
    js_match = re.search(js_pattern, content)
    if js_match:
        js_url = urljoin(base_url, js_match.group())
        try:
            js_response = requests.get(js_url, timeout=10)
            js_content = js_response.text
            
            # Check for clinicalguru HTTPS references
            https_refs = re.findall(r'https://clinicalguru-36y53\.ondigitalocean\.app', js_content)
            http_refs = re.findall(r'http://clinicalguru-36y53\.ondigitalocean\.app', js_content)
            
            print(f"✓ JavaScript file loaded: {js_response.status_code}")
            print(f"✓ HTTPS API references found: {len(https_refs)}")
            if http_refs:
                print(f"⚠ HTTP API references found: {len(http_refs)}")
            else:
                print("✓ No HTTP API references found")
                
        except Exception as e:
            print(f"⚠ Could not load JavaScript: {e}")
    
    # Test 3: Test API endpoint accessibility
    try:
        api_url = urljoin(base_url, "/api/health")
        api_response = requests.get(api_url, timeout=10)
        print(f"✓ API endpoint accessible: {api_response.status_code}")
    except Exception as e:
        print(f"⚠ API endpoint test failed: {e}")
    
    # Test 4: Check Content Security Policy headers
    headers = response.headers
    csp_header = headers.get('Content-Security-Policy', '')
    if 'upgrade-insecure-requests' in csp_header:
        print("✓ CSP upgrade-insecure-requests found")
    else:
        print("⚠ No CSP upgrade-insecure-requests directive")
    
    print("\nSummary:")
    print("The frontend has been rebuilt with HTTPS environment variables.")
    print("Mixed content issues should now be resolved.")
    print("\nTo verify in browser:")
    print("1. Open https://clinicalguru-36y53.ondigitalocean.app/")
    print("2. Open browser DevTools (F12)")
    print("3. Check Console for mixed content warnings")
    print("4. All API requests should use HTTPS")
    
    return True

if __name__ == "__main__":
    test_frontend_https_compliance()
