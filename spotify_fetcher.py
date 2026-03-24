import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class SpotifyDataEngine:
    def __init__(self):
        auth_manager = SpotifyClientCredentials(
            client_id=os.getenv('435b153e416440b793f0d826ee012ce6'),
            client_secret=os.getenv('d101d92af3e646e495305ea659620aeb')
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_tour_audio_features(self, album_id, era_label):
        print(f"Extracting audio signals for {era_label}...")
        tracks = self.sp.album_tracks(album_id)['items']
        data = []
        for track in tracks:
            f = self.sp.audio_features(track['id'])[0]
            if f:
                f.update({
                    'track_name': track['name'],
                    'era': era_label,
                    'is_stadium_engineered': 1 if f['energy'] > 0.7 else 0
                })
                data.append(f)
        return pd.DataFrame(data)

# Test run for 2018 Baseline
if __name__ == "__main__":
    engine = SpotifyDataEngine()
    # Love Yourself: Answer Album ID
    df = engine.get_tour_audio_features('292789c8-5535-492d-a25c-9f58803e027f', 'LY_2018')
    df.to_csv('spotify_signals.csv', index=False)
