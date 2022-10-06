class Config:
    """Set Flask configuration from .env file."""
    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://usman:poposikbuk1@localhost/testdb'
    UPLOAD_FOLDER = '/home/usmon/PythonProjects/wella/photos'
    SECRET_KEY = 'a23c36266d504b8d84e99bb58c150786'
