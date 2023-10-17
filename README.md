<h1 align="center">
🎶 Song vibe 🎶
</h1>

<div id="top" align="center">

![GitHub](https://img.shields.io/github/license/fm1320/song-vibe?link=https%3A%2F%2Fgithub.com%2Ffm1320%2Fsong-vibe%2Fblob%2Fmain%2FLICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/fm1320/song-vibe?logo=github)
![GitHub forks](https://img.shields.io/github/forks/fm1320/song-vibe?logo=github)


</div>

### This is a tool that gives song recommendations based on vibes and moods. Sometimes the music and playlists we hear don't "hit" our vibe, so we are using AI to try to change that.

A dataset of songs and their descriptions of moods and vibes is generated by promoting an LLM. 
Each song's vibe is encoded using a transformer model and saved as a vector index. 
Then this vector index is queried by similarity using the vector embedding of the user's input

## Installation

Follow the instructions below to run the Streamlit server locally.

### Pre-requisites

Make sure you have Python ≥3.10 installed.

### Steps

1. Clone the repository

```bash
git clone https://github.com/fm1320/song-vibe
cd song-vibe
```

2. Install dependencies from requirements file

```bash
pip install requirments.txt
```

3. (For Training a new index) The file  `data.csv` is an example of what the training data of song descriptions looks like. This training data has been synthetically generated by prompting an LLM.
   By running `train.py` the song descriptions are encoded by a transformer network and a vector index file `index.bin` using FAISS is created. Currenlty a flat index is used.

> **Note:** Make sure you have a paid OpenAI API key for faster completions and to avoid hitting rate limits.

4. Run the Streamlit server

```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser to access the app.

## Tech Stack

- User Interface - [Streamlit](https://streamlit.io/)
- Index search - [FAISS](https://github.com/facebookresearch/faiss)
- Sentence Transformers - [SBERT](https://www.sbert.net/)

## Roadmap


- *coming soon*: Full web app using Spotify API and more songs
- Support and add more synthetic song descriptions 
- Support for more transformer encoders and indices

## Contributing

All contributions are welcome!

## License

Free to use, star, share, and acknowledge use if you can!
