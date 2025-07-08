import sys
import os

# Always add the src directory to sys.path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Ensures src and venv site-packages are always on sys.path for all test runs
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)
venv_path = os.path.join(project_root, '..', '.venv')
venv_lib = os.path.join(venv_path, 'Lib', 'site-packages')
venv_lib_alt = os.path.join(venv_path, 'lib', 'site-packages')
if os.path.isdir(venv_lib) and venv_lib not in sys.path:
    sys.path.insert(0, venv_lib)
elif os.path.isdir(venv_lib_alt) and venv_lib_alt not in sys.path:
    sys.path.insert(0, venv_lib_alt)
