from unittest.mock import patch
from pizza.core.agent_router import create_agent_with_tools

@patch("pizza.plugins.spotify_plugin.play_song")
def test_agent_handles_play_song(mock_play_song):
    """Test that the agent selects the correct tool to play a song."""
    mock_play_song.return_value = "▶️ Playing 'Imagine' by John Lennon"

    agent = create_agent_with_tools()
    response = agent.run("play Imagine by John Lennon")

    mock_play_song.assert_called_once()
    called_arg = mock_play_song.call_args[0][0]
    assert "Imagine" in called_arg and "John Lennon" in called_arg
