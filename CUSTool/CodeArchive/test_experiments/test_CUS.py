import os
import json
import time
import unittest
from unittest.mock import patch, mock_open
import subprocess
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
# Ensure the CUS module is correctly imported

from CUS import (
    load_simulation_dictionary,
    CoreLogic,
    handle_error,
    monitor_error_folder,
    LogFileHandler,
    launch_external_program,
)

class TestCUS(unittest.TestCase):
    def setUp(self):
        self.simulation_dict_content = '{"output1": "input1", "output2": "input2"}'

    @patch("builtins.open", new_callable=mock_open, read_data='{}')
    def test_load_simulation_dictionary_empty(self, mock_file):
        result = load_simulation_dictionary()
        self.assertEqual(result, {})

    @patch("builtins.open", new_callable=mock_open, read_data='{"output1": "input1"}')
    def test_load_simulation_dictionary_valid(self, mock_file):
        result = load_simulation_dictionary()
        self.assertEqual(result, {"output1": "input1"})

    @patch("CUS.keyboard")
    def test_simulate_input(self, mock_keyboard):
        CoreLogic.simulate_input("abc\n")
        self.assertEqual(mock_keyboard.press.call_count, 4)
        self.assertEqual(mock_keyboard.release.call_count, 4)

    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_handle_error(self, mock_file, mock_makedirs):
        handle_error("ERROR: Something went wrong")
        mock_makedirs.assert_called_once()
        mock_file.assert_called_once()

    @patch("os.listdir", return_value=[])
    def test_monitor_error_folder_empty(self, mock_listdir):
        monitor_error_folder()
        mock_listdir.assert_called_once()

    @patch("os.listdir", side_effect=[["error1.txt"], []])
    def test_monitor_error_folder_not_empty(self, mock_listdir):
        monitor_error_folder()
        self.assertEqual(mock_listdir.call_count, 2)

    @patch("CUS.log_simulation_event")
    @patch("CUS.CoreLogic.simulate_input")
    def test_process_log_content(self, mock_simulate_input, mock_log_event):
        handler = LogFileHandler()
        handler.simulation_dictionary = {"output1": "input1"}
        handler.process_log_content("output1")
        mock_simulate_input.assert_called_once_with("input1")
        mock_log_event.assert_called_once_with("output1", "input1")

    @patch("subprocess.Popen")
    def test_launch_external_program(self, mock_popen):
        launch_external_program()
        mock_popen.assert_called_once_with(
            ["path_to_external_program", "--output", "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

if __name__ == "__main__":
    unittest.main()
