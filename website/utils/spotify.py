from dotenv import load_dotenv
from flask import url_for
import os
import base64
import json
from requests import post, get
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

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

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album"
    header = get_auth_header(token)
    result = get(url, headers=header)
    json_result = json.loads(result.content)['items']
    return json_result

def create_spotify_oauth():
    load_dotenv()
    return SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'), client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                        redirect_uri=url_for("profiles.redirectPage", _external=True),
                        scope="user-top-read")