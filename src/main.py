import os
from dotenv import load_dotenv
from core.command_router import CommandRouter
from core.command_matcher import CommandMatcher
from core.nlp_parser import NLPCommandParser
import importlib.util


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
}

nlp_parser = NLPCommandParser(nlp_map)

def say_hello():
    """Say hello to the user."""
    print("Hello from Pizza!")

def say_goodbye():
    """Say goodbye to the user."""
    print("Goodbye from Pizza!")
    return False  # Return False to indicate exit

router.register("hello", say_hello)
router.register("exit", say_goodbye)
router.register("quit", say_goodbye)


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

load_plugins(router)
command_matcher = CommandMatcher(router.commands.keys())

# Assistant loop
if __name__ == "__main__":
    print(
        "Welcome to Pizza! Type 'hello' to greet or 'exit'/'quit' to leave."
        )
    while True:
        try:
            cmd = input("> ")

            result = None

            # Step 1: try command matcher
            matched = command_matcher.match(cmd)
            if matched:
                print(f"Interpreted as: {matched}")
                result = router.handle(matched)
            else:
                # Step 2: try NLP parser
                parsed = nlp_parser.parse(cmd)
                if parsed:
                    print(f"Interpreted as: {parsed}")
                    result = router.handle(parsed)
                else:
                    print("Command not recognized.")


            if result is False:
                break

        except KeyboardInterrupt:
            print("\nExiting...")
            break