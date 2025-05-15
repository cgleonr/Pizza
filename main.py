import os
from dotenv import load_dotenv
from core.command_router import CommandRouter
import importlib.util


load_dotenv()

router = CommandRouter()

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
    """Load plugins from the specified folder and
    register their commands."""
    for filename in os.listdir(plugin_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            file_path = os.path.join(plugin_folder, filename)

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

# Assistant loop
if __name__ == "__main__":
    print(
        "Welcome to Pizza! Type 'hello' to greet or 'exit'/'quit' to leave."
        )
    while True:
        try:
            cmd = input("> ")
            result = router.handle(cmd)
            if result is False:
                break
        except KeyboardInterrupt:
            print("\nGoodbye...")
            break