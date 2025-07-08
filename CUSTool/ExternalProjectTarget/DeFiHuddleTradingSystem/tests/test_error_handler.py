import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.error_handler import ErrorHandler

class TestErrorHandler(unittest.TestCase):
    def test_handle_error(self):
        try:
            raise ValueError("Test error")
        except Exception as e:
            ErrorHandler.handle_error(e, context="TestContext")
        # No assertion needed, just ensure no crash

if __name__ == "__main__":
    unittest.main()
