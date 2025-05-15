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
        scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"
    ))

    
    def play_music(query=None):
        """Search and play a specific song on Spotify."""

        # Step 1: Ask for the song name if it wasn't passed in
        if not query:
            query = input("🎵 What song would you like to play? > ").strip()
            if not query:
                print("❌ No song specified.")
                return

        # Step 2: Search for the track
        results = sp.search(q=query, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            print("❌ No tracks found.")
            return

        track = tracks[0]
        uri = track["uri"]
        name = track["name"]
        artist = track["artists"][0]["name"]
        print(f"🎧 Found: {name} by {artist}")

        # Step 3: Get devices
        devices = sp.devices().get("devices", [])
        if not devices:
            print("❌ No Spotify devices available. Open Spotify on your phone or computer first.")
            return

        # Step 4: Try active device first
        active_device = next((d for d in devices if d["is_active"]), None)
        target_device_id = None

        if active_device:
            target_device_id = active_device["id"]
            print(f"📡 Using active device: {active_device['name']}")
        else:
            # If no device is active, list devices and ask the user
            print("❔ No active device found. Available devices:")
            for idx, d in enumerate(devices):
                print(f"{idx + 1}. {d['name']} (type: {d['type']})")

            choice = input("🔢 Choose a device by number (or press Enter to cancel): ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(devices)):
                print("⚠️ Invalid choice or cancelled.")
                return

            target_device_id = devices[int(choice) - 1]["id"]

        # Step 5: Play the track
        try:
            print(f"▶️ Playing '{name}' by {artist}...")
            sp.start_playback(device_id=target_device_id, uris=[uri])
        except Exception as e:
            print(f"⚠️ Failed to start playback: {e}")




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