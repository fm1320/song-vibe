import streamlit as st

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
st.markdown("<h1 style='text-align: center; color: white;'>Enter Text</h1>", unsafe_allow_html=True)
user_input = st.text_input("")

# You can do something with the user input here
if user_input:
    st.write(f"You entered: {user_input}")
