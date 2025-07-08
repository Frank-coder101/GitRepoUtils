import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from unittest.mock import patch
from src.core.config_manager import ConfigManager
from src.ui.cli_wizard import run_cli_wizard

class TestCliWizard(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '10000', 'TWS', 'testuser', 'testpass', '5'])
    def test_run_cli_wizard(self, mock_input):
        config = ConfigManager.default_config()
        run_cli_wizard(config)
        self.assertEqual(config['funds'], 10000.0)
        self.assertEqual(config['broker']['type'], 'TWS')
        self.assertEqual(config['broker']['username'], 'testuser')
        self.assertEqual(config['broker']['password'], 'testpass')

    @patch('builtins.input', side_effect=['invalid', '5'])
    def test_invalid_input(self, mock_input):
        config = ConfigManager.default_config()
        with self.assertLogs('src.ui.cli_wizard', level='INFO') as log:
            run_cli_wizard(config)
        self.assertIn('Invalid option. Please try again.', log.output)

if __name__ == "__main__":
    unittest.main()
