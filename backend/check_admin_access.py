#!/usr/bin/env python3
"""
Alternative: Try to get admin/owner access information
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Try connecting with different privilege levels
connection_strings = [
    # Original connection
    os.getenv('DATABASE_URL'),
    
    # Try with different database roles
    f"postgresql://clinical_console:AVNS_tzTnBpgGSn7s9FjIeOn@astrobsmvelvet-db-do-user-23752526-0.e.db.ondigitalocean.com:25060/postgres?sslmode=require",
    
    # Try defaultdb (common DigitalOcean default)
    f"postgresql://clinical_console:AVNS_tzTnBpgGSn7s9FjIeOn@astrobsmvelvet-db-do-user-23752526-0.e.db.ondigitalocean.com:25060/defaultdb?sslmode=require"
]

for i, conn_str in enumerate(connection_strings):
    try:
        print(f"\\nTrying connection {i+1}...")
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        
        cursor.execute("SELECT current_user, current_database(), session_user;")
        current_user, current_db, session_user = cursor.fetchone()
        print(f"✓ Connected as: {current_user} to database: {current_db}")
        
        # Check privileges
        cursor.execute("""
            SELECT has_database_privilege(current_user, current_database(), 'CREATE'),
                   has_schema_privilege(current_user, 'public', 'CREATE');
        """)
        db_create, schema_create = cursor.fetchone()
        print(f"  Database CREATE privilege: {db_create}")
        print(f"  Schema CREATE privilege: {schema_create}")
        
        if schema_create:
            print("✅ This connection has CREATE privileges!")
            break
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Connection {i+1} failed: {e}")

print("\\n" + "="*50)
print("INSTRUCTIONS:")
print("1. Go to https://cloud.digitalocean.com/databases")
print("2. Click on your database 'astrobsmvelvet-db-do-user-23752526-0'")
print("3. Go to 'Users & Databases' tab")
print("4. Either grant SUPERUSER to 'clinical_console' or create a new admin user")
print("5. Use the Console tab to run the SQL from 'simplified_tables.sql'")
print("="*50)
