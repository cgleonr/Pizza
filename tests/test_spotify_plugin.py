from unittest.mock import patch, MagicMock
from pizza.core.command_router import CommandRouter
from pizza.plugins import spotify_plugin

@patch("builtins.input", return_value="Imagine Dragons Believer")
@patch("plugins.spotify_plugin.Spotify")
@patch("plugins.spotify_plugin.SpotifyOAuth")
@patch("plugins.spotify_plugin.load_settings")
def test_spotify_plugin_register_commands(
    mock_load_settings,
    mock_spotify_oauth,
    mock_spotify_class,
    mock_input,
    ):
    """Test the registration of Spotify commands in the plugin."""
    # Mock env settings
    mock_load_settings.return_value = {
        "SPOTIFY_CLIENT_ID": "test_id",
        "SPOTIFY_CLIENT_SECRET": "test_secret",
        "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8888/callback"
    }

    # Mock spotify client instance
    mock_spotify = MagicMock()
    mock_spotify_class.return_value = mock_spotify

    #Simulate a spotify track search result
    mock_spotify.search.return_value = {
        "tracks": {
            "items": [
                {
                    "uri": "spotify:track:1234",
                    "name": "Believer",
                    "artists": [{"name": "Imagine Dragons"}]
                }
            ]
        }
    }

    # Set up router
    router = CommandRouter()

    # Register the plugin
    spotify_plugin.register(router)

    # Test "spotify_play"
    router.handle("spotify_play")

    # Test "spotify_pause"
    router.handle("spotify_pause")
    mock_spotify.pause_playback.assert_called_once()

    # Test "spotify_play_song"
    router.handle("spotify_play_song")
    mock_spotify.search.assert_called_once_with(
        q="Imagine Dragons Believer", type="track", limit=1
        )
    #Verify start_playback was called twice (once for play, once for play_song)
    assert mock_spotify.start_playback.call_count == 2
    mock_spotify.start_playback_asser_any_call()
    mock_spotify.start_playback_asser_any_call(uris=["spotify:track:1234"])