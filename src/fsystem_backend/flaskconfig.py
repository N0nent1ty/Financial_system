from pathlib import Path
import os
from .password_env import setPWDToEnv

basedir=Path(__file__).resolve().parents[1]
class CConfig():
    def __init__(self):
        setPWDToEnv()
        
        # Validate database configuration
        self.validate_db_config()
    
    def validate_db_config(self):
        """Validate that all required database configuration is present"""
        required_vars = [
            'POSTGRES_USER',
            'POSTGRES_PASSWORD',
            'POSTGRES_DB'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please check your password_env.py file and ensure all variables are set."
            )
    
    #SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = Path(basedir).joinpath("uploaded_images")
    API_TITLE ="Financial system API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_JSON_PATH=f"{Path(basedir).joinpath('openapi.json')}"
    OPENAPI_URL_PREFIX = '/doc'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_REDOC_PATH = '/redoc'
    # The following is equivalent to OPENAPI_SWAGGER_UI_VERSION = '3.19.5'
    OPENAPI_SWAGGER_UI_URL = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.19.5/'

    
    #Database setting
    DATABASE_NAME="financial_system.db"
    DATABASE_PATH=f"{basedir.joinpath(DATABASE_NAME)}"
    #SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(basedir).joinpath(DATABASE_NAME)}"
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    
    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # App configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')




    @staticmethod
    def init_app(app):
        pass
if __name__ =="__main__":
    print(basedir)