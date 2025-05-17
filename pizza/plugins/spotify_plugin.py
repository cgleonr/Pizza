# src/plugins/spotify_plugin.py

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from pizza.config.env_loader import load_settings

_sp = None  # global Spotify client instance


def init_spotify():
    """Initialize or reuse Spotify client."""
    global _sp
    if _sp is None:
        settings = load_settings()
        _sp = Spotify(auth_manager=SpotifyOAuth(
            client_id=settings["SPOTIFY_CLIENT_ID"],
            client_secret=settings["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=settings["SPOTIFY_REDIRECT_URI"],
            scope="user-read-playback-state user-modify-playback-state user-read-currently-playing streaming"
        ))
    return _sp


def play_song(query=None) -> str:
    sp = init_spotify()

    if not query:
        query = input("🎵 What song would you like to play? > ").strip()
        if not query:
            return "❌ No song specified."

    results = sp.search(q=query, type="track", limit=3)
    tracks = results.get("tracks", {}).get("items", [])

    if not tracks:
        return "❌ No matching tracks found."

    track = tracks[0]  # Default to the first track
    uri = track["uri"]
    name = track["name"]
    artist = track["artists"][0]["name"]

    devices = sp.devices().get("devices", [])
    if not devices:
        return "❌ No Spotify devices available. Open Spotify first."

    active_device = next((d for d in devices if d["is_active"]), None)
    device_id = active_device["id"] if active_device else devices[0]["id"]

    try:
        sp.start_playback(device_id=device_id, uris=[uri])
        return f"▶️ Playing '{name}' by {artist}"
    except Exception as e:
        return f"⚠️ Failed to play song: {e}"


def pause_music() -> str:
    sp = init_spotify()
    try:
        sp.pause_playback()
        return "⏸️ Playback paused."
    except Exception as e:
        return f"⚠️ Failed to pause playback: {e}"


def resume_music() -> str:
    sp = init_spotify()
    try:
        sp.start_playback()
        return "▶️ Playback resumed."
    except Exception as e:
        return f"⚠️ Failed to resume playback: {e}"


def now_playing() -> str:
    """Displays whichever song is currently playing on the active device,
      as well as what device it is playing on"""
    sp = init_spotify()
    try:
        playback = sp.current_playback()
        if not playback or not playback.get("is_playing"):
            return "🛑 Nothing is currently playing."

        item = playback["item"]
        device = playback["device"]

        name = item["name"]
        artist = item["artists"][0]["name"]
        device_name = device["name"]
        device_type = device["type"]

        return f"🎶 Now playing '{name}'\nby {artist}\non {device_name} ({device_type})"
    except Exception as e:
        return f"⚠️ Failed to get current playback: {e}"

def play_playlist(name: str) -> str:
    """Plays the specified laylist by name from the user's library
    (created or followed)"""
    sp = init_spotify()
    playlists = sp.current_user_playlists(limit=50)["items"]

    match = next(
        (pl for pl in playlists if name.lower() in pl["name"].lower()), None
    )
    if not match:
        return f"❌ Playlist '{name}' not found in your library."

    uri = match["uri"]
    sp.start_playback(context_uri=uri)
    return f"▶️ Playing playlist: {match['name']}"

def recent_playlists(limit: int = 3) -> str:
    """Displays up to 3 recently played playlists based on playback context
     from spotify API"""
    sp = init_spotify()
    recent = sp.current_user_recently_played(limit=50)["items"]

    seen = {}
    for item in recent:
        context = item.get("context")
        if context and context["type"] == "playlist":
            uri = context["uri"]
            if uri not in seen:
                seen[uri] = item["track"]["name"]

        if len(seen) >= limit:
            break

    if not seen:
        return "❌ No recently played playlists found."

    response = "🕓 Recently played playlists:\n"
    for i, (uri, track_name) in enumerate(seen.items(), 1):
        response += f"{i}. Playlist URI: {uri} (from track: {track_name})\n"
    return response.strip()

def list_my_playlists() -> str:
    """Lists 10 of the user's playlists (created or saved)"""
    sp = init_spotify()
    playlists = sp.current_user_playlists(limit=10)["items"]
    if not playlists:
        return "You don’t have any playlists."

    return "\n".join(
        [f"{i+1}. {pl['name']}" for i, pl in enumerate(playlists)]
    )




def register(router):
    """For router support"""
    router.register("spotify_play", resume_music)
    router.register("spotify_pause", pause_music)
    router.register("spotify_play_song", play_song)
    router.register("spotify_now_playing", now_playing)
    router.register("spotify_play_playlist", play_playlist)
    router.register("spotify_recent_playlists", recent_playlists)
    router.register("spotify_list_playlists", list_my_playlists)

__all__ = ["play_song"]