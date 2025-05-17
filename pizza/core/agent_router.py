from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_ollama import ChatOllama
from langchain.tools import tool

from pizza.plugins import spotify_plugin


def get_ollama_llm(model_name="mistral"):
    """Returns an Ollama LLM instance."""
    return ChatOllama(model=model_name)


def create_agent_with_tools(tools=None, model="mistral"):
    """Creates an agent with the given tools and Ollama LLM."""
    llm = get_ollama_llm(model)
    tools = tools or get_all_tools()

    # Filter only tools that are single input (for ZeroShotAgent)
    single_input_tools = [tool for tool in tools if tool.is_single_input]

    return initialize_agent(
        tools=single_input_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )



# TOOL WRAPPERS
@tool
def agent_play_song(song_name: str) -> str:
    """Play a specific song by name using Spotify."""
    return spotify_plugin.play_song(song_name)


@tool
def agent_pause() -> str:
    """Pause current Spotify playback."""
    return spotify_plugin.pause_music()


@tool
def agent_resume() -> str:
    """Resume Spotify playback."""
    return spotify_plugin.resume_music()


@tool
def agent_now_playing() -> str:
    """Show the currently playing song and device."""
    return spotify_plugin.now_playing()


@tool
def agent_play_playlist(name: str) -> str:
    """Play a playlist by name from your Spotify library."""
    return spotify_plugin.play_playlist(name)


@tool
def agent_recent_playlists(limit: int = 3) -> str:
    """Show the last few recently played playlists."""
    return spotify_plugin.recent_playlists(limit)


@tool
def agent_list_playlists() -> str:
    """List the top 10 playlists from your Spotify account."""
    return spotify_plugin.list_my_playlists()


def get_all_tools():
    """Returns all registered Spotify agent tools."""
    return [
        agent_play_song,
        agent_pause,
        agent_resume,
        agent_now_playing,
        agent_play_playlist,
        agent_recent_playlists,
        agent_list_playlists
    ]
