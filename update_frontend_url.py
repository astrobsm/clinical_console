#!/usr/bin/env python3
"""Update frontend with actual backend URL after deployment."""

backend_url = input("Enter your DigitalOcean backend URL: ")

# Update .env.production
with open('frontend/.env.production', 'w') as f:
    f.write(f"# Production Environment Variables\n")
    f.write(f"REACT_APP_API_BASE={backend_url}\n")

print(f"✅ Updated frontend/.env.production with: {backend_url}")
print("\n🔄 Next steps:")
print("1. cd frontend")
print("2. npm run build")
print("3. Deploy the new build to your frontend")
