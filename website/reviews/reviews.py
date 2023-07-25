from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from website.models import User, Album
from website import db
import json
from website.utils import date

reviews = Blueprint('reviews', __name__, template_folder='templates', static_url_path='reviews/', static_folder='static')

@reviews.route('/delete-album', methods=['POST'])
def delete_album():  
    album_json = json.loads(request.data)
    albumId = album_json['albumId']
    album = Album.query.get(albumId)
    if album:
        if album.user_id == current_user.id:
            db.session.delete(album)
            db.session.commit()

    return jsonify({})

@reviews.route('/my-reviews')
@login_required
def my_reviews():
    sorted_albums = Album.query.filter_by(user_id=current_user.id).order_by(Album.date.desc()).all()
    return render_template('my_reviews.html', user=current_user, get_date=date.get_date, albums=sorted_albums)


@reviews.route('/all-reviews/<username>', methods=['GET'])
@login_required
def all_reviews(username):
    if username==current_user.username:
        return redirect(url_for("reviews.my_reviews", _external=True))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("profiles.my_profile", _external=True))
    sorted_albums = Album.query.filter_by(user_id=user.id).order_by(Album.date.desc()).all()
    return render_template("all_reviews.html", user=user, get_date=date.get_date, albums=sorted_albums)