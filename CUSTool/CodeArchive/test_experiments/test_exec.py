#!/usr/bin/env python3
"""Test to debug CUS execution issues"""

print("=== TESTING CUS EXECUTION ===")

try:
    print("About to execute CUS.py...")
    
    # Try to exec the file to see if there are any errors
    with open('CUS.py', 'r') as f:
        code = f.read()
    
    # Execute the code
    exec(code)
    print("CUS.py executed successfully")
    
except Exception as e:
    print(f"Error executing CUS.py: {e}")
    import traceback
    traceback.print_exc()

print("=== EXECUTION TEST COMPLETE ===")
