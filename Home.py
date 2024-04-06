from helpers import recommend_song
import streamlit as st
import spotipy
from spotipy import SpotifyClientCredentials

st.set_page_config(layout="wide")

st.title("The Song Recommender")
st.write("---")
col1, col2 = st.columns([.5, .5])
client_id = col1.text_input('Client ID')
client_secret = col2.text_input('Client Secret')
if client_id and client_secret:
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
else:
    st.stop()
st.write("---")
col1, col2 = st.columns([.5, .5])
song = col1.text_input('Song')
artist = col2.text_input('Artist')
st.write("---")
if artist and song:
    song_recommended = recommend_song(sp, song, artist)
else:
    st.stop()
st.header(song_recommended, divider='rainbow')