#!/usr/bin/env python3
"""
Debug script for production deployment issues
Add this temporarily to check what's happening in production
"""

import os
import sys
from flask import Flask, jsonify

def debug_production():
    """Debug function to check production environment"""
    debug_info = {
        'python_version': sys.version,
        'current_directory': os.getcwd(),
        'environment_variables': {
            'FLASK_ENV': os.getenv('FLASK_ENV'),
            'DATABASE_URL': 'SET' if os.getenv('DATABASE_URL') else 'NOT SET',
            'SECRET_KEY': 'SET' if os.getenv('SECRET_KEY') else 'NOT SET',
            'JWT_SECRET_KEY': 'SET' if os.getenv('JWT_SECRET_KEY') else 'NOT SET',
            'PORT': os.getenv('PORT'),
        },
        'files_in_directory': os.listdir('.'),
    }
    
    # Try database connection
    try:
        import psycopg2
        database_url = os.getenv('DATABASE_URL') or 'postgresql://clinical_console:AVNS_tzTnBpgGSn7s9FjIeOn@astrobsmvelvet-db-do-user-23752526-0.e.db.ondigitalocean.com:25060/plasticsurgunit_db?sslmode=require'
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute('SELECT current_user, current_database();')
        user, db = cursor.fetchone()
        cursor.close()
        conn.close()
        debug_info['database_connection'] = f'SUCCESS: {user}@{db}'
    except Exception as e:
        debug_info['database_connection'] = f'ERROR: {str(e)}'
    
    return debug_info

# Add this route temporarily to your app.py
def add_debug_route(app):
    @app.route('/api/debug', methods=['GET'])
    def debug_endpoint():
        return jsonify(debug_production())

if __name__ == '__main__':
    print("Debug info:")
    info = debug_production()
    for key, value in info.items():
        print(f"{key}: {value}")
