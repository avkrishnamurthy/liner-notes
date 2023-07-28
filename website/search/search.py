from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from website.models import Album, User, FavoriteAlbum
from website import db
import json
from website.utils import date, spotify

search = Blueprint('search', __name__, template_folder='templates', static_url_path='search/', static_folder='static')


@search.route('/search', methods=['GET', 'POST'])
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
                return redirect(url_for("search.search_album", _external=True))
            artist_id = result["id"]
            albums = spotify.get_albums_by_artist(token, artist_id)
            for i in range(len(albums)):
                print(albums[i])
                img_urls.append([albums[i]['images'][1]['url'], albums[i]['name'], i, albums[i]['artists'][0]['name'], albums[i]['external_urls']['spotify']])
    return render_template("search.html", user=current_user, img_urls=img_urls)

@search.route('/add-album', methods=["POST"])
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

@search.route('/add-favorite', methods=['POST'])
def add_favorite():
    favorite_json = json.loads(request.data)
    album_img = favorite_json['albumImgUrl']
    album_name = favorite_json['albumName']
    artist_name = favorite_json['artistName']
    new_favorite = FavoriteAlbum(artist_name = artist_name, album_name = album_name, album_img=album_img, user_id = current_user.id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({})