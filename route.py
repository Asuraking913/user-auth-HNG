from models import Users, Organisation
from extensions import db
from flask import request, jsonify
from extensions import hasher
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

def root_route(app):

    hasher = Bcrypt()


    @app.route("/")
    def home():
        return "<h1>This is the home page</h1>"

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
            new_org = Organisation(name = f"{firstname}'s Organisation")
            db.session.add(new_org)
            db.session.commit()
            userId = Users.query.filter_by(email = email).first()
            access_token = create_access_token(identity=userId.userId)

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
            db.session.rollback()
            print(e)
            return {
                "error" : f"{e}",
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            }, 400
    
    @app.route("/auth/login", methods = ['POST'])
    def login():
        data = request.json
        email = data['email']
        pass_w = data['password']
        user = Users.query.filter_by(email = email).first()
        if user.email == email:
            if hasher.check_password_hash(user.password, pass_w):
                access_token = create_access_token(identity=user.userId)
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
                }, 201
                
        return {
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, 401
    
    @app.route("/api/users/<id>")
    @jwt_required()
    def get_users(id):
        try:
            user = Users.query.filter_by(userId = id).first()
            return {
            		"status": "success",
                    "message": f"Record for {user.firstName}",
                    "data": {
                    "userId": user.userId,
                    "firstName": user.firstName,
            		"lastName": user.lastName,
            		"email": user.email,
            		"phone": user.phone
                }
            }, 200

        except Exception as e:
            return {
                "status": "Bad request",
                "message": "User does not exist",
                "statusCode": 401
            }, 401
        
    @app.route("/api/organisations", methods = ['GET', "POST"])
    @jwt_required()
    def get_organisations():
        if request.method == 'GET':
            user_id = get_jwt_identity()
            user_orgs = Users.query.filter_by(userId = user_id).first().organisation

            orgList = [{"orgId" : orgs.orgId, "name" : orgs.name, "descrption": orgs.description} for orgs in user_orgs]

            return {
                "status": "success",
	            	"message": "User's list of organisation",
                "data": {
                  "organisations": orgList
                }
            }, 200
        if request.method == 'POST':
            def validator(data):
                error = []
                required_fields = ['name', "descrip"]
                for field in required_fields:
                    if field not in data or not data[field]:
                        error.append({
                        "field": field,
                        "message": f"The {field} value is invalid"
                    })
                return error
            try:
                data = request.json
                errors = validator(data)
                if errors != []:
                    return {"errors": errors}, 422
                org_name = request.json['name']
                descrip = request.json['descrip']
                user_id = get_jwt_identity()
                user = Users.query.filter_by(userId = user_id).first()
                new_org = Organisation(name = org_name, description = descrip, users = user)
                db.session.add(new_org)
                db.session.commit()
                org_id = Organisation.query.filter_by(userId = user_id).first()

                return {
                    "status": "success",
                    "message": "Organisation created successfully",
                    "data": {
	                    "orgId": org_id.orgId, 
	                    "name": org_name, 
	                    "description": descrip
                    }
                }
            
            except Exception as e:
                return{
                    "status": "Bad Request",
                    "message": "Client error",
                    "statusCode": 400
                }

    
    @app.route("/api/organisations/<id>")
    @jwt_required()
    def get_organisation(id):
        user_id = get_jwt_identity()
        user = Users.query.filter_by(userId = user_id).first()

        return {
            "status": "success",
        		"message": f"{user.firstName}'s organisation record",
            "data": {
        		"orgId": user.organisation[0].orgId,
        		"name": user.organisation[0].name, 
        		"description": user.organisation[0].description,
        	}
        }, 200

    @app.route("/api/organisations/<orgId>/users", methods = ['POST'])
    def add_user_org(orgId):
        user_id = request.json['userId']
        user = Users.query.filter_by(userId = user_id).first()
        org = Organisation.query.filter_by(orgId = orgId).first()
        org_name = org.name
        org.users = user
        db.session.commit()

        return {
            "status": "success",
            "message": f"{user.firstName} added to {org_name} successfully",
        }