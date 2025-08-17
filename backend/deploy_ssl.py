#!/usr/bin/env python3
"""
Deploy SSL Configuration to Production
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - Failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False

def deploy_ssl_configuration():
    """Deploy SSL configuration to production"""
    print("🔐 Deploying SSL Configuration to Production")
    print("=" * 60)
    
    # Check if we're in the right directory
    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(base_dir)
    
    print(f"Working directory: {os.getcwd()}")
    
    # Check SSL files exist
    ssl_files = [
        'backend/ca-certificate.crt',
        'backend/ssl_config.py',
        'backend/test_ssl_connection.py'
    ]
    
    print("\n1. Verifying SSL Files...")
    missing_files = []
    for file_path in ssl_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    # Git status
    print("\n2. Git Status...")
    run_command("git status --porcelain", "Checking git status")
    
    # Add SSL files
    print("\n3. Adding SSL Configuration Files...")
    commands = [
        ("git add backend/ca-certificate.crt", "Adding CA certificate"),
        ("git add backend/ssl_config.py", "Adding SSL configuration module"),
        ("git add backend/app.py", "Adding updated app configuration"),
        ("git add backend/database.py", "Adding enhanced database module"),
        ("git add backend/test_ssl_connection.py", "Adding SSL test script"),
        ("git add SSL_CONFIGURATION_COMPLETE.md", "Adding SSL documentation")
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n   Added {success_count}/{len(commands)} files successfully")
    
    # Commit changes
    print("\n4. Committing SSL Configuration...")
    commit_message = "feat: Add SSL database configuration with CA certificate\n\n- Added DigitalOcean CA certificate for secure database connections\n- Enhanced database configuration with SSL support\n- Added SSL status monitoring endpoint\n- Implemented comprehensive SSL verification\n- Production-ready HIPAA-compliant encryption"
    
    if run_command(f'git commit -m "{commit_message}"', "Committing SSL changes"):
        print("   ✅ SSL configuration committed successfully")
    else:
        print("   ⚠️  Commit may have failed or no changes to commit")
    
    # Push to production
    print("\n5. Deploying to Production...")
    if run_command("git push origin main", "Pushing to DigitalOcean"):
        print("   ✅ Deployment initiated successfully")
        print("   🚀 DigitalOcean will rebuild and deploy with SSL configuration")
    else:
        print("   ❌ Deployment failed")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 SSL CONFIGURATION DEPLOYMENT COMPLETE!")
    print("")
    print("📋 What's been deployed:")
    print("   🔐 CA Certificate for encrypted database connections")
    print("   ⚙️  Enhanced SSL configuration module")
    print("   📊 SSL status monitoring endpoint (/api/ssl-status)")
    print("   🧪 SSL connection verification tools")
    print("")
    print("🔗 Production URL: https://clinicalguru-36y53.ondigitalocean.app/")
    print("📊 SSL Status: https://clinicalguru-36y53.ondigitalocean.app/api/ssl-status")
    print("")
    print("⏱️  Deployment will be live in 2-3 minutes")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = deploy_ssl_configuration()
    sys.exit(0 if success else 1)
