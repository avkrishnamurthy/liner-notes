from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user

from website.utils import spotify, date
from website.models import User, FavoriteAlbum
from website import db
import json
import spotipy
import time

profiles = Blueprint('profiles', __name__, template_folder = 'templates', static_url_path='profiles/', static_folder='static')

@profiles.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    if username==current_user.username:
        return redirect(url_for("profiles.my_profile", _external=True))
    user = User.query.filter_by(username=username).first()
    
    if not user: 
        flash("User does not exist", category="error")
        return redirect(url_for("profiles.my_profile", _external=True))
    
    following_users = set(user.following.all())
    follower_users = set(user.follower.all())

    return render_template('profile.html', current_user = current_user, user=user, len=len, get_date=date.get_date, following=following_users, followers=follower_users)

@profiles.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    follow_json = json.loads(request.data)
    follow_username = follow_json['username']
    user = User.query.filter_by(username=follow_username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("profiles.my_profile"))

    if current_user in user.follower:
        user.follower.remove(current_user)
    else:
        user.follower.append(current_user)
    
    db.session.commit()

    return redirect(url_for("profiles.profile", username=username))

@profiles.route('/check-user-exists', methods=['POST'])
def check_user_exists():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    user_exists = True if user else False
    return jsonify({'exists': user_exists})

@profiles.route('/my-profile')
@login_required
def my_profile():
    if not current_user.access_token:
        sp_oauth = spotify.create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    else:
        now = int(time.time())
        is_expired = current_user.token_expiration-now < 60
        if is_expired:
            sp_oauth = spotify.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(current_user.refresh_token)
            user = User.query.get(current_user.id)
            user.access_token = token_info['access_token']
            user.token_expiration = token_info['expires_at']
            db.session.commit()
        sp = spotipy.Spotify(auth=current_user.access_token)
        toptracks = sp.current_user_top_tracks(limit=5)['items']
        top_tracks_json = {}
        tracks = []
        for tn, track in enumerate(toptracks):
            top_tracks_json[tn] = (track['name'], track['album']['images'][1]['url'], track['album']['artists'][0]['name'])
            tracks.append((track['name'], track['album']['images'][1]['url'], track['album']['artists'][0]['name']))

        user = User.query.get(current_user.id)
        user.top_tracks = top_tracks_json
        db.session.commit()

        following_users = set(user.following.all())
        follower_users = set(user.follower.all())
        return render_template("my_profile.html", user=current_user, t_tracks = tracks, len=len, get_date = date.get_date, following=following_users, followers=follower_users)

@profiles.route('/redirect')
@login_required
def redirectPage():
    sp_oauth = spotify.create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    user = User.query.get(current_user.id)
    if user:
        user.access_token = token_info['access_token']
        user.refresh_token = token_info['refresh_token']
        user.token_expiration = token_info['expires_at']
        db.session.commit()
    return redirect(url_for("profiles.my_profile", _external=True))


@profiles.route('/delete-favorite', methods=['POST'])
@login_required
def delete_favorite():
    favorite_json = json.loads(request.data)
    favoriteId = favorite_json['favoriteId']
    favorite = FavoriteAlbum.query.get(favoriteId)
    if favorite:
        if favorite.user_id == current_user.id:
            db.session.delete(favorite)
            db.session.commit()
    return jsonify({})