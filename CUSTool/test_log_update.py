#!/usr/bin/env python3
"""Test script to simulate log file updates and test CUS detection"""

import time
import os

LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"

def append_to_log(content):
    """Append content to the log file"""
    with open(LOG_FILE, "a") as f:
        f.write(content + "\n")
    print(f"Added to log: {content}")

def test_cus_detection():
    """Test if CUS detects log file changes"""
    print("=== Testing CUS Detection ===")
    
    # Add a timestamp
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Add new content that should trigger CUS
    append_to_log(f"{timestamp} INFO Test message from simulator.")
    time.sleep(1)
    
    append_to_log("Welcome to DeFi Huddle Trading System Setup Wizard!")
    time.sleep(1)
    
    append_to_log("Options:")
    append_to_log("1. Configure trading system")
    append_to_log("2. Activate EMERGENCY STOP") 
    append_to_log("3. Deactivate EMERGENCY STOP")
    append_to_log("4. Show EMERGENCY STOP status")
    append_to_log("5. Exit wizard")
    append_to_log("Select an option:")
    
    print("=== Test content added to log file ===")
    print("If CUS is running, it should now detect the 'Select an option:' trigger")
    print("and respond with typing '4' (Show EMERGENCY STOP status)")

if __name__ == "__main__":
    test_cus_detection()
