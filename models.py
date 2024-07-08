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

class Organisation(db.Model):
    orgId = db.Column(db.String(255), unique = True, primary_key = True, default = create_id)
    name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255))
    userId = db.Column(db.String(255), db.ForeignKey('users.userId'))

class UserOrganization(db.Model):
    __tablename__ = 'user_organization'
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), primary_key=True)
    orgId = db.Column(db.Integer, db.ForeignKey('organisation.orgId'), primary_key=True)
    db.UniqueConstraint('userId', 'orgId', name='unique_user_organisation')