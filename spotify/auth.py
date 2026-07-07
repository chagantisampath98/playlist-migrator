import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()

SCOPES = "playlist-read-private playlist-read-collaborative"


def get_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
            scope=SCOPES,
        )
    )