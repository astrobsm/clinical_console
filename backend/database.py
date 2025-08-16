from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def configure_ssl_engine(app):
    """
    Configure SQLAlchemy engine with SSL settings
    """
    from backend.ssl_config import create_ssl_engine
    
    try:
        # Create SSL-configured engine
        engine = create_ssl_engine()
        
        # Replace the default engine
        db.engine = engine
        
        print("Database engine configured with SSL")
        return True
    except Exception as e:
        print(f"Failed to configure SSL engine: {e}")
        return False
