import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

year = input("Enter the year : ")

url = f"https://www.billboard.com/charts/hot-100/{year}-08-21/"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')
table = soup.select("li ul li h3")
songs = []
for x in table:
    songs.append(x.getText().strip())

print(songs)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=config.client_id,
        client_secret=config.client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)
playlist = []
for key in songs:
    spotify_result = sp.search(q=f"track:{key}", type="track")
    try:
        song_uri = spotify_result['tracks']['items'][0]['uri']
        playlist.append(song_uri)
    except IndexError:
        print(f"{key} doesn't exist in Spotify. Skipped.")

print(playlist)
my_playlist = sp.user_playlist_create(user=f"{user_id}", name=f"Billboard Top Tracks {year}", public=False)
sp.playlist_add_items(playlist_id=my_playlist["id"], items=playlist)