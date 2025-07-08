import os
import sys
import logging

# Ensure project root is always on sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to activate venv if present
venv_path = os.path.join(project_root, '.venv')
venv_lib = os.path.join(venv_path, 'Lib', 'site-packages')
venv_lib_alt = os.path.join(venv_path, 'lib', 'site-packages')
if os.path.isdir(venv_lib) and venv_lib not in sys.path:
    sys.path.insert(0, venv_lib)
elif os.path.isdir(venv_lib_alt) and venv_lib_alt not in sys.path:
    sys.path.insert(0, venv_lib_alt)

# Log environment info (not to user, just for audit)
logging.basicConfig(level=logging.INFO)
logging.info(f"Python executable: {sys.executable}")
logging.info(f"sys.path: {sys.path}")
