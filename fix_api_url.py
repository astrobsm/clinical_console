#!/usr/bin/env python3
"""Quick fix to update frontend API URL for production."""

def update_frontend_api():
    backend_url = input("Enter your DigitalOcean backend URL (e.g., https://clinical-console-backend-xxxxx.ondigitalocean.app): ")
    
    # Update .env.production
    with open('frontend/.env.production', 'w') as f:
        f.write(f"# Production Environment Variables\n")
        f.write(f"REACT_APP_API_BASE={backend_url}\n")
    
    print(f"✅ Updated frontend/.env.production with: {backend_url}")
    print("\n🔄 Next steps:")
    print("1. cd frontend")
    print("2. npm run build")
    print("3. Copy build to backend: Copy-Item -Recurse build ../backend/frontend_build -Force")
    print("4. Your app will now use the DigitalOcean backend!")

if __name__ == '__main__':
    update_frontend_api()
