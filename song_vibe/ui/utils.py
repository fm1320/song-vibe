import streamlit as st
import pandas as pd
from song_vibe.utils import load_data, load_model, load_index


@st.cache_data
def load_data(folder: str = "data/", file: str = "data.csv") -> pd.DataFrame:
    return load_data(folder)


@st.cache_resource
def load_model():
    return load_model()


@st.cache_data
def load_index():
    return load_index()
