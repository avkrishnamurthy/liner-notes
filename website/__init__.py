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
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{getenv('DB_USERNAME')}:{getenv('DB_PASSWORD')}!@localhost:5432/{DB_NAME}"
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    db.init_app(app)

    # from . import views
    from .auth.auth import auth
    from .reviews.reviews import reviews
    from .feed.feed import feed_
    from .profiles.profiles import profiles
    from .search.search import search

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(reviews, url_prefix='/')
    app.register_blueprint(feed_, url_prefix='/')
    app.register_blueprint(profiles, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

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
