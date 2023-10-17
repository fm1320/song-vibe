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
    st.write(suggest(user_input))
else:
    st.write("")

st.image('https://images.unsplash.com/photo-1614680376593-902f74cf0d41?auto=format&fit=crop&q=80&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&w=1974',width=100)
if st.button("Hear this playlist on Spotify!"):
       st.text("More songs and full spotify integration coming soon!")




