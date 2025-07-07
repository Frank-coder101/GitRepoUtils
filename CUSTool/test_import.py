#!/usr/bin/env python3
"""Test to debug CUS import issues"""

print("=== TESTING CUS IMPORT ===")

try:
    print("About to import CUS...")
    import CUS
    print("CUS imported successfully")
    
    # Check if main function exists
    if hasattr(CUS, 'main'):
        print("main function found")
    else:
        print("main function NOT found")
        
    # Try to access some variables
    print(f"SAFE_MODE: {CUS.SAFE_MODE}")
    print(f"OUTPUT_LOG_FILE: {CUS.OUTPUT_LOG_FILE}")
    
except Exception as e:
    print(f"Error importing CUS: {e}")
    import traceback
    traceback.print_exc()

print("=== IMPORT TEST COMPLETE ===")
