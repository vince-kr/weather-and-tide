import subprocess
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent

def check_poetry_installed():
    try:
        subprocess.run(["poetry", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Poetry is not installed. Please install it first.")
        print("You can install Poetry by running: pip install poetry")
        sys.exit(1)

def setup_poetry_environment():
    subprocess.run(["poetry", "install"], check=True)

def run_main_script():
    subprocess.run(["poetry", "run", "python", f"{PROJECT_ROOT}/weather_and_tide/main.py"], check=True)

if __name__ == "__main__":
    check_poetry_installed()
    setup_poetry_environment()
    run_main_script()
