from flask import Flask
from config import Config
from patient_doctor_conversation.routes import main as main_blueprint
from patient_doctor_conversation.routes import auth as auth_blueprint

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    app.config.from_pyfile('config.py')

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
