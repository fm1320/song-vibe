import streamlit as st
from song_vibe.inference import suggest


def run():

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
    st.markdown(
        "<h1 style='text-align: center; color: white;'>Tired of songs that you just don't ... vibe with ?</h1>",
        unsafe_allow_html=True,
    )
    user_input = st.text_input(
        "Describe your mood in the text box below, and we will do the rest. "
    )

    # You can do something with the user input here
    if user_input:
        st.write(suggest(user_input))
    else:
        st.write("")

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1118px-Spotify_logo_with_text.svg.png",
        width=200,
    )
    if st.button("Hear this playlist on Spotify!"):
        st.text(
            """More songs and full spotify integration coming soon! 
    The Spotify version is in beta, to try it out contact me:
    @filip.makraduli@marks-and-spencer.com """
        )


if __name__ == "__main__":
    run()
