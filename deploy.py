#!/usr/bin/env python3
"""
Simple deployment helper for DigitalOcean App Platform
"""

import os
import subprocess
import sys

def deploy_to_digitalocean():
    """Deploy the current code to DigitalOcean"""
    
    print("🚀 Deploying to DigitalOcean...")
    
    # Check if git is configured
    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Git repository not found. Make sure you're in the right directory.")
        return False
    
    try:
        # Add all changes
        print("📝 Adding changes...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        print("💾 Committing changes...")
        commit_message = "Fix production login issues and add debug endpoints"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Push to main branch (triggers DigitalOcean deployment)
        print("🔄 Pushing to main branch...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Deployment initiated!")
        print("🔗 Check your app at: https://clinicalguru-36y53.ondigitalocean.app")
        print("🔍 Debug info available at: https://clinicalguru-36y53.ondigitalocean.app/api/debug")
        print("⏱️  Deployment usually takes 2-5 minutes...")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_to_digitalocean()
