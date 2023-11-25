import pandas as pd
from dotenv import find_dotenv, load_dotenv
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from collections import Counter
from utils.database_operations import DatabaseOps

# Database connection
database = DatabaseOps()
database.connect_db()

env = find_dotenv()
load_dotenv(env)

from pathlib import Path
import os

import pandas as pd



# Functions to retrieve data from the database or CSV file based on db_access parameter
def get_tracks(db_access=False):
    """
    Retrieve top 10 tracks data either from a database or a CSV file.

    Args:
        db_access (bool): Indicates whether database access is available.

    Returns:
        pandas.DataFrame: DataFrame containing top 10 tracks data.
    """
    if db_access:
        # Replace this with actual database query
        return database.run_query("SELECT * FROM feature_store.top_10_tracks")
    else:
        # Encontrar o diretório raiz do projeto
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        file_path = os.path.join(data_dir, 'top_10_tracks.csv')
        
        return pd.read_csv(file_path)

def get_artists(db_access=False):
    """
    Retrieve top 10 artists data from the database.

    Args:
        db_access (bool): Indicates whether database access is available.

    Returns:
        pandas.DataFrame: DataFrame containing top 10 artists data.
    """
    if db_access:
        # Replace this with actual database query
        return database.run_query("SELECT * FROM feature_store.top_10_artists")
    else:
        # Encontrar o diretório raiz do projeto
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        file_path = os.path.join(data_dir, 'top_10_artists.csv')
        
        return pd.read_csv(file_path)
    
def get_user_info(db_access=False):
    """
    Retrieve user info from the database.

    Args:
        db_access (bool): Indicates whether database access is available.

    Returns:
        pandas.DataFrame: DataFrame containing user info.
    """
    if db_access:
        # Replace this with actual database query
        return database.run_query("SELECT * FROM feature_store.user_info")
    else:
        # Encontrar o diretório raiz do projeto
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        file_path = os.path.join(data_dir, 'user_info.csv')
        
        return pd.read_csv(file_path)

def get_artists_info(db_access=False):
    """
    Retrieve top 10 artists' additional information from the database.

    Args:
        db_access (bool): Indicates whether database access is available.

    Returns:
        pandas.DataFrame: DataFrame containing additional info for top 10 artists.
    """
    if db_access:
        # Replace this with actual database query
        return database.run_query("SELECT * FROM feature_store.top_10_artists_info")
    else:
        # Encontrar o diretório raiz do projeto
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        file_path = os.path.join(data_dir, 'top_10_artists_info.csv')
        
        return pd.read_csv(file_path)

# Streamlit interface setup
st.set_page_config(layout="wide")

# Retrieve data
tracks = get_tracks()
user = get_user_info()
artists = get_artists()
artists_info = get_artists_info()


# Count genre frequency
genres_list = artists['GENRES'].str.split(', ')
genre_counts = Counter([genre for genres in genres_list for genre in genres])
result = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['FREQ'])
top_5_genres = result.sort_values('FREQ', ascending=False)





# Display user info and image
# spotify_icon = Image.open('../images/logo.png')
# st.image(spotify_icon, width=100)  # Adicionando o ícone do Spotify
st.title(f"{user['display_name'].values[0]} Spotify Retrospective ")
st.write('--'*50)

response = requests.get(user['0'][0])
img = Image.open(BytesIO(response.content))
st.image(img)


# Display top tracks, artists, and genres
col1, col2, col3 = st.columns(3)

with col1:
    st.info("🌟 TOP TRACKS")
    for i in range(10):
        st.write(f"{i+1}. {tracks['NAME'][i]} by {tracks['ARTIST'][i]}")

with col2:
    st.info("🌟 TOP ARTISTS")
    for i in range(10):
        st.write(f"{i+1}. {artists['NAME'][i]}")

with col3:
    st.info('🌟 TOP GENRES')
    for i in range(10):
        st.write(f"{i+1}. {top_5_genres.index[i]}")

st.write('--'*50)
st.title('🔥 Artists Info')
st.write('--'*50)
# Display top artists info
for _, artist_data in artists_info.iterrows():
    artist_name = artist_data['NAME']
    artist_image_url = artist_data['IMAGE']
    artist_genres = artist_data['GENRES']
    artist_popularity = artist_data['POPULARITY']
    artist_spotify_url = artist_data['LINK SPOTIFY']
    artist_followers = artist_data['FOLLOWERS']

    st.info(f"## {artist_name}")

    col1, col2 = st.columns([2, 3])

    with col1:
        response = requests.get(artist_image_url)
        artist_img = Image.open(BytesIO(response.content))
        st.image(artist_img, width=300)
        st.write(f"[Open in Spotify]({artist_spotify_url})")

    with col2:
        for c in range(3):
            st.write('')
        st.write(f"**Genres:** {(artist_genres)}")
        st.write('--'*10)
        st.write(f"**Popularity:** {artist_popularity}")
        st.write('--'*10)
        st.write(f"**Followers:** {artist_followers}")
        st.write('--'*10)

    st.markdown("---")  # Adds a horizontal line between artist info sections
