import spotipy
import os
from read_from_playlist import read_from_playlist
from spotipy.oauth2 import SpotifyOAuth
os.environ['SPOTIPY_CLIENT_ID'] = "eccc38a0aee54128b738756e51529341"
os.environ['SPOTIPY_CLIENT_SECRET'] = "9836635dd43441c794d822007f78ef65"
os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:9000"

def write_playlist():
    # Access user account using OAuth
    scope = "playlist-modify-public"
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    user_id = "colimartin"
    playlist_name = "Sorted Playlist"
    # playlist_desc = "Playlist sorted by song qualities"
    # Create new playlist
    print(f"Creating new playlist {playlist_name}")
    response = user.user_playlist_create(user_id, playlist_name)
    print(f"Playlist {playlist_name} created")

    # Get songs from playlist
    print("Reading from source playlist")
    analyses = read_from_playlist()
    print("Source tracks loaded")
    # Filter songs by danceability, returning only those that pass the criteria
    #print("Sorting by danceability")
    #songs_output = sort_by_danceability(analyses, 0.6)
    #print("Sorted tracks loaded")
    print("Sorting by valence")
    songs_output = sort_by_valence(analyses, 0.5)
    print("Sorted tracks loaded")
    print("Sorting by energy")
    songs_output = sort_by_energy(songs_output, 0.6)
    print("Sorted tracks loaded")
    print("Converting dict of songs to list of track IDs")
    songs_list = dict_to_list(songs_output)
    print("Dictionary converted to list")

    # Get ID of newly created playlist
    playlist_id = response['id']
    # Add filtered songs to new playlist
    print(f"Adding filtered songs to playlist {playlist_name}")
    user.playlist_add_items(playlist_id, songs_list)
    print("New songs added")

def sort_by_danceability(analyses, val):
    accepted_songs = []
    for track in analyses:
        if track['features']['danceability'] > val:
            accepted_songs.append({
                "id": track['id'],
                "features": track['features']
            })
    print(accepted_songs)
    return accepted_songs

def sort_by_valence(analyses, val):
    accepted_songs = []
    for track in analyses:
        if track['features']['valence'] < val:
            accepted_songs.append({
                "id": track['id'],
                "features": track['features']
            })
    print(accepted_songs)
    return accepted_songs

def sort_by_energy(analyses, val):
    accepted_songs = []
    for track in analyses:
        if track['features']['energy'] > val:
            accepted_songs.append({
                "id": track['id'],
                "features": track['features']
            })
    print(accepted_songs)
    return accepted_songs

def dict_to_list(songs_output):
    songs_list = []
    for track in songs_output:
        songs_list.append(track['id'])
    return songs_list

write_playlist()