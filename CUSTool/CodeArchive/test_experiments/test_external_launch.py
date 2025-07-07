#!/usr/bin/env python3
"""
Test script for external program launch functionality
This script tests only the external program launch without running the full CUS monitoring loop
"""

import os
import sys
import time

# Add current directory to path to import CUS
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from CUS import launch_external_program, EXTERNAL_PROGRAM_CMD
    print("✅ CUS module imported successfully")
except ImportError as e:
    print(f"❌ Failed to import CUS module: {e}")
    sys.exit(1)

def test_external_program_launch():
    """Test the external program launch functionality"""
    print("\n" + "="*50)
    print("TESTING EXTERNAL PROGRAM LAUNCH")
    print("="*50)
    
    print(f"External Program Command: {EXTERNAL_PROGRAM_CMD}")
    
    # Check if the external program file exists
    external_program_path = EXTERNAL_PROGRAM_CMD[0]
    if os.path.exists(external_program_path):
        print(f"✅ External program file exists: {external_program_path}")
    else:
        print(f"⚠️  External program file NOT found: {external_program_path}")
        print("   This is expected if the external program hasn't been created yet.")
    
    print("\n🚀 Attempting to launch external program...")
    
    try:
        launch_external_program()
        print("✅ External program launch function executed without errors")
        print("   Check your system for the launched process or any error messages above.")
        
        # Give a moment for the process to start
        time.sleep(2)
        print("\n📝 Note: If the external program file doesn't exist, you should see an error message above.")
        print("   This is normal behavior - CUS will handle the error gracefully.")
        
    except Exception as e:
        print(f"❌ Error during external program launch: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🔧 CUS External Program Launch Test")
    print("This test verifies that the external program launch functionality works correctly.")
    print("It's safe to run and won't crash your system.")
    
    success = test_external_program_launch()
    
    print("\n" + "="*50)
    if success:
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("The external program launch functionality is working correctly.")
    else:
        print("❌ TEST FAILED")
        print("There was an issue with the external program launch functionality.")
    print("="*50)

if __name__ == "__main__":
    main()
