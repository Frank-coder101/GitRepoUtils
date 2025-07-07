#!/usr/bin/env python3
"""
Simple test to check if CUS functions are available
"""

import os
import sys

# Add the CUS directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Test if CUS functions are available"""
    try:
        print("Testing CUS import...")
        import CUS
        print("✓ CUS imported successfully")
        
        # Check if functions exist
        functions_to_check = [
            'prompt_user_to_focus_external_program',
            'focus_target_window',
            'safe_print'
        ]
        
        for func_name in functions_to_check:
            if hasattr(CUS, func_name):
                print(f"✓ {func_name} found")
            else:
                print(f"✗ {func_name} not found")
        
        # Try to call a simple function
        print("\nTesting safe_print function...")
        CUS.safe_print("Test message from outside CUS")
        print("✓ safe_print worked")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
