import os
from dotenv import load_dotenv

REQUIRED_ENV_VARS = [
    "SPOTIFY_CLIENT_ID",
    "SPOTIFY_CLIENT_SECRET",
    "SPOTIFY_REDIRECT_URI",
]

def load_settings():
    """Load environment variables from .env file and check for required variables."""
    load_dotenv()

    settings = {}
    missing = []
    
    for var in REQUIRED_ENV_VARS:
        value = os.getenv(var)
        if value is None:
            missing.append(var)
        else:
            settings[var] = value

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
            "Make sure your .env file is set up correctly."
        )
    return settings