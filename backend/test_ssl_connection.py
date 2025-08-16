#!/usr/bin/env python3
"""
SSL Database Connection Test
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Load environment variables
load_dotenv('.env')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ssl_connection():
    """Test SSL database connection"""
    print("🔐 SSL Database Connection Test")
    print("=" * 50)
    
    try:
        from ssl_config import verify_ssl_connection, get_ssl_status, get_ssl_database_url
        
        # Test 1: Check SSL configuration
        print("\n1. Checking SSL Configuration...")
        database_url = get_ssl_database_url()
        print(f"   Database URL: {database_url[:50]}...")
        
        # Test 2: Verify CA certificate
        ca_cert_path = os.path.join(current_dir, 'ca-certificate.crt')
        if os.path.exists(ca_cert_path):
            print(f"   ✅ CA Certificate found: {ca_cert_path}")
            
            # Get certificate info
            with open(ca_cert_path, 'r') as f:
                cert_content = f.read()
                if '-----BEGIN CERTIFICATE-----' in cert_content:
                    print(f"   ✅ CA Certificate format: Valid PEM format")
                else:
                    print(f"   ❌ CA Certificate format: Invalid format")
        else:
            print(f"   ❌ CA Certificate not found: {ca_cert_path}")
        
        # Test 3: Test SSL connection
        print("\n2. Testing SSL Connection...")
        ssl_working = verify_ssl_connection()
        if ssl_working:
            print("   ✅ SSL connection successful")
        else:
            print("   ❌ SSL connection failed")
        
        # Test 4: Get detailed SSL status
        print("\n3. SSL Connection Details...")
        ssl_status = get_ssl_status()
        
        for key, value in ssl_status.items():
            if key == 'ssl_enabled':
                status = "✅ Enabled" if value else "❌ Disabled"
                print(f"   SSL Status: {status}")
            elif key == 'certificate_exists':
                status = "✅ Found" if value else "❌ Missing"
                print(f"   Certificate: {status}")
            elif key == 'error':
                print(f"   Error: {value}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Test 5: Test with psycopg2 directly
        print("\n4. Testing Direct psycopg2 Connection...")
        try:
            import psycopg2
            
            # Get connection parameters
            if os.path.exists(ca_cert_path):
                conn = psycopg2.connect(
                    host='astrobsmvelvet-db-do-user-23752526-0.e.db.ondigitalocean.com',
                    port=25060,
                    database='plasticsurgunit_db',
                    user='clinical_console',
                    password='AVNS_tzTnBpgGSn7s9FjIeOn',
                    sslmode='require',
                    sslrootcert=ca_cert_path
                )
            else:
                conn = psycopg2.connect(database_url)
            
            with conn.cursor() as cur:
                # Check SSL status
                cur.execute("SELECT ssl_is_used();")
                ssl_used = cur.fetchone()[0]
                print(f"   ✅ Direct connection SSL status: {'Enabled' if ssl_used else 'Disabled'}")
                
                # Get version
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"   PostgreSQL Version: {version.split(',')[0]}")
                
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Direct connection failed: {e}")
        
        print("\n" + "=" * 50)
        if ssl_working:
            print("🎉 SSL Configuration: SUCCESS")
        else:
            print("❌ SSL Configuration: FAILED")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ssl_connection()
