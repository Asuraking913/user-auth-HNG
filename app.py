from flask import Flask
from extensions import jwt, db
from config import AppConfig
from route import root_route

def create_app():

    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(AppConfig)
        db.init_app(app)
        from models import Users, Organisation
        db.create_all()
        jwt.init_app(app)
    
    return app

#routes init
app = create_app()
root_route(app)

if __name__ == '__main__':
    # with app.app_context():
    #     db.init_app(app)
    #     db.create_all()
    #     jwt.init_app(app)
    app.run(debug=True)