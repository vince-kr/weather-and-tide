import glob
from pathlib import Path
import re
import subprocess

# Find whether a venv already exists
venv_config_paths = glob.glob("*/py*cfg")
if venv_config_paths and len(venv_config_paths) == 1:
    venv_path = Path(venv_config_paths[0]).parent
elif venv_config_paths and len(venv_config_paths) > 1:
    print('Found more than one virtual env. Exiting.')
    quit(1)
else:
    print('Generating new virtual env. Press any key to continue.')
    input()
    subprocess.run(('python', '-m', 'venv', 'venv'))
    venv_path = Path("venv")

# Ensured that a venv exists; install dependencies
pip_executable = Path(venv_path / 'bin' / 'pip')
with open('requirements.txt') as rf:
    all_requirements = rf.read().split('\n')
all_requirements = (re.sub('==.*', '', req) for req in all_requirements)
pip_list_output = subprocess.run((pip_executable, 'list'), capture_output=True).stdout
installed = pip_list_output.decode('utf-8')
if not all(req in installed for req in all_requirements):
    print('Installing requirements. Press any key to continue.')
    input()
    subprocess.run((pip_executable, 'install', '-r', 'requirements.txt'))

# Environment is satisfied
python_executable = Path(venv_path / 'bin' / 'python')
subprocess.run((python_executable, 'main.py'))