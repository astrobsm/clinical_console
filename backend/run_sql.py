#!/usr/bin/env python3
"""
Run this script to execute the SQL commands using Python.
This will attempt to create tables with your current user permissions.
"""

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv('DATABASE_URL')

def execute_sql_file(filename):
    """Execute SQL commands from a file"""
    try:
        # Connect to database
        print(f"Connecting to database...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Read SQL file
        with open(filename, 'r') as file:
            sql_content = file.read()
        
        # Split into individual statements and execute
        statements = sql_content.split(';')
        
        for i, statement in enumerate(statements):
            statement = statement.strip()
            if statement:  # Skip empty statements
                try:
                    print(f"Executing statement {i+1}...")
                    cursor.execute(statement)
                    conn.commit()
                    print(f"✓ Statement {i+1} executed successfully")
                except psycopg2.Error as e:
                    print(f"✗ Error in statement {i+1}: {e}")
                    conn.rollback()
                    
        cursor.close()
        conn.close()
        print("✓ Database setup completed!")
        
    except Exception as e:
        print(f"✗ Database connection error: {e}")

if __name__ == "__main__":
    execute_sql_file('create_tables.sql')
