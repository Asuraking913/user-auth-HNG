from flask import jsonify, request, json, session
from models import db, Users
from flask_bcrypt import Bcrypt

def root_route(app):

	hasher = Bcrypt(app)

	@app.route("/")
	def home(): 
		return "<h1>Oi!! This is the home page</h1>"
	
	@app.route("/api/show", methods = ['GET'])
	def show(): 
		user_id = session.get('id')
		if user_id:

			found_user = Users.query.filter_by(id = user_id).first()
			return {
				"name": found_user.user_name,
				"email" : found_user.user_email, 
			}
		return {
			"msg" : "No User"
		}, 401
	
	@app.route("/get_user")
	def get_user():
		try:
			user_id = session.get('id')
			if user_id:
				found_user = Users.query.filter_by(id = user_id).first()
				return {
					"user" : found_user.user_name,
				}
		except:
			pass
		return {"msg" :"No User"}, 401

	@app.route("/api/register", methods = ['POST'])
	def register_user():
		username = request.json['user']
		useremail = request.json['email']
		userpass = request.json['pass']
		userpass = hasher.generate_password_hash(userpass)
		found_user = Users.query.all()
		for users in found_user:
			if users.user_name == username:
				return {
					"msg": "User Name Already exists"
				}, 409
			if users.user_email == useremail:
				return {
					"msg": "Email Address Already exists"
				}, 409
		new_user = Users(username, userpass)
		db.session.add(new_user)
		db.session.commit()
		new_user.user_email = useremail
		db.session.commit()

		return {
			"msg" : "Created User"
		}, 200
	
	@app.route("/api/login", methods = ['POST'])
	def login():

		user_id = session.get("id")
		if user_id:
			response = jsonify({
				"msg" : "User is already logged"
			}), 401
			return response


		username = request.json['user']
		userpass = request.json['pass']
		found_user = Users.query.filter_by(user_name = username).all()
		for user in found_user: 
			if user.user_name == username:
				if hasher.check_password_hash(user.user_pass, userpass):
					session['id'] = user.id
					response = jsonify({
						"msg" : "User logged in"
					})
					return response
				else :
					return {
						"msg" : "Incorrect password"
					}, 401
			
		return {
			"msg" : "Incorrect Username"
		}, 401
	
	@app.route("/api/logout")
	def logout():
		session.pop("id", None)
		return "Usr Logged Out"