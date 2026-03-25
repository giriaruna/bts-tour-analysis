import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

auth_manager = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
    )
sp = spotipy.Spotify(auth_manager=auth_manager)


album_id = "43wFM1HquliY3iwKWzPN4y"

# fetch all tracks (handle pagination)
results = sp.album_tracks(album_id)
tracks = results['items']

while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])

# Extract only metadata
data = []
for t in tracks:
    data.append({
        "track_name": t['name'],
        "track_id": t['id'],
        "duration_ms": t['duration_ms'],
        "track_number": t['track_number'],
        "explicit": t['explicit'],
        "artists": ", ".join([a['name'] for a in t['artists']])
    })

df = pd.DataFrame(data)
df.to_csv("spotify_album_metadata.csv", index=False)


# test out search markets 
market_results = sp.search_markets(
    q="BTS",
    type="track",
    limit=5,
    markets=["BR", "KR", "FR"]
)

for market, data in market_results.items():
    print(f"\nMarket: {market}")
    for track in data['tracks']['items']:
        print( track['name'],
              track['album']['name'],
            track["album"]["release_date"],
    track["album"]["release_date_precision"],
     track['is_playable'] )
