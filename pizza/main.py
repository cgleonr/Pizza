import sys
import os
sys.path.append(os.path.dirname(__file__))
from dotenv import load_dotenv
from pizza.core.command_router import CommandRouter
from pizza.core.command_matcher import CommandMatcher
from pizza.core.nlp_parser import NLPCommandParser
import importlib.util
from pizza.core.agent_router import create_agent_with_tools, play_song


load_dotenv()

router = CommandRouter()
nlp_map = {
    "greet": "hello",
    "exit": "exit",
    "introduce": "hello",
    "quit": "exit",
    "play": "spotify_play",
    "pause": "spotify_pause",
    "music": "spotify_play",   # fallback match
    "song": "spotify_play_song",
    "track": "spotify_play_song",
    "playing": "spotify_now_playing",
    "now": "spotify_now_playing",
    "current": "spotify_now_playing",
    "help": "help",
    "assist": "help",
    "what can you do": "help",
    "recent": "spotify_recent_playlists",
    "last": "spotify_recent_playlists",
    "playlists": "spotify_list_playlists",
    "my playlists": "spotify_list_playlists",
    "favorite": "spotify_play_playlist",


}

nlp_parser = NLPCommandParser(nlp_map)

def say_hello():
    """Say hello to the user."""
    print("Hello from Pizza!")

def say_goodbye():
    """Say goodbye to the user."""
    print("Goodbye from Pizza!")
    return False  # Return False to indicate exit

def load_plugins(router, plugin_folder="plugins"):
    """Load plugins from the specified folder 'src/plugins/' and
    register their commands."""
    plugin_path = os.path.join(os.path.dirname(__file__), plugin_folder)
    for filename in os.listdir(plugin_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(plugin_path, filename)

            spec = importlib.util.spec_from_file_location(
                module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "register"):
                # Call the register function in the plugin module
                module.register(router)
                print(f"Loaded plugin: {module_name}")
            else:
                print(f"Skipped {module_name}: no 'register()' function.")

def show_help():
    """Display all available commands and their descriptions."""
    print("\n🧠 Available Commands:\n")

    for name in router.commands:
        func = router.commands[name]
        doc = func.__doc__.strip() if func.__doc__ else "No description provided."
        print(f"🔹 {name:<20} — {doc}")

    print("\nTry saying things like:")
    print("  • play Smooth Operator")
    print("  • pause")
    print("  • now playing")
    print("  • hello")
    print("  • quit\n")
    

load_plugins(router)
command_matcher = CommandMatcher(
    router.commands.keys(),
    aliases={
        "now playing": "spotify_now_playing",
        "what's playing": "spotify_now_playing",
        "current song": "spotify_now_playing",
        "help": "help",
        "assist": "help",
        "what can you do": "help",
        
    }
)


router.register("hello", say_hello)
router.register("exit", say_goodbye)
router.register("quit", say_goodbye)
router.register("help", show_help)

tools = [play_song]
agent = create_agent_with_tools(tools)




# Assistant loop
if __name__ == "__main__":
    print(
        "Welcome to Pizza! Type 'hello' to greet or 'exit'/'quit' to leave."
        )
    while True:
        try:
            cmd = input("> ")

            result = None

            # Step 1: Try the agent first
            try:
                response = agent.run(cmd)
                print(f"🧠 Agent: {response}")
            except Exception as e:
                print(f"⚠️ Agent failed: {e}")
                print("🔁 Trying command matcher...")

                # Step 2: Try command matcher
                matched = command_matcher.match(cmd)
                if matched:
                    print(f"🔍 Interpreted as: {matched}")
                    result = router.handle(matched)
                else:
                    # Step 3: Try NLP parser
                    parsed = nlp_parser.parse(cmd)
                    if parsed:
                        print(f"🧠 NLP interpreted as: {parsed}")
                        if parsed == "spotify_play_song":
                            query = nlp_parser.extract_song_query(cmd)
                            if query:
                                print(f"🎵 Extracted query: '{query}'")
                                result = router.handle(parsed, query=query)
                            else:
                                result = router.handle(parsed)
                        else:
                            result = router.handle(parsed)
                    else:
                        print("❌ Could not understand command.")

            if result is False:
                break

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
