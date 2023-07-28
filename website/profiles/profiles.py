from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session
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
    user = User.query.get(current_user.id)
    token_info = user.token_info
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    if token_info: cache_handler.session['token_info'] = token_info    
    #If want currently listening track
    # auth_manager = spotipy.oauth2.SpotifyOAuth(scope="user-top-read user-read-currently-playing",
    #                                            cache_handler=cache_handler,
    #                                            show_dialog=True)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope="user-top-read",
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    #Currently listening track
    # k = spotify.current_user_playing_track()
    toptracks = spotify.current_user_top_tracks(limit=5)['items']
    me = spotify.me()["display_name"]
    top_tracks_json = {}
    tracks = []
    for tn, track in enumerate(toptracks):
        print(track['external_urls']['spotify'])
        print("AAAAA")
        top_tracks_json[tn] = (track['name'], track['album']['images'][1]['url'], track['album']['artists'][0]['name'], track['external_urls']['spotify'])
        tracks.append((track['name'], track['album']['images'][1]['url'], track['album']['artists'][0]['name'], track['external_urls']['spotify']))

    user = User.query.get(current_user.id)
    user.top_tracks = top_tracks_json
    db.session.commit()
    following_users = set(user.following.all())
    follower_users = set(user.follower.all())
    return render_template("my_profile.html", user=current_user, t_tracks = tracks, me=me, len=len, get_date = date.get_date, following=following_users, followers=follower_users)

@profiles.route('/redirect')
@login_required
def redirectPage():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
                                               cache_handler=cache_handler,
                                               show_dialog=True)
    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        user = User.query.get(current_user.id)
        user.token_info = cache_handler.session['token_info']
        db.session.commit()
    return redirect(url_for('profiles.my_profile', _external=True))

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