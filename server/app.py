from datetime import timedelta
from flask import Flask
from routes import root_route
from models import db
from config import Appconfig
from flask_cors import CORS, cross_origin
from flask_session import Session


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config.from_object(Appconfig)
root_route(app)
app.permanent_session_lifetime = timedelta(minutes=4)
app.secret_key = "@#$@#$@#"
server_session = Session(app)
# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE'] = True
# app.config['SESSION_COOKIE_HTTPONLY'] =True


if __name__ == "__main__": 
	with app.app_context():
		db.init_app(app)
		db.create_all()
		# server_session.init_app(app)
	app.run(debug = True, port = 2000)