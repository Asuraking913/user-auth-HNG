from models import Users, Organisation
from extensions import db
from flask import request, jsonify

def root_route(app):

    def validator(data):
        error = []
        if data and data['firstname']:
            return error.append({
              "field": "First Name",
              "message": "The First Name value is invalid"
            },) 
             

        if data and data['lastname']:
            return error.append({
              "field": "Last Name",
              "message": "Last Name value is invalid"
            },) 
             
        
        if data and data['email']:
            return error.append({
              "field": "Email",
              "message": "The Email value is invalid"
            },) 
             
        
        if data and data['password']:
            return error.append({
              "field": "password",
              "message": "The password value is invalid"
            },) 
             

        if data and data['phone']:
            return error.append({
              "field": "phone",
              "message": "The phone value is invalid"
            },)
            

        

    @app.route("/auth/test")
    def test():
        return "Testing"

    @app.route("/auth/register", methods = ['POST'])
    def register():
        data = {
        "firstname" : request.json['firstName'],
        "lastname" : request.json['lastName'],
        "email" : request.json['email'],
        "password" : request.json['password'],
        "phone" : request.json['phone']
        }

        validator(data)

        return "Register"