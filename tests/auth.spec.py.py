import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, jwt, db
from flask import json
import requests
from config import AppConfig

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True 
        app.config.from_object(AppConfig)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            jwt.init_app(app)
            db.init_app(app)
            db.create_all()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"text" : "<h1>This is the home page</h1>"})

    def test_auth_login(self):
        data ={"user" : "Israel", "pass" : "password"} 
        response = self.client.post("/api/login", json=data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
# {"user" : "Israel", "pass" : "password"}