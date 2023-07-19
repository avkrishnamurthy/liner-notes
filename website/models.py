from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.Text)
    album_name = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    album_img = db.Column(db.String(10000))
    rating = db.Column(db.Float)
    review = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user_albums')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    albums = db.relationship('Album', overlaps='user_albums,user')
    favorite_albums = db.relationship('FavoriteAlbum', overlaps='user_favorite_albums,user')
    top_tracks = db.Column(JSONB)
    access_token = db.Column(db.Text)
    token_expiration = db.Column(db.Integer)
    refresh_token = db.Column(db.Text)
    follower = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref('following', lazy='dynamic'),
        lazy='dynamic'
    )
    feed = db.relationship(
        'Album',
        secondary=followers,
        primaryjoin=(followers.c.following_id == id),
        secondaryjoin=(followers.c.follower_id == Album.user_id),
        order_by=Album.date.desc(),
        overlaps="follower,following",
        lazy='dynamic'
    )

class FavoriteAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(10000))
    album_name = db.Column(db.String(10000))
    album_img = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='user_favorite_albums')
