import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class AppConfig:
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres.qfkcizyvmvolluzkqxqf:CdVAy16F9ej0lZS9@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_SECRET_KEY = "#@$@#$@#$@#$@#$@$#@#$@#$@#$@$##@$@#$%##^$^FDHFH#$^%$#W#"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=7)