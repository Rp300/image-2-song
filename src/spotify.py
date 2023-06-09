import streamlit as st
import requests
import json
from base64 import b64encode

# Define your Spotify API credentials
CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]

# Wrapper function
def generate_song_suggestions(songs):
    # Authenticate and get the access token
    access_token = get_access_token()
    # Display the songs and play buttons
    for song in songs:
        preview_url = get_preview_url(song[0], song[1], access_token)
        if preview_url:
            st.audio(preview_url, format='audio/mp3', start_time=0)
            st.write(f"{song[0]} - {song[1]}")
        else:
            st.write(f"Preview not available for {song[0]} - {song[1]}")

# Get the access token from Spotify API
def get_access_token():
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'client_credentials',
    }
    token_headers = {
        'Authorization': 'Basic ' + b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode('utf-8')).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = json.loads(token_response.text)
    return token_response_data['access_token']

# Get the preview URL for a song
def get_preview_url(track_name, artist_name, access_token):
    search_url = f'https://api.spotify.com/v1/search?q=track:{track_name} artist:{artist_name}&type=track&limit=1'
    search_headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }
    search_response = requests.get(search_url, headers=search_headers)
    search_response_data = json.loads(search_response.text)

    # Extract the track ID from the search results
    if 'items' in search_response_data['tracks'] and len(search_response_data['tracks']['items']) > 0:
        return search_response_data['tracks']['items'][0]['preview_url']
    else:
        return None