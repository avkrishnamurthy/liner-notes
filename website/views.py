from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Album, User
from . import db
import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home(): 
    return render_template("home.html", user=current_user)


@views.route('/profile/<username>')
@login_required
def profile(username):
    if username==current_user.username:
        return redirect(url_for("views.my_profile", _external=True))
    user = User.query.filter_by(username=username).first()
    if not user: 
        flash("User does not exist", category="error")
        return redirect(url_for("views.my_profile", _external=True))
    return render_template('profile.html', user=user)


@views.route('/check-user-exists', methods=['POST'])
def check_user_exists():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    user_exists = True if user else False
    return jsonify({'exists': user_exists})

@views.route('/my-profile')
@login_required
def my_profile():
    if not current_user.access_token:
        sp_oauth = create_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    else:
        now = int(time.time())
        #If expired or will expire in a minute, then get a new refresh token
        is_expired = current_user.token_expiration-now < 60
        if is_expired:
            sp_oauth = create_spotify_oauth()
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

        return render_template("my_profile.html", user=current_user, t_tracks = tracks)

@views.route('/redirect')
@login_required
def redirectPage():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    user = User.query.get(current_user.id)
    if user:
        user.access_token = token_info['access_token']
        user.refresh_token = token_info['refresh_token']
        user.token_expiration = token_info['expires_at']
        db.session.commit()
    return redirect(url_for("views.my_profile", _external=True))

def create_spotify_oauth():
    load_dotenv()
    return SpotifyOAuth(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'),
                        redirect_uri=url_for("views.redirectPage", _external=True),
                        scope="user-top-read")

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search_album():
    img_urls = []
    artist_name = ""
    if request.method == 'POST': 
        artist = request.form.get('artist')#Gets the note from the HTML 

        if len(artist) < 1:
            flash('Artist name is too short', category='error') 
        else: 
            artist_name = artist
        # else:
        #     new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
        #     db.session.add(new_note) #adding the note to the database 
        #     db.session.commit()
        #     flash('Note added!', category='success')
        artist_name = artist
    
        load_dotenv()

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        def get_token():
            auth_string = client_id+":"+client_secret
            auth_bytes = auth_string.encode("utf-8")
            auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

            url = "https://accounts.spotify.com/api/token"
            headers = {
                "Authorization": "Basic "+auth_base64,
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {"grant_type": "client_credentials"}
            result = post(url, headers=headers, data=data)
            json_result = json.loads(result.content)
            token = json_result['access_token']
            return token

        def get_auth_header(token):
            return {"Authorization": "Bearer "+token}

        def search_for_artist(token, artist_name):
            url = "https://api.spotify.com/v1/search"
            header = get_auth_header(token)
            query = f"?q={artist_name}&type=artist&limit=1"
            query_url = url+query
            result = get(query_url, headers=header)
            json_result = json.loads(result.content)["artists"]["items"]
            if len(json_result)==0:
                print("No artist with this name exists...")
                return None
            return json_result[0]

        def get_songs_by_artist(token, artist_id):
            url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album"
            header = get_auth_header(token)
            result = get(url, headers=header)
            json_result = json.loads(result.content)['items']
            return json_result
        token = get_token()
        if artist_name:
            result = search_for_artist(token, artist_name)
            artist_id = result["id"]
            songs = get_songs_by_artist(token, artist_id)

            for i in range(len(songs)):
                img_urls.append([songs[i]['images'][1]['url'], songs[i]['name']])
    return render_template("search.html", user=current_user, img_urls=img_urls)

@views.route('/delete-album', methods=['POST'])
def delete_album():  
    album_json = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    albumId = album_json['albumId']
    print(albumId)
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
    rating = album['rating']
    review = album['review']
    new_album = Album(album_name = album_name, album_img=album_img, user_id = current_user.id, rating=rating, review=review)
    db.session.add(new_album)
    db.session.commit()
    flash("Album added", category="success")
    return jsonify({})

