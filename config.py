import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_ENV = 'development'
    DATABASE_URL = os.environ.get('DATABASE_URL')
