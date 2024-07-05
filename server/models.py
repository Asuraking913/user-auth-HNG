from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

def create_id():
	return uuid4().hex

db = SQLAlchemy()

class Users(db.Model):
	id = db.Column(db.String(32), primary_key = True, unique = True, default = create_id)
	user_name = db.Column(db.String(40), unique= True, nullable = False)
	user_email = db.Column(db.String(345))
	user_pass = db.Column(db.String(50), unique = True, nullable = False)

	def __init__(self, name, pass_w):
		self.user_pass = pass_w
		self.user_name = name




