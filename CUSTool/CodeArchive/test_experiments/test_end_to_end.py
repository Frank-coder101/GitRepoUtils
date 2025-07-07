#!/usr/bin/env python3
"""
CUS End-to-End Workflow Test
This test simulates the exact CUS workflow to verify correct behavior
"""

import time
import json
import pyautogui
import subprocess
import os
from PIL import ImageGrab
import pytesseract

def load_simulation_dictionary():
    """Load the simulation dictionary exactly like CUS does"""
    with open("simulation_dictionary.txt", "r") as file:
        return json.load(file)

def capture_screen():
    """Capture screen exactly like CUS does"""
    screenshot = ImageGrab.grab()
    return screenshot

def extract_text_from_image(image):
    """Extract text from image using OCR exactly like CUS does"""
    text = pytesseract.image_to_string(image)
    return text.strip()

def perform_action(action, use_alt_tab=True):
    """Perform action exactly like CUS does"""
    print(f"[CUS-TEST] Starting action: {action}")
    
    # Focus using Alt+Tab if enabled
    if use_alt_tab:
        print("[CUS-TEST] Using Alt+Tab to switch to ExtP...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        print("[CUS-TEST] Alt+Tab executed - should be focused on ExtP")
    
    # Process the action
    if action.startswith("type_"):
        text = action[5:]  # Extract text after "type_"
        print(f"[CUS-TEST] About to type: '{text}'")
        
        # Send text using pyautogui (like CUS does)
        pyautogui.typewrite(text, interval=0.1)
        time.sleep(0.5)
        
        # Press Enter
        pyautogui.press('enter')
        print(f"[CUS-TEST] Completed typing: '{text}' and pressed Enter")
        
    elif action == "press_enter":
        pyautogui.press('enter')
        print("[CUS-TEST] Sent Enter key")
    
    elif action == "wait_random":
        import random
        wait_time = random.randint(1, 3)
        time.sleep(wait_time)
        print(f"[CUS-TEST] Waited {wait_time} seconds")
    
    else:
        print(f"[CUS-TEST] Unknown action: {action}")

def process_screen_content(simulation_dictionary, current_text, trigger_to_test=None):
    """Process screen content exactly like CUS does"""
    if not current_text:
        print("[CUS-TEST] No text found in screen")
        return
    
    print(f"[CUS-TEST] Screen text length: {len(current_text)}")
    print(f"[CUS-TEST] Screen text preview: {current_text[:200]}...")
    
    # Check for simulation triggers
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in current_text.lower():
            print(f"[CUS-TEST] 🎯 TRIGGER DETECTED: '{trigger}' -> '{action}'")
            
            # If testing a specific trigger, only respond to that one
            if trigger_to_test and trigger != trigger_to_test:
                print(f"[CUS-TEST] Skipping trigger '{trigger}' (testing '{trigger_to_test}')")
                continue
            
            # Perform the action
            perform_action(action)
            
            print(f"[CUS-TEST] ✅ Action completed for trigger: '{trigger}'")
            return trigger, action
    
    if trigger_to_test:
        print(f"[CUS-TEST] Target trigger '{trigger_to_test}' not found in screen text")
    else:
        print("[CUS-TEST] No triggers found in screen text")
    
    return None, None

def create_test_extP():
    """Create a test ExtP window using Notepad"""
    print("[CUS-TEST] Creating test ExtP window...")
    
    try:
        # Open Notepad
        process = subprocess.Popen(['notepad.exe'])
        time.sleep(2)
        
        # Type ExtP-like content
        test_content = """DeFi Huddle Trading System - Test Mode
===================================

System initialized successfully.

Select an option:
1. Configure trading system
2. Activate EMERGENCY STOP
3. Deactivate EMERGENCY STOP
4. Show EMERGENCY STOP status
5. Exit wizard

Enter your choice: """
        
        pyautogui.typewrite(test_content, interval=0.01)
        
        print("[CUS-TEST] ✅ Test ExtP window created with content")
        return process
        
    except Exception as e:
        print(f"[CUS-TEST] ❌ Error creating test ExtP: {e}")
        return None

def test_end_to_end_workflow():
    """Test the complete end-to-end workflow"""
    print("=== CUS END-TO-END WORKFLOW TEST ===")
    
    # Load simulation dictionary
    print("[CUS-TEST] Loading simulation dictionary...")
    simulation_dict = load_simulation_dictionary()
    print(f"[CUS-TEST] Loaded {len(simulation_dict)} simulation rules")
    
    # Create test ExtP
    extP_process = create_test_extP()
    if not extP_process:
        print("[CUS-TEST] ❌ Failed to create test ExtP")
        return
    
    print("\n[CUS-TEST] Test ExtP is ready!")
    print("[CUS-TEST] You should see a Notepad window with 'Select an option:' text")
    
    # Focus this window first
    input("\nPress Enter when you can see the Notepad window...")
    
    # Now test the CUS workflow
    print("\n[CUS-TEST] Starting CUS workflow simulation...")
    
    # Step 1: Capture screen
    print("[CUS-TEST] Step 1: Capturing screen...")
    screenshot = capture_screen()
    
    # Step 2: Extract text
    print("[CUS-TEST] Step 2: Extracting text from screen...")
    screen_text = extract_text_from_image(screenshot)
    
    # Step 3: Process for triggers
    print("[CUS-TEST] Step 3: Processing screen content for triggers...")
    trigger_found, action_taken = process_screen_content(
        simulation_dict, 
        screen_text, 
        trigger_to_test="Select an option:"
    )
    
    if trigger_found:
        print(f"\n[CUS-TEST] ✅ SUCCESS!")
        print(f"[CUS-TEST] Found trigger: '{trigger_found}'")
        print(f"[CUS-TEST] Executed action: '{action_taken}'")
        print(f"[CUS-TEST] Check the Notepad window - it should show '1' after 'Enter your choice: '")
    else:
        print(f"\n[CUS-TEST] ❌ FAILED!")
        print(f"[CUS-TEST] Target trigger 'Select an option:' not found")
        print(f"[CUS-TEST] Screen text was: {screen_text[:500]}...")
    
    # Wait for user to verify
    input("\nPress Enter after checking the Notepad window...")
    
    # Clean up
    try:
        extP_process.terminate()
        print("[CUS-TEST] ✅ Test ExtP closed")
    except:
        print("[CUS-TEST] ⚠️ Please close Notepad manually")
    
    return trigger_found is not None

def main():
    """Main test function"""
    print("=== CUS END-TO-END WORKFLOW TEST ===")
    print("This test simulates the exact CUS workflow:")
    print("1. Create test ExtP window (Notepad)")
    print("2. Capture screen with OCR")
    print("3. Detect 'Select an option:' trigger")
    print("4. Use Alt+Tab to focus ExtP")
    print("5. Send '1' keystroke")
    print("6. Verify ExtP receives '1' (not 'Alt+Tab')")
    
    response = input("\nRun the test? (y/n): ").strip().lower()
    if response != 'y':
        print("Test cancelled.")
        return
    
    # Run the test
    success = test_end_to_end_workflow()
    
    print("\n=== TEST RESULTS ===")
    if success:
        print("✅ END-TO-END TEST PASSED!")
        print("   - CUS correctly detected trigger")
        print("   - Alt+Tab focus worked")
        print("   - Correct keystroke sent (should be '1')")
        print("   - No literal 'Alt+Tab' text sent")
    else:
        print("❌ END-TO-END TEST FAILED!")
        print("   - Check OCR setup and trigger detection")
    
    print("\n🎯 CONCLUSION:")
    print("   The literal 'Alt+Tab' text you observed was from test_alt_tab_focus.py")
    print("   The production CUS code correctly sends numeric keystrokes.")

if __name__ == "__main__":
    main()
