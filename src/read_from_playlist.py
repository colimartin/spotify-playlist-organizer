import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
import requests
os.environ['SPOTIPY_CLIENT_ID'] = "eccc38a0aee54128b738756e51529341"
os.environ['SPOTIPY_CLIENT_SECRET'] = "9836635dd43441c794d822007f78ef65"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:9000"

def read_from_playlist(playlist_id):
    # Access user account using OAuth
    scope = "playlist-read-private"
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return read_songs_from_playlist(user, playlist_id)

# Get access token to allow request for track audio features
def get_access_token(client_id, client_secret):
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    # convert the response to JSON
    auth_response_data = auth_response.json()
    # save the access token
    access_token = auth_response_data['access_token']
    return access_token

# Header for access token
headers = {
    'Authorization': 'Bearer {token}'.format(token=
        get_access_token("eccc38a0aee54128b738756e51529341", "9836635dd43441c794d822007f78ef65"))
}

# Uses access token to access track audio features
def get_analysis(track_id):
    base_url = 'https://api.spotify.com/v1/'
    analysis = requests.get(base_url + 'audio-features/' + track_id, headers=headers)
    return analysis

# Uses OAuth to get user playlist and calls get_analysis to access track features
# Returns list of dictionary entries of the form:
#   { id: Spotify track ID
#     features: JSON of Spotify track audio features }
# One entry for each song in the input playlist

def read_songs_from_playlist(user, playlist_id):
    playlist = user.playlist_items(playlist_id)
    analyses = []
    for song in playlist['items']:
        track_id = song['track']['id']
        analysis = get_analysis(track_id)
        analysis_json = analysis.json()
        #danceability = analysis_json['danceability']
        #print(analysis_json)
        analyses.append({
            "id": track_id,
            "features": analysis_json
        })
        #print(danceability)
        #print(song['track']['name'])
    return analyses