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
        scope="user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"
    ))

    def play_music():
        """Try to resume Spotify playback, or fall back to playing a new song."""
        devices = sp.devices().get("devices", [])
        if not devices:
            print("❌ No Spotify devices found. Open Spotify and start playing something.")
            return

        active_device = next((d for d in devices if d["is_active"]), None)

        if not active_device:
            print("❌ No active device. Start Spotify and play a song manually first.")
            return

        try:
            print(f"▶️ Trying to resume playback on: {active_device['name']}")
            sp.start_playback(device_id=active_device["id"])
        except Exception as e:
            if "Restriction violated" in str(e):
                print("⚠️ Cannot resume playback. You may need to choose a specific song.")
                fallback = input("🎵 Enter a song to play instead > ").strip()
                if not fallback:
                    print("❌ No song entered.")
                    return
                play_song(fallback)
            else:
                print(f"⚠️ Failed to resume playback: {e}")


    def pause_music():
        """Pause music on Spotify."""
        try:
            print("⏸️  Pausing playback...")
            sp.pause_playback()
        except Exception as e:
            print(f"⚠️  Failed to pause playback: {e}")

    def play_song(query=None):
        """Search and play a specific song on the selected or active device."""
        if query:
            query = query.strip()
            print(f"🎵 Searching for: {query}")
        else:
            query = input("What song would you like to play? > ").strip()
            if not query:
                print("❌  No song specified.")
                return

        results = sp.search(q=query, type="track", limit=3)
        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            print("❌  No matching tracks found.")
            return

        # Let user choose from top 3 matches
        if len(tracks) > 1:
            print("🎧 Multiple tracks found:")
            for i, track in enumerate(tracks, start=1):
                name = track["name"]
                artist = track["artists"][0]["name"]
                print(f"{i}. {name} by {artist}")
            choice = input("🔢  Choose a track by number (or press Enter to cancel): ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(tracks)):
                print("⚠️  Invalid choice or cancelled.")
                return
            track = tracks[int(choice) - 1]
        else:
            track = tracks[0]

        uri = track["uri"]
        name = track["name"]
        artist = track["artists"][0]["name"]
        print(f"▶️ Playing '{name}' by {artist}...")

        devices = sp.devices().get("devices", [])
        if not devices:
            print("❌  No Spotify devices available. Open Spotify on a device first.")
            return

        active_device = next((d for d in devices if d["is_active"]), None)
        if active_device:
            device_id = active_device["id"]
            print(f"📡 Using active device: {active_device['name']}")
        else:
            print("❔ No active device found. Available devices:")
            for idx, d in enumerate(devices):
                print(f"{idx + 1}. {d['name']} (type: {d['type']})")
            choice = input("🔢 Choose a device by number (or press Enter to cancel): ").strip()
            if not choice.isdigit() or not (1 <= int(choice) <= len(devices)):
                print("⚠️  Invalid device or cancelled.")
                return
            device_id = devices[int(choice) - 1]["id"]

        try:
            sp.start_playback(device_id=device_id, uris=[uri])
        except Exception as e:
            print(f"⚠️  Failed to start playback: {e}")

    
    def now_playing():
        """Get the currently playing track on Spotify."""
        try:
            playback = sp.current_playback()
            if not playback or not playback.get("is_playing"):
                print("🛑 Nothing is currently playing.")
                return
            
            item = playback.get["item"]
            device = playback["device"]

            name = item["name"]
            artist = item["artists"][0]["name"]
            device_name = device["name"]
            device_type = device["type"]

            print(f"🎶 Now playing '{name}'\nby {artist}\non {device_name} ({device_type})")
        except Exception as e:
            print(f"⚠️  Failed to get current playback: {e}")


    router.register("spotify_play", play_music)
    router.register("spotify_pause", pause_music)
    router.register("spotify_play_song", play_song)
    router.register("spotify_now_playing", now_playing)
