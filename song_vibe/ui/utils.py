import streamlit as st
import pandas as pd
import song_vibe.utils as utils


@st.cache_data
def load_data(folder: str = "data/", file: str = "data.csv") -> pd.DataFrame:
    return utils.load_data(folder, file)


@st.cache_resource
def load_model():
    return utils.load_model()


@st.cache_data
def load_index():
    return utils.load_index()
