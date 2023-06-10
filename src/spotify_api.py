import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pandas as pd

class SpotifyAPI:
    def __init__(self):
        self.api_root = 'https://api.spotify.com/v1'
        
        # Define your Spotify credentials
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.redirect_uri = 'http://localhost:5000/callback'  # Altere para a sua redirect_uri

        # Inicializar a instância de autenticação
        self.auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope='user-library-read user-top-read'  # Escopo das permissões necessárias
        )

        auth_url = self.auth_manager.get_authorize_url()

        print('Auth URL:', auth_url)
        # Solicitar o código de autorização do usuário
        authorization_code = input('Código de autorização:')
        
        # Obter o token de acesso usando o código de autorização
        token_info = self.auth_manager.get_access_token(authorization_code)
        
        # Verificar se o token de acesso foi obtido com sucesso
        if token_info:
            print('Token de acesso obtido com sucesso!')
            if self.auth_manager.is_token_expired(token_info):
                print('Token de acesso expirado.')
            else:
                print('Token de acesso válido.')
                # Conectar usando spotipy.Spotify()
                self.spotify_api = spotipy.Spotify(auth=token_info['access_token'])
        else:
            print('Falha ao obter o token de acesso.')

    
    def user_info(self):
        # Exemplo: obter informações do usuário
        user_info = self.spotify_api.current_user()
        return pd.DataFrame.from_dict(user_info, orient='index').T
    

    def user_top_tracks(self, parameters):
        top_tracks = self.spotify_api.current_user_top_tracks(**parameters)

        tracks_data = []

        # Exibir as principais músicas
        for i, track in enumerate(top_tracks['items'], start=1):
            track_data = {
                'RANKING': i,
                'NAME': track['name'],
                'ARTIST': track['artists'][0]['name']
            }
            tracks_data.append(track_data)

        return pd.DataFrame(tracks_data)

    def user_top_artist(self, parameters):
        top_artists = self.spotify_api.current_user_top_artists(**parameters)

        artists_data = []

        for i, artist in enumerate(top_artists['items'], start=1):
            artist_data = {
                'RANKING': i,
                'NAME': artist['name'],
                'GENRES': ', '.join(artist['genres']),
                'POPULARITY': artist['popularity']
            }
            artists_data.append(artist_data)

        return pd.DataFrame(artists_data)