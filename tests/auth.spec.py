import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask_sqlalchemy import SQLAlchemy
from flask import json, Flask
from extensions import db, jwt
from config import AppConfig
from route import root_route
from models import Organisation

def create_app():
        app = Flask(__name__)


        with app.app_context():
            app.config.from_object(AppConfig)
            jwt.init_app(app)
            db.init_app(app)
            db.create_all()

            return app
app = create_app()
root_route(app)

data_gen = {
        "firstName" : "Asura",
        "lastName" : "Obi",
        "email" : "israelshedrack913@gmail.com",
        "password" : "12345",
        "phone" : "090351655"
        }


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True 
        self.client = app.test_client()

    def test_test_route(self):
        response = self.client.get("/auth/test")
        self.assertEqual(response.status_code, 200)


    def test_register_route(self):
        response = self.client.post("/auth/register", json = data_gen)
        get_json = response.get_json()
        print(get_json)
        self.assertEqual(get_json['data']['user']['firstName'], data_gen['firstName'])
        user_id = get_json['data']['user']['userId']
        with app.app_context():
            org = Organisation.query.filter_by(userId = user_id).first().name
        self.assertEqual(org, f"{data_gen['firstName']}'s Organisation")
        self.assertIn('accessToken', get_json['data'])
        # print(org)

    def test_route_login(self):
        response = self.client.post("/auth/login", json=data_gen)
        get_json = response.get_json()
        if response.status_code == 201:
            self.assertIn('accessToken', get_json['data'])
            self.assertIn('firstName', get_json['data']['user'])
            self.assertIn('lastName', get_json['data']['user'])
            self.assertIn('email', get_json['data']['user'])
            self.assertIn('phone', get_json['data']['user'])

        elif response.status_code == 422:
            self.assertIn('message', get_json)

    # def test_duplicate_email(self):
    #     response = self.client.post("/auth/register", json = data_gen)
    #     get_json = response.get_json()
    #     if response.status_code == 400:
    #         self.assertEqual(response.status_code, 400)
    #         self.assertEqual(["Email already exists", "userId already exists",], get_json['message'])
    #     else:
    #         self.assertEqual(response.status_code, 201)

    def test_validation(self):
      response = self.client.post("/auth/login", json = data_gen)
      get_json = response.get_json()
      required = ['firstName', 'lastName', 'email', 'password', "phone"]
      for details in required:
          self.assertIn(details, get_json['data']['user'])

    # data_gen = {
        # "firstName" : "Asura",
        # "lastName" : "Obi",
        # "email" : "israelshedrack913@gmail.com",
        # "password" : "12345",
        # "phone" : "090351655"
        # }

if __name__ == "__main__":
    unittest.main()
# {"user" : "Israel", "pass" : "password"}