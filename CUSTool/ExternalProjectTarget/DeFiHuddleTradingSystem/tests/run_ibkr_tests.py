import unittest
import sys
import os

# Ensure the parent directory is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test cases in the desired logical order
from tests.test_broker_manager import TestBrokerManager
from tests.test_order_manager import TestOrderManager
from tests.test_execution_controller import TestExecutionController


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # Add tests in logical order
    suite.addTests(loader.loadTestsFromTestCase(TestBrokerManager))
    suite.addTests(loader.loadTestsFromTestCase(TestOrderManager))
    suite.addTests(loader.loadTestsFromTestCase(TestExecutionController))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
