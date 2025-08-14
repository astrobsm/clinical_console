import requests

base_url = 'https://clinicalguru-36y53.ondigitalocean.app'

# Check debug endpoint
try:
    response = requests.get(f'{base_url}/debug/models', timeout=10)
    print(f'Debug endpoint: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print('User table info:')
        print(f"User count: {data.get('User', {}).get('count', 'N/A')}")
        
        # If no users, let's try to create admin
        if data.get('User', {}).get('count', 0) == 0:
            print('No users found, need to create admin')
        else:
            print('Users exist, trying login with different credentials')
            
    else:
        print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {str(e)}')

# Test basic connectivity
try:
    frontend_response = requests.get(f'{base_url}/', timeout=5)
    print(f'Frontend accessibility: {frontend_response.status_code}')
    if 'Clinical Console' in frontend_response.text:
        print('✓ Frontend is serving React app correctly')
    else:
        print('⚠ Frontend may not be serving React app')
except Exception as e:
    print(f'Frontend error: {str(e)}')
