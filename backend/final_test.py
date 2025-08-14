import requests
import json

base_url = 'https://clinicalguru-36y53.ondigitalocean.app'

# Test login to get token
login_data = {'email': 'sylvia4douglas@gmail.com', 'password': 'natiss_natiss'}
try:
    login_response = requests.post(f'{base_url}/api/auth/login', json=login_data, timeout=10)
    if login_response.status_code == 200:
        token = login_response.json().get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        
        endpoints = [
            '/api/patients',
            '/api/discharges', 
            '/api/assessments',
            '/api/notifications',
            '/api/dashboard/summary',
            '/api/academic-events'
        ]
        
        print('Testing API endpoints with HTTPS:')
        success_count = 0
        for endpoint in endpoints:
            try:
                response = requests.get(f'{base_url}{endpoint}', headers=headers, timeout=5)
                status = 'SUCCESS' if response.status_code == 200 else 'FAILED'
                print(f'{endpoint}: {response.status_code} - {status}')
                if response.status_code == 200:
                    success_count += 1
            except Exception as e:
                print(f'{endpoint}: ERROR - {str(e)}')
        
        print(f'\nAPI Success Rate: {success_count}/{len(endpoints)} ({100*success_count/len(endpoints):.0f}%)')
        
        # Test frontend accessibility
        try:
            frontend_response = requests.get(f'{base_url}/', timeout=5)
            status = 'SUCCESS' if frontend_response.status_code == 200 else 'FAILED'
            print(f'Frontend: {frontend_response.status_code} - {status}')
            
            # Check if the response contains our React app
            if 'Clinical Console' in frontend_response.text:
                print('Frontend: React app detected successfully')
            else:
                print('Frontend: Warning - React app not detected in response')
                
        except Exception as e:
            print(f'Frontend: ERROR - {str(e)}')
    else:
        print(f'Login failed: {login_response.status_code}')
        print(f'Response: {login_response.text}')
except Exception as e:
    print(f'Login error: {str(e)}')
