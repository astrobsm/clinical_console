# Test script to run AFTER tables are created
python -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = conn.cursor()

# Check if tables exist
cursor.execute(\"SELECT tablename FROM pg_tables WHERE schemaname = 'public';\")
tables = [t[0] for t in cursor.fetchall()]
print(f'✓ Available tables: {tables}')

# Check users
if 'clinical_users' in tables:
    cursor.execute('SELECT email, role, name FROM clinical_users;')
    users = cursor.fetchall()
    print(f'✓ Users in database: {users}')
else:
    print('❌ No clinical_users table found')

cursor.close()
conn.close()
"

# Then test login
Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method POST -ContentType "application/json" -Body '{"email":"admin@plasticsurg.com","password":"admin123"}'
