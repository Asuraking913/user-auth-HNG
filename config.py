import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class AppConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=100)