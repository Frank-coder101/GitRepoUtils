import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.execution_controller import ExecutionController

class DummyBroker:
    def is_connected(self):
        return True
    def check_capabilities(self):
        return True

class TestExecutionController(unittest.TestCase):
    def test_run_backtest(self):
        config = {'mode': 'BackTesting'}
        broker = DummyBroker()
        controller = ExecutionController(config, broker)
        controller.run()  # Should log backtest start

    def test_run_live(self):
        config = {'mode': 'Live'}
        broker = DummyBroker()
        controller = ExecutionController(config, broker)
        controller.run()  # Should log live trading start

if __name__ == "__main__":
    unittest.main()
