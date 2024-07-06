from models import Users, Organisation
from extensions import db
from flask import request, jsonify
from extensions import hasher
from flask_jwt_extended import create_access_token

def root_route(app):

    def validator(data):
        error = []
        required_fields = ['firstName', 'lastName', 'email', 'password', "phone"]
        for field in required_fields:
            if field not in data or not data[field]:
                error.append({
                "field": field,
                "message": f"The {field} value is invalid"
            })
        return error

        

    @app.route("/auth/test")
    def test():
        return "Testing"

    @app.route("/auth/register", methods = ['POST'])
    def register():
        data = request.json

        #errors
        errors = validator(data)
        if errors != []:
            return {"errors": errors}, 422
        # ['firstName', 'lastName', 'email', 'password']
        try:
            firstname = data['firstName']
            lastname = data['lastName']
            email = data['email']
            pass_w = data['password']
            pass_w = hasher.generate_password_hash(pass_w)
            phone = data['phone']
            universal_users = Users.query.all()
            userId = Users.query.filter_by(email = email).first()
            for user in universal_users: 
                if user.email == email:
                    return {
                            "status": "Bad request",
                            "message": "Email already exists",
                            "statusCode": 400
                                }, 400

            new_user = Users(firstName = firstname, lastName = lastname, email = email, password = pass_w, phone = phone)
            db.session.add(new_user)
            db.session.commit()
            new_org = Organisation(f"{firstname}'s Organisation")
            db.session.add(new_org)
            db.session.commit()
            userId = Users.query.filter_by(email = email).first()
            access_token = create_access_token(identity=email)

            return {
                    "status": "success",
                    "message": "Registration successful",
                    "data": {
                      "accessToken": access_token,
                      "user": {
	                      "userId": userId.userId,
	                      "firstName": firstname, 
	                			"lastName": lastname,
	                			"email": email,
	                			"phone": phone,
                  }
                }
            }, 201 
        except Exception as e:
            return {
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }
    
    @app.route("/auth/login", methods = ['POST'])
    def login():
        data = request.json
        email = data['email']
        pass_w = data['password']
        user = Users.query.filter_by(email = email).first()
        if user.email == email:
            if hasher.check_password_hash(user.password, pass_w):
                access_token = create_access_token(identity=email)
                return {
                        "status": "success",
                        "message": "Login successful",
                        "data": {
                          "accessToken": access_token,
                          "user": {
	                          "userId": user.userId,
	                          "firstName": user.firstName,
	                    			"lastName": user.lastName,
	                    			"email": user.email,
	                    			"phone": user.phone,
                          }
                        }
                }
                
        return {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, 401