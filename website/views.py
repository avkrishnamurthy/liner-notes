from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Album, User, FavoriteAlbum
from . import db
import json
import spotipy
import time
from . import spotify, date

views = Blueprint('views', __name__)

@views.route('/all-reviews/<username>', methods=['GET'])
@login_required
def all_reviews(username):
    if username==current_user.username:
        return redirect(url_for("views.my_review", _external=True))
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("views.my_profile", _external=True))
    sorted_albums = Album.query.filter_by(user_id=user.id).order_by(Album.date.desc()).all()
    return render_template("all_reviews.html", user=user, get_date=date.get_date, albums=sorted_albums)

@views.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    if username==current_user.username:
        return redirect(url_for("views.my_profile", _external=True))
    user = User.query.filter_by(username=username).first()
    
    if not user: 
        flash("User does not exist", category="error")
        return redirect(url_for("views.my_profile", _external=True))
    
    following_users = set(user.following.all())
    follower_users = set(user.follower.all())

    return render_template('profile.html', current_user = current_user, user=user, len=len, get_date=date.get_date, following=following_users, followers=follower_users)

@views.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    follow_json = json.loads(request.data)
    follow_username = follow_json['username']
    user = User.query.filter_by(username=follow_username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("views.my_profile"))

    if current_user in user.follower:
        user.follower.remove(current_user)
    else:
        user.follower.append(current_user)
    
    db.session.commit()

    return redirect(url_for("views.profile", username=username))

@views.route('/check-user-exists', methods=['POST'])
def check_user_exists():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    user_exists = True if user else False
    return jsonify({'exists': user_exists})

@views.route('/my-reviews')
@login_required
def my_reviews():
    sorted_albums = Album.query.filter_by(user_id=current_user.id).order_by(Album.date.desc()).all()
    return render_template('my_reviews.html', user=current_user, get_date=date.get_date, albums=sorted_albums)

@views.route('/my-profile')
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

@views.route('/feed')
@login_required
def feed():
    page = request.args.get('page', 1, type=int)
    per_page = 3
    my_feed = current_user.feed.paginate(page=page, per_page=per_page)
    return render_template("feed.html", user=current_user, feed=my_feed, convert_datetime=date.convert_datetime, length=my_feed.pages)

@views.route('/redirect')
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
    return redirect(url_for("views.my_profile", _external=True))

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_album():
    img_urls = []
    if request.method == 'POST': 
        artist = request.form.get('artist')#Gets the note from the HTML 

        if len(artist) < 1:
            flash('Artist name is too short', category='error') 
    
        token = spotify.get_token()
        if artist:
            result = spotify.search_for_artist(token, artist)
            if not result: 
                flash('Error finding artist.', category='error') 
                return redirect(url_for("views.search_album", _external=True))
            artist_id = result["id"]
            songs = spotify.get_albums_by_artist(token, artist_id)
            for i in range(len(songs)):
                img_urls.append([songs[i]['images'][1]['url'], songs[i]['name'], i, songs[i]['artists'][0]['name']])
    return render_template("search.html", user=current_user, img_urls=img_urls)


@views.route('/delete-album', methods=['POST'])
def delete_album():  
    album_json = json.loads(request.data)
    albumId = album_json['albumId']
    album = Album.query.get(albumId)
    if album:
        if album.user_id == current_user.id:
            db.session.delete(album)
            db.session.commit()

    return jsonify({})
@views.route('/add-album', methods=["POST"])
def add_album():
    album = json.loads(request.data)
    album_img = album['albumImgUrl']
    album_name = album['albumName']
    artist_name = album['artistName']
    rating = album['rating']
    review = album['review']
    new_album = Album(artist_name = artist_name, album_name = album_name, album_img=album_img, user_id = current_user.id, rating=rating, review=review)
    db.session.add(new_album)
    db.session.commit()
    flash('Album review added!', category='success')
    return jsonify({})

@views.route('/add-favorite', methods=['POST'])
def add_favorite():
    favorite_json = json.loads(request.data)
    album_img = favorite_json['albumImgUrl']
    album_name = favorite_json['albumName']
    artist_name = favorite_json['artistName']
    new_favorite = FavoriteAlbum(artist_name = artist_name, album_name = album_name, album_img=album_img, user_id = current_user.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({})


@views.route('/delete-favorite', methods=['POST'])
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