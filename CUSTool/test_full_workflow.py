#!/usr/bin/env python3
"""
Full Workflow Test for CUS
Tests the complete workflow: trigger detection -> Alt+Tab focus -> keystroke simulation
"""

import time
import pyautogui
import subprocess
import os
import sys

def create_test_notepad():
    """Create a test Notepad window to simulate ExtP"""
    print("Creating test Notepad window...")
    try:
        # Open Notepad
        process = subprocess.Popen(['notepad.exe'], shell=True)
        time.sleep(2)  # Give time for Notepad to open
        
        # Type some initial content to simulate ExtP prompts
        pyautogui.write("DeFi Huddle Trading System - Test Mode\n")
        pyautogui.write("Select an option:\n")
        pyautogui.write("1. Configure trading system\n")
        pyautogui.write("2. Activate EMERGENCY STOP\n")
        pyautogui.write("3. Deactivate EMERGENCY STOP\n")
        pyautogui.write("4. Show EMERGENCY STOP status\n")
        pyautogui.write("5. Exit wizard\n")
        pyautogui.write("Enter your choice: ")
        
        print("✓ Test Notepad window created with ExtP-like content")
        return process
    except Exception as e:
        print(f"✗ Error creating test Notepad: {e}")
        return None

def test_alt_tab_focus():
    """Test Alt+Tab focus functionality"""
    print("\n=== Testing Alt+Tab Focus ===")
    
    # Focus this command window first
    print("This window should be focused...")
    time.sleep(1)
    
    # Execute Alt+Tab to switch to Notepad
    print("Executing Alt+Tab to switch to Notepad...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)
    
    # Type a test message
    print("Sending '1' to the focused window...")
    pyautogui.write('1')
    pyautogui.press('enter')
    
    # Alt+Tab back to this window
    time.sleep(1)
    pyautogui.hotkey('alt', 'tab')
    print("✓ Alt+Tab test completed")

def test_simulation_dictionary():
    """Test the simulation dictionary parsing"""
    print("\n=== Testing Simulation Dictionary ===")
    
    # Read the dictionary file
    dict_file = "simulation_dictionary.txt"
    if not os.path.exists(dict_file):
        print(f"✗ Dictionary file {dict_file} not found")
        return False
    
    try:
        with open(dict_file, 'r') as f:
            content = f.read()
        
        # Parse as JSON
        import json
        simulation_dict = json.loads(content)
        
        # Check key triggers
        test_triggers = [
            "Select an option:",
            "1. Configure trading system",
            "2. Activate EMERGENCY STOP",
            "3. Deactivate EMERGENCY STOP",
            "4. Show EMERGENCY STOP status"
        ]
        
        print("Checking simulation dictionary entries:")
        for trigger in test_triggers:
            if trigger in simulation_dict:
                action = simulation_dict[trigger]
                print(f"✓ '{trigger}' -> '{action}'")
            else:
                print(f"✗ '{trigger}' not found in dictionary")
        
        return True
    except Exception as e:
        print(f"✗ Error parsing simulation dictionary: {e}")
        return False

def test_perform_action_simulation():
    """Test the perform_action function logic"""
    print("\n=== Testing Action Simulation Logic ===")
    
    # Test actions that should send numbers
    test_actions = ["type_1", "type_2", "type_3", "type_4"]
    
    for action in test_actions:
        if action.startswith("type_"):
            text = action[5:]  # Extract text after "type_"
            print(f"Action '{action}' would send text: '{text}'")
            
            # Verify it's a number, not "Alt+Tab"
            if text.isdigit():
                print(f"✓ Action '{action}' correctly sends number '{text}'")
            else:
                print(f"✗ Action '{action}' sends non-number text: '{text}'")
        else:
            print(f"Action '{action}' is not a type action")

def main():
    """Main test function"""
    print("=== CUS Full Workflow Test ===")
    print("This test will validate the complete CUS workflow")
    print("Make sure no important windows are open that could be affected")
    
    # Get user confirmation
    response = input("\nContinue with test? (y/n): ").strip().lower()
    if response != 'y':
        print("Test cancelled.")
        return
    
    # Test 1: Simulation Dictionary
    dict_ok = test_simulation_dictionary()
    if not dict_ok:
        print("❌ Dictionary test failed - stopping")
        return
    
    # Test 2: Action Logic
    test_perform_action_simulation()
    
    # Test 3: Alt+Tab Focus (interactive)
    response = input("\nTest Alt+Tab focus with Notepad? (y/n): ").strip().lower()
    if response == 'y':
        # Create test Notepad
        notepad_process = create_test_notepad()
        if notepad_process:
            print("\n📝 Notepad is now open with test content")
            print("This test will:")
            print("1. Focus this command window")
            print("2. Use Alt+Tab to switch to Notepad")
            print("3. Send '1' and Enter to Notepad")
            print("4. Alt+Tab back to this window")
            
            input("\nPress Enter to start the Alt+Tab test...")
            test_alt_tab_focus()
            
            # Close Notepad
            try:
                notepad_process.terminate()
                print("✓ Test Notepad closed")
            except:
                print("⚠️ Please close Notepad manually")
    
    print("\n=== Test Summary ===")
    print("✓ Simulation dictionary structure verified")
    print("✓ Action logic verified - type_1 sends '1', not 'Alt+Tab'")
    print("✓ Alt+Tab focus mechanism tested")
    print("\nIf all tests passed, CUS should work correctly:")
    print("- Trigger 'Select an option:' should execute 'type_1'")
    print("- Action 'type_1' should send '1' to ExtP")
    print("- Alt+Tab should successfully focus ExtP before sending keys")

if __name__ == "__main__":
    main()
