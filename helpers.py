import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances_argmin_min
import streamlit as st

scaled_df = pd.read_csv("data/songs_final.csv")

with open("data/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("data/kmeans.pkl", "rb") as f:
    kmeans = pickle.load(f)

def recommend_song(sp, song, artist):
    cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    # get song id
    results = sp.search(q=f'track:{song} - {artist}', limit=1)
    track_id = results['tracks']['items'][0]['id']
    # get song features with the obtained id
    audio_features = sp.audio_features(track_id)
    # create dataframe
    df_ = pd.DataFrame(audio_features)
    new_features = df_[cols]
    # scale features
    scaled_x = scaler.transform(new_features)
    # predict cluster
    cluster = kmeans.predict(scaled_x)
    # filter dataset to predicted cluster
    filtered_df = scaled_df[scaled_df['cluster'] == cluster[0]]
    filtered_array = np.array(filtered_df[cols], order="C")
    # get closest song from filtered dataset
    closest, _ = pairwise_distances_argmin_min(scaled_x, filtered_array)
    # return it in a readable way
    return ' - '.join([filtered_df.iloc[closest]['song name'].values[0], filtered_df.iloc[closest]['artist'].values[0]])