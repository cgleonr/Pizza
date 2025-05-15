from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from config.env_loader import load_settings

def register(router):
    """Register commands with the command router."""
    settings = load_settings()

    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=settings["SPOTIFY_CLIENT_ID"],
        client_secret=settings["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=settings["SPOTIFY_REDIRECT_URI"],
        scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
    ))

    def play_music():
        """Play music on Spotify."""
        print("Playing music on Spotify...")
        sp.start_playback()

    def pause_music():
        """Pause music on Spotify."""
        print("Pausing playback")
        sp.pause_playback()

    def play_song():
        """Play a specific song on Spotify."""
        query = input("What song would you like to play? > ").strip()
        if not query:
            print("No song specified.")
            return
        
        results = sp.search(q=query, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            print("No tracks found.")
            return
        
        track = tracks[0]
        uri = track["uri"]
        name = track["name"]
        artist = track["artists"][0]["name"]
        print(f"Playing {name} by {artist}...")
        sp.start_playback(uris=[uri])

    router.register("spotify_play_song", play_song)
    router.register("spotify_play", play_music)
    router.register("spotify_pause", pause_music)