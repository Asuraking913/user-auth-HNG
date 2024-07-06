from extensions import db
from uuid import uuid4

def create_id():
    return uuid4().hex

class Users(db.Model):
    userId = db.Column(db.String(255), unique = True, primary_key = True, default=create_id)
    firstName = db.Column(db.String(255), nullable = False)
    lastName = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(225), nullable = False)
    phone = db.Column(db.String(50))
    organisation = db.relationship('Organisation', backref='users')

    def __init__(self, firstname, lastname, email):
        self.firstName = firstname
        self.lastName = lastname
        self.email = email

class Organisation(db.Model):
    orgId = db.Column(db.String(255), unique = True, primary_key = True, default = create_id)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255))
    userId = db.Column(db.String(255), db.ForeignKey('users.userId'))

    def __init__(self, name, descp):
        self.name = name
        self.description = descp