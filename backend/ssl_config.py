"""
SSL Configuration for PostgreSQL Database Connection
"""
import os
import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def get_ssl_database_url():
    """
    Create a database URL with proper SSL configuration using the CA certificate
    """
    base_url = os.getenv('DATABASE_URL')
    
    if not base_url:
        # Fallback for production environment
        base_url = 'postgresql://clinical_console:AVNS_tzTnBpgGSn7s9FjIeOn@astrobsmvelvet-db-do-user-23752526-0.e.db.ondigitalocean.com:25060/plasticsurgunit_db'
    
    # Get the directory where this script is located (backend directory)
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    ca_cert_path = os.path.join(backend_dir, 'ca-certificate.crt')
    
    # Check if CA certificate exists
    if os.path.exists(ca_cert_path):
        logger.info(f"Using SSL CA certificate: {ca_cert_path}")
        
        # Remove existing sslmode parameter if present
        if '?sslmode=' in base_url:
            base_url = base_url.split('?sslmode=')[0]
        elif '&sslmode=' in base_url:
            parts = base_url.split('&sslmode=')
            base_url = parts[0] + '&'.join(parts[1:]).split('&', 1)[1] if '&' in parts[1] else parts[0]
        
        # Add SSL parameters with CA certificate
        ssl_params = f"sslmode=require&sslrootcert={ca_cert_path}"
        
        # Add SSL parameters to URL
        if '?' in base_url:
            database_url = f"{base_url}&{ssl_params}"
        else:
            database_url = f"{base_url}?{ssl_params}"
            
        logger.info("Database URL configured with SSL certificate")
        return database_url
    else:
        logger.warning(f"CA certificate not found at {ca_cert_path}, using basic SSL mode")
        
        # Ensure basic SSL is enabled if no certificate
        if 'sslmode=' not in base_url:
            if '?' in base_url:
                return f"{base_url}&sslmode=require"
            else:
                return f"{base_url}?sslmode=require"
        
        return base_url

def create_ssl_engine():
    """
    Create a SQLAlchemy engine with SSL configuration
    """
    database_url = get_ssl_database_url()
    
    # Additional SSL connection arguments for SQLAlchemy
    connect_args = {}
    
    # Get CA certificate path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    ca_cert_path = os.path.join(backend_dir, 'ca-certificate.crt')
    
    if os.path.exists(ca_cert_path):
        connect_args = {
            'sslmode': 'require',
            'sslrootcert': ca_cert_path
        }
        logger.info("Engine configured with SSL certificate")
    else:
        connect_args = {
            'sslmode': 'require'
        }
        logger.info("Engine configured with basic SSL")
    
    return create_engine(
        database_url,
        connect_args=connect_args,
        pool_pre_ping=True,  # Validate connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        echo=False           # Set to True for SQL debugging
    )

def verify_ssl_connection():
    """
    Verify that SSL connection is working properly
    """
    try:
        engine = create_ssl_engine()
        with engine.connect() as conn:
            result = conn.execute("SELECT version()")
            version = result.fetchone()[0]
            logger.info(f"SSL Database connection successful. PostgreSQL version: {version}")
            return True
    except Exception as e:
        logger.error(f"SSL Database connection failed: {e}")
        return False

def get_ssl_status():
    """
    Get detailed SSL connection status
    """
    try:
        engine = create_ssl_engine()
        with engine.connect() as conn:
            # Check SSL status
            result = conn.execute("SELECT ssl_is_used()")
            ssl_used = result.fetchone()[0]
            
            # Get connection info
            result = conn.execute("SELECT inet_server_addr(), inet_server_port()")
            server_info = result.fetchone()
            
            return {
                'ssl_enabled': ssl_used,
                'server_address': server_info[0] if server_info else None,
                'server_port': server_info[1] if server_info else None,
                'ca_certificate_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ca-certificate.crt'),
                'certificate_exists': os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ca-certificate.crt'))
            }
    except Exception as e:
        logger.error(f"Failed to get SSL status: {e}")
        return {
            'ssl_enabled': False,
            'error': str(e),
            'ca_certificate_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ca-certificate.crt'),
            'certificate_exists': os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ca-certificate.crt'))
        }
