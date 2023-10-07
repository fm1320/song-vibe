import streamlit as st
import pandas as pd
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer




def suggest(song_desc: str = ""):
            data = pd.read_csv('data.csv')
            data.rename(columns={'Song_name': 'category', 'Response': 'text'}, inplace=True)
            df = pd.DataFrame(data, columns = ['text', 'category'])
            encoder = SentenceTransformer("paraphrase-mpnet-base-v2")
            index = faiss.read_index('index.bin')
            search_text = song_desc
            search_vector = encoder.encode(search_text)
            _vector = np.array([search_vector])
            faiss.normalize_L2(_vector)

            k = index.ntotal
            distances, ann = index.search(_vector, k=k)

            results = pd.DataFrame({'distances': distances[0], 'ann': ann[0]})
            results = results.head(10)
            merge = pd.merge(results, df, left_on='ann', right_index=True)
            res_dict = {"results": list(merge.to_dict()['category'].values())}
            print(res_dict)
            return res_dict





# Set page configuration to wide and hide the menu
st.set_page_config(layout="centered")

# Background image CSS
background_style = """
<style>
    body {
        background-image: url('https://example.com/your-image-url.jpg');
        background-size: cover;
    }
</style>
"""

# Display the background style
st.markdown(background_style, unsafe_allow_html=True)

# Text input in the center of the page
st.markdown("<h1 style='text-align: center; color: white;'>Tired of songs that you just don't ... vibe with ?</h1>", unsafe_allow_html=True)
user_input = st.text_input("Describe your mood in the text box below, and we will do the rest. ")


# You can do something with the user input here
if user_input:
    a = suggest(user_input)
    st.write(a)

from flask import Flask, redirect, request, session, url_for, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE
import os 
import json


# Replace with app's client ID from Spotify Developer and redirect URI
CLIENT_ID = "244ea9a10c0040bbb4ee180a3d8e5519"
REDIRECT_URI = 'https://expert-meme-9wvvgr466xwc954-8501.app.github.dev/'

# Initialize the SpotifyPKCE object
sp_oauth = SpotifyPKCE(CLIENT_ID, REDIRECT_URI, scope="user-library-read playlist-read-private playlist-modify-public playlist-modify-private")

import streamlit as st
import spotipy
import spotipy.util as util

# Spotify API credentials
CLIENT_ID = "244ea9a10c0040bbb4ee180a3d8e5519"
CLIENT_SECRET = "31b769f36e2e4c1385b8e67effabcb42"
REDIRECT_URI = 'https://expert-meme-9wvvgr466xwc954-8501.app.github.dev/'  # You need to set this as a valid redirect URI in your Spotify App settings
SCOPE = 'playlist-modify-public'



# Streamlit app
st.title("Like the choice? Try this playlist in spotify! ")


# Authenticate with Spotify
username = None
token = None

# Check if the user is logged in
if 'token_info' not in st.session_state:
    # Display a button to initiate the Spotify login process
    if st.button("Log in with Spotify"):
        auth_url = util.prompt_for_user_token(
            username,
            SCOPE,
            CLIENT_ID,
            CLIENT_SECRET,
            REDIRECT_URI,
        )
        st.session_state.token_info = {'access_token': auth_url}

# If the user is logged in, display the playlist creation form
if 'token_info' in st.session_state:
    token_info = st.session_state.token_info
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user = sp.current_user()
    username = user['id']

    st.success(f"Logged in as {username}")
    st.subheader("Paste your song list in JSON format:")
    song_list_json = a
    try:
        song_data = json.loads(song_list_json)
        song_list = song_data.get("results", [])
    except json.JSONDecodeError:
        st.error("Invalid JSON format. Please provide a valid JSON object.")

    if song_list:
        st.success(f"Loaded {len(song_list)} songs from JSON input.")
        # Create a new playlist
        playlist_name = st.text_input("Enter the playlist name:")
        if st.button("Create Playlist"):
            playlist = sp.user_playlist_create(username, playlist_name)
            playlist_id = playlist['id']

            # Add songs to the playlist
            track_uris = []
            for song_title in song_list:
                results = sp.search(q=f"track:{song_title}", type='track')
                if results['tracks']['items']:
                    track_uris.append(results['tracks']['items'][0]['uri'])
            if track_uris:
                sp.user_playlist_add_tracks(username, playlist_id, track_uris)
                st.success(f"Playlist '{playlist_name}' created with {len(track_uris)} songs.")
            else:
                st.error("No valid songs found in the search results.")
