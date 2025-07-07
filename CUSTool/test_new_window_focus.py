#!/usr/bin/env python3
"""
Test script for the new window focus workflow
This script tests the user-guided window focus setup
"""

import os
import sys
import time
import traceback

# Add the CUS directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Test the new window focus workflow"""
    try:
        print("=== TESTING NEW WINDOW FOCUS WORKFLOW ===")
        print("This script will test the new user-guided window focus setup.")
        print("Please have an external program running (like Notepad) to test with.")
        
        # Import the CUS functions
        from CUS import prompt_user_to_focus_external_program, focus_target_window, safe_print
        
        print("\n1. Testing window focus setup...")
        success = prompt_user_to_focus_external_program()
        
        if success:
            print("\n✓ Window focus setup successful!")
            
            # Test multiple focus attempts
            print("\n2. Testing multiple focus attempts...")
            for i in range(3):
                print(f"\nFocus test {i+1}/3...")
                time.sleep(1)
                if focus_target_window():
                    print(f"✓ Focus test {i+1} successful")
                else:
                    print(f"✗ Focus test {i+1} failed")
                time.sleep(2)
            
            print("\n=== TEST COMPLETE ===")
            print("If all focus tests succeeded, the new workflow is working correctly!")
            
        else:
            print("\n✗ Window focus setup failed")
            print("Please check that an external program is running and try again.")
            
    except Exception as e:
        print(f"\nError during test: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
