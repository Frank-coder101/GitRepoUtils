import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.logger import Logger
import os
import logging

class TestLogger(unittest.TestCase):
    def test_logger_init_and_info(self):
        Logger.init()
        Logger.info("Test info message")
        # Flush and close all handlers to ensure log file is written
        for handler in logging.root.handlers:
            handler.flush()
            handler.close()
        self.assertTrue(os.path.exists(os.path.expanduser("~/.defihuddle_audit.log")))

if __name__ == "__main__":
    unittest.main()
