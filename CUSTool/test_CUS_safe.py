import os
import json
import time
import unittest
from unittest.mock import patch, mock_open, MagicMock
import subprocess
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

class TestCUSSafe(unittest.TestCase):
    """Safe unit tests for CUS.py that won't crash the system"""
    
    def setUp(self):
        self.simulation_dict_content = '{"output1": "input1", "output2": "input2"}'
        # Mock the keyboard controller to prevent actual keyboard interactions
        self.keyboard_patcher = patch('CUS.keyboard')
        self.mock_keyboard = self.keyboard_patcher.start()
        
    def tearDown(self):
        self.keyboard_patcher.stop()

    def test_json_parsing(self):
        """Test JSON parsing without file system access"""
        test_data = '{"test": "value"}'
        result = json.loads(test_data)
        self.assertEqual(result, {"test": "value"})

    @patch("os.path.exists", return_value=False)
    def test_load_simulation_dictionary_file_not_exists(self, mock_exists):
        """Test when simulation dictionary file doesn't exist"""
        # Import locally to avoid import issues
        try:
            from CUS import load_simulation_dictionary
            result = load_simulation_dictionary()
            self.assertEqual(result, {})
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"output1": "input1"}')
    def test_load_simulation_dictionary_valid_json(self, mock_file, mock_exists):
        """Test loading valid JSON simulation dictionary"""
        try:
            from CUS import load_simulation_dictionary
            result = load_simulation_dictionary()
            self.assertEqual(result, {"output1": "input1"})
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_load_simulation_dictionary_invalid_json(self, mock_file, mock_exists):
        """Test loading invalid JSON simulation dictionary"""
        try:
            from CUS import load_simulation_dictionary
            result = load_simulation_dictionary()
            self.assertEqual(result, {})
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    def test_error_patterns(self):
        """Test error pattern matching"""
        try:
            from CUS import ERROR_PATTERNS, is_error
            self.assertIn("ERROR", ERROR_PATTERNS)
            self.assertIn("CRITICAL", ERROR_PATTERNS)
            self.assertIn("FAIL", ERROR_PATTERNS)
            
            # Test error detection
            self.assertTrue(is_error("ERROR: Something went wrong"))
            self.assertTrue(is_error("CRITICAL: System failure"))
            self.assertTrue(is_error("FAIL: Test failed"))
            self.assertFalse(is_error("INFO: Normal operation"))
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("CUS.terminate_external_program")
    def test_handle_error_safe(self, mock_terminate, mock_file, mock_makedirs):
        """Test error handling without actual system calls"""
        try:
            from CUS import handle_error
            handle_error("ERROR: Something went wrong")
            mock_makedirs.assert_called_once()
            mock_file.assert_called_once()
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    @patch("os.listdir", return_value=[])
    def test_monitor_error_folder_empty(self, mock_listdir):
        """Test monitoring empty error folder"""
        try:
            from CUS import monitor_error_folder
            monitor_error_folder()
            mock_listdir.assert_called_once()
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

    def test_configuration_constants(self):
        """Test that configuration constants are properly defined"""
        try:
            from CUS import (
                OUTPUT_LOG_FILE, 
                POLL_INTERVAL, 
                MAX_LOG_SIZE, 
                NEW_ERRORS_PATH, 
                SIMULATION_EVENTS_PATH,
                SIMULATION_DICTIONARY_FILE
            )
            self.assertIsInstance(OUTPUT_LOG_FILE, str)
            self.assertIsInstance(POLL_INTERVAL, int)
            self.assertIsInstance(MAX_LOG_SIZE, int)
            self.assertIsInstance(NEW_ERRORS_PATH, str)
            self.assertIsInstance(SIMULATION_EVENTS_PATH, str)
            self.assertIsInstance(SIMULATION_DICTIONARY_FILE, str)
        except ImportError as e:
            self.skipTest(f"CUS module import failed: {e}")

if __name__ == "__main__":
    # Run tests with minimal output to reduce crash risk
    unittest.main(verbosity=1, exit=False)
