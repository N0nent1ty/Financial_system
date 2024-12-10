import sys
sys.path.append("..")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from psycopg2 import OperationalError
from password_env import setPWDToEnv
def test_postgresql_connection(host='localhost', 
                             database='your_database',
                             user='your_username',
                             password='your_password',
                             port='5432'):
    """
    Test PostgreSQL connection and return connection status
    Returns tuple: (bool, str) - (success status, message)
    """
    try:
        # Attempt to create a connection
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        
        # Get cursor and PostgreSQL version to verify connection
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        
        return True, f"Successfully connected to PostgreSQL. Version: {version[0]}"
        
    except OperationalError as e:
        return False, f"Error connecting to PostgreSQL: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

# Example usage in Flask app
app = Flask(__name__)

@app.route('/test-db')
def test_db():
    host='localhost'
    database=os.getenv('POSTGRES_DB')  # Replace with your database name
    user=os.getenv('POSTGRES_USER')      # Replace with your username
    password=os.getenv('POSTGRES_PASSWORD')  # Replace with your password
    port=os.getenv('POSTGRES_PORT', '5432')   # Replace with your port if different

    success, message = test_postgresql_connection(
        host=host,
        database=database,  # Replace with your database name
        user=user,      # Replace with your username
        password=password,  # Replace with your password
        port=port   # Replace with your port if different
    )
    


    return {
        'success': success,
        'message': message
    }

if __name__ == '__main__':
    # Test connection directly when running the script

    setPWDToEnv()
    host='localhost'
    database=os.getenv('POSTGRES_DB')  # Replace with your database name
    user=os.getenv('POSTGRES_USER')      # Replace with your username
    password=os.getenv('POSTGRES_PASSWORD')  # Replace with your password
    port=os.getenv('POSTGRES_PORT', '5432')   # Replace with your port if different
    print(f"host:{host}, user: {user}, password: {password}, port: {port}")
    success, message = test_postgresql_connection(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    print(message)