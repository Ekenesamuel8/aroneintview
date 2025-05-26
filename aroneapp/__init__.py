import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import db, login_manager, csrf
from .auth.routes import auth_arch
from .main.routes import main_arch

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLDB')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_arch)
    app.register_blueprint(main_arch)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return db.session.get(User, int(user_id))

    return app