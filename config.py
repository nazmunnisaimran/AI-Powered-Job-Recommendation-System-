import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_ai_job_recommendation_system_123890!')
    
    # Database configuration: support MySQL and fall back to SQLite
    # Example MySQL connection string: mysql+pymysql://user:password@localhost/dbname
    mysql_host = os.environ.get('MYSQL_HOST')
    mysql_user = os.environ.get('MYSQL_USER')
    mysql_password = os.environ.get('MYSQL_PASSWORD')
    mysql_db = os.environ.get('MYSQL_DB')
    
    if mysql_host and mysql_user and mysql_db:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
    else:
        # Fallback to local SQLite file
        base_dir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'job_recommender.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload parameters
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {'pdf'}

    # Session lifetime configuration (30 days) for login stability
    from datetime import timedelta
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
