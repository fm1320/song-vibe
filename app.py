import streamlit as st
import pandas as pd
import sys
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

@st.cache_data
def read_from_data():
            dataframe = pd.read_csv('data.csv')
            return dataframe
            
@st.cache_resource  
def load_model():
            return SentenceTransformer("paraphrase-mpnet-base-v2")

@st.cache_data
def load_index():
            return faiss.read_index('index.bin')

            
def suggest(song_desc: str = ""):
            data = read_from_data()
            data.rename(columns={'Song_name': 'category', 'Response': 'text'}, inplace=True)
            df = pd.DataFrame(data, columns = ['text', 'category'])
            encoder = load_model()
            index = load_index()
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
    st.write(suggest(user_input))
else:
    st.write("")

st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1118px-Spotify_logo_with_text.svg.png',width=200)
if st.button("Hear this playlist on Spotify!"):
       st.text('''More songs and full spotify integration coming soon! 
The Spotify version is in beta, to try it out contact me:
@filip.makraduli@marks-and-spencer.com ''')




