#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR / "pointless_impressions_src"))

# Determine which environment we are running
ENV = os.environ.get("ENV", "dev")  # default to dev

# Map ENV values to .env files
env_files = {
    "dev": ".env.dev",
    "staging": ".env.staging",
    "production": ".env.production"
}

# Load the correct .env file
env_file_path = os.path.join(
    os.path.dirname(__file__), env_files.get(ENV, ".env.dev")
    )
load_dotenv(env_file_path)

# Set Django settings module according to ENV
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    f"pointless_impressions_src.pointless_impressions.settings.{ENV}"
)


def main():
    """Run administrative tasks."""
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
