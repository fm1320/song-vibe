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




import streamlit as st
import base64
from requests import post, get
import json
import urllib.parse


# Spotify API credentials
#SPOTIFY_CLIENT_ID = "244ea9a10c0040bbb4ee180a3d8e5519"
#SPOTIFY_CLIENT_SECRET = "31b769f36e2e4c1385b8e67effabcb42"
SPOTIFY_CLIENT_ID = st.secrets['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = st.secrets['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = 'https://expert-meme-9wvvgr466xwc954-8501.app.github.dev/'  # You need to set this as a valid redirect URI in your Spotify App settings

def get_token():
    client_id =st.secrets['SPOTIFY_CLIENT_ID']
    client_secret =st.secrets['SPOTIFY_CLIENT_SECRET']
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_headers(token):
    return {"Authorization": "Bearer " + token}

if st.button('Login with Spotify'):
    token = get_token()
    st.write("Sucess")    

    # Save the access token along with any other Spotify API call methods
