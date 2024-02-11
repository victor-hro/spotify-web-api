import pandas as pd
from dotenv import find_dotenv, load_dotenv
from utils.database_operations import DatabaseOps
from utils.spotify_api import SpotifyAPI

# Initial Settings
database = DatabaseOps()
database.connect_db()

env = find_dotenv()
load_dotenv(env)

api = SpotifyAPI()


# Extract Data
## user top tracks
parameters = {
    'time_range': 'long_term',  # Período de tempo: short_term, medium_term, long_term
    'limit': 10,  # Número máximo de principais faixas a serem retornadas
    'offset': 0  # Deslocamento para resultados de pesquisa paginados (opcional)
}

top_10_tracks = api.user_top_tracks(parameters)


## user info
user_info = api.user_info()
user_img = pd.DataFrame([user_info['images'][0][1]['url']])
user_info = pd.concat([user_info[['display_name']], user_img], axis=1)


## user top artists
parameters = {
    'time_range': 'long_term',
    'limit': 10
}

top_10_artists = api.user_top_artist(parameters)


## artist info
# Creating an empty DataFrame
top_10_artists_info = pd.DataFrame()

# Looping through the top 10 artists and obtaining their information
for artist_ in top_10_artists[:10].NAME.to_list():
    # Getting artist information using the 'get_artist_info' method from the 'api' object
    # Concatenating the obtained artist information into the 'top_10_artists_info' DataFrame
    top_10_artists_info = pd.concat([top_10_artists_info, api.get_artist_info(artist_)], ignore_index=True)

# Extracting and replacing the 'Imagens' column values with the URL
top_10_artists_info['IMAGE'] = top_10_artists_info['IMAGE'].apply(lambda x: x[1]['url'] if len(x) > 1 and len(x[1]) > 1 else None)


# Insert Database
database.insert(dataframe=top_10_tracks, schema='feature_store', table='top_10_tracks', if_exists='replace')
database.insert(dataframe=top_10_artists, schema='feature_store', table='top_10_artists', if_exists='replace')
database.insert(dataframe=top_10_artists_info, schema='feature_store', table='top_10_artists_info', if_exists='replace')
database.insert(dataframe=user_info, schema='feature_store', table='user_info', if_exists='replace')

# Load data - streamlit app
top_10_tracks.to_csv(r'./data/top_10_tracks.csv', index=None)
top_10_artists.to_csv(r'./data/top_10_artists.csv', index=None)
top_10_artists_info.to_csv(r'./data/top_10_artists_info.csv', index=None)
user_info.to_csv(r'./data/user_info.csv', index=None)