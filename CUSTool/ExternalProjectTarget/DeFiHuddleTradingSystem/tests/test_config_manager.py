import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):
    def test_default_config(self):
        config = ConfigManager.default_config()
        self.assertIn("funds", config)
        self.assertIn("broker", config)
        self.assertIn("mode", config)
        self.assertIn("watchlist", config)
        self.assertIn("risk", config)
        self.assertIn("ai_optimizer", config)
        self.assertIn("logging", config)

if __name__ == "__main__":
    unittest.main()
