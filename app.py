import pandas as pd
from dotenv import find_dotenv, load_dotenv

from src.database_operations import DatabaseOps

database = DatabaseOps()
database.connect_db()

env = find_dotenv()
load_dotenv(env);


def get_tracks():
    query = """select * from staging.top_10_tracks"""
    return database.run_query(query)

def get_artists():
    query = """select * from trusted.top_10_artists"""
    return database.run_query(query)

def get_user_info():
    query = """select * from staging.user_info"""
    return database.run_query(query)

tracks = get_tracks()
user = get_user_info()
artists = get_artists()

from collections import Counter

genres_list = artists['GENRES'].str.split(', ')

# Contar a frequência de cada gênero
genre_counts = Counter([genre for genres in genres_list for genre in genres])

# Converter o resultado em um DataFrame
result = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['FREQ'])

top_5_generos = result.sort_values('FREQ', ascending=False)[:5]


import streamlit as st

from PIL import Image
import requests
from io import BytesIO

response = requests.get(user['0'][0])
img = Image.open(BytesIO(response.content))



# Configurar a página do Streamlit
st.set_page_config(layout="wide")

st.title("MY SPOTIFY RETROSPECTIVE")
st.markdown(f"# Me: {user['display_name'].values[0]}")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.image(img)

with c2:
    st.info("TOP TRACKS")
    for i in range(5):
        st.write(f"{i+1}. {tracks['NAME'][i]} by {tracks['ARTIST'][i]}")

with c3:
    st.info("TOP ARTISTS")
    for i in range(5):
        st.write(f"{i+1}. {artists['NAME'][i]}")

with c4:
    st.info('TOP GENRES')
    for i in range(5):
        st.write(f"{i+1}. {top_5_generos.iloc[i].name}")