import requests
import base64
import pandas as pd
import os
from dotenv import find_dotenv, load_dotenv

from src.database_operations import DatabaseOps
from src.spotify_api import SpotifyAPI
database = DatabaseOps()
database.connect_db()


env = find_dotenv()
load_dotenv(env)


api = SpotifyAPI()


parameters = {
    'time_range': 'long_term',  # Período de tempo: short_term, medium_term, long_term
    'limit': 10,  # Número máximo de principais faixas a serem retornadas
    'offset': 0  # Deslocamento para resultados de pesquisa paginados (opcional)
}

top_10_tracks = api.user_top_tracks(parameters)

parameters = {
    'time_range': 'long_term',
    'limit': 10
}

top_10_artists = api.user_top_artist(parameters)

user_info = api.user_info()

database.insert(dataframe=top_10_tracks, schema='trusted', table='top_10_tracks', if_exists='replace')
database.insert(dataframe=top_10_artists, schema='trusted', table='top_10_artists', if_exists='replace')
database.insert(dataframe=user_info, schema='trusted', table='user_info', if_exists='replace')