from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

jwt = JWTManager()
db = SQLAlchemy()
hasher = Bcrypt()