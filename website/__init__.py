from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from os import getenv
from flask_login import LoginManager
from sqlalchemy import text
from dotenv import load_dotenv
db = SQLAlchemy()
DB_NAME = "flask_db"


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{getenv('DB_USERNAME')}:{getenv('DB_PASSWORD')}!@localhost:5432/{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Album
    
    with app.app_context():
        db.create_all()

    #To add, change, delete columns
    # with app.app_context():
    #     with db.engine.begin() as connection:
    #         connection.execute(text("ALTER TABLE user DROP COLUMN spotify_token"))
    #         connection.execute(text("ALTER TABLE user ADD COLUMN access_token TEXT"))
    #         connection.execute(text("ALTER TABLE user ADD COLUMN refresh_token TEXT"))
    #         connection.execute(text("ALTER TABLE user ADD COLUMN token_expiration INTEGER"))
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
