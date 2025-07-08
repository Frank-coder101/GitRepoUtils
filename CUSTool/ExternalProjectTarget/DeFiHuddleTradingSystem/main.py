import sys
import os
# Ensure both project root and src are on sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if src_path not in sys.path:
    sys.path.insert(0, src_path)
import bootstrap

from src.ui.cli_wizard import run_cli_wizard
from src.core.config_manager import ConfigManager
from src.integration.broker_manager import BrokerManager
from src.core.execution_controller import ExecutionController
from src.core.logger import Logger
from src.core.persistence import Persistence


def main():
    Logger.init()
    config = ConfigManager.load_or_create()
    run_cli_wizard(config)
    broker = BrokerManager(config)
    execution_controller = ExecutionController(config, broker)
    execution_controller.run()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")
