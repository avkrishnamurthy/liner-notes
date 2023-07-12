from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    album_img = db.Column(db.String(10000))
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    albums = db.relationship('Album')
    top_tracks = db.Column(JSONB)
    access_token = db.Column(db.Text)
    token_expiration = db.Column(db.Integer)
    refresh_token = db.Column(db.Text)
