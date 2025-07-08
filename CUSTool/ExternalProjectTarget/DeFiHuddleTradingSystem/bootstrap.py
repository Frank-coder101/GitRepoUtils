import os
import sys
import logging

# Ensure project root and src are always on sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Test mode: 'unit' (default) or 'integration'
TEST_MODE = os.environ.get('TEST_MODE', 'unit').lower()

# Automated IBKR config for integration tests
if TEST_MODE == "integration":
    os.environ.setdefault("IBKR_HOST", "127.0.0.1")
    os.environ.setdefault("IBKR_PORT", "7497")
    os.environ.setdefault("IBKR_CLIENT_ID", "999")

# Do NOT activate venv; always use system Python
# Log environment info (not to user, just for audit)
logging.basicConfig(level=logging.INFO)
logging.info(f"Python executable: {sys.executable}")
logging.info(f"sys.path: {sys.path}")
logging.info(f"TEST_MODE: {TEST_MODE}")
logging.info(f"IBKR_HOST: {os.environ.get('IBKR_HOST')}")
logging.info(f"IBKR_PORT: {os.environ.get('IBKR_PORT')}")
logging.info(f"IBKR_CLIENT_ID: {os.environ.get('IBKR_CLIENT_ID')}")

# Validate TEST_MODE
valid_test_modes = ['unit', 'integration']
if TEST_MODE not in valid_test_modes:
    raise ValueError(f"Invalid TEST_MODE: {TEST_MODE}. Must be one of {valid_test_modes}.")

# Validate IBKR environment variables
required_env_vars = ['IBKR_HOST', 'IBKR_PORT', 'IBKR_CLIENT_ID']
for var in required_env_vars:
    if not os.environ.get(var):
        raise EnvironmentError(f"Environment variable {var} is required but not set.")

# Determine execution mode
EXECUTION_MODE = os.environ.get('EXECUTION_MODE', 'backtest').lower()

# Set environment variables and validate based on mode
if EXECUTION_MODE == 'backtest':
    logging.info("Running in backtest mode.")
    # No external dependencies
elif EXECUTION_MODE == 'live':
    required_vars = ['IBKR_HOST', 'IBKR_PORT', 'IBKR_CLIENT_ID']
    for var in required_vars:
        if not os.environ.get(var):
            raise EnvironmentError(f"Environment variable {var} is required for live mode but not set.")
elif EXECUTION_MODE == 'unit':
    logging.info("Running in unit test mode.")
    # Simulated environment
elif EXECUTION_MODE == 'integration':
    required_vars = ['IBKR_HOST', 'IBKR_PORT', 'IBKR_CLIENT_ID']
    for var in required_vars:
        if not os.environ.get(var):
            raise EnvironmentError(f"Environment variable {var} is required for integration mode but not set.")
else:
    raise ValueError(f"Invalid EXECUTION_MODE: {EXECUTION_MODE}")

input("Bootstrap complete. Press Enter to exit...")
