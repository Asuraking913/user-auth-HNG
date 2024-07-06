from flask import Flask
from extensions import jwt, db
from config import AppConfig
from route import root_route

app = Flask(__name__)
app.config.from_object(AppConfig)

#routes init
root_route(app)

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
        jwt.init_app(app)
    app.run(debug=True)