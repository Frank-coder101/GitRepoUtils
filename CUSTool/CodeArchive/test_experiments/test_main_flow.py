#!/usr/bin/env python3
"""
Test script to isolate the main flow issue
"""
import os
import sys
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def safe_print(message):
    """Safe print function"""
    print(f"[TEST] {message}")

def test_main_flow():
    """Test the main flow components"""
    safe_print("=== TESTING MAIN FLOW ===")
    
    # Test 1: Basic startup
    safe_print("Test 1: Basic startup")
    time.sleep(1)
    safe_print("✓ Basic startup works")
    
    # Test 2: Focus prompt
    safe_print("Test 2: Focus prompt")
    print("\n" + "="*60)
    print("WINDOW FOCUS SETUP")
    print("="*60)
    print("CUS can work in three modes:")
    print("1. SIMPLE MODE: Use Alt+Tab to switch to ExtP (recommended)")
    print("2. GUIDED MODE: You help CUS identify the ExtP window")
    print("3. PATTERN MODE: CUS tries to find ExtP using window title patterns")
    print("Please ensure the External Program is running before proceeding.")
    print("="*60)
    
    focus_mode = input("Choose mode - (s)imple, (g)uided, (p)attern [s]: ").strip().lower()
    if not focus_mode:
        focus_mode = 's'
    
    safe_print(f"✓ Focus mode selected: {focus_mode}")
    
    # Test 3: Alt+Tab focus function
    if focus_mode in ['s', 'simple']:
        safe_print("Test 3: Alt+Tab focus function")
        test_alt_tab_focus()
    
    safe_print("=== TEST COMPLETE ===")

def test_alt_tab_focus():
    """Test Alt+Tab focus function"""
    print("\n" + "="*60)
    print("SIMPLE FOCUS MODE")
    print("="*60)
    print("This mode uses Alt+Tab to switch to your External Program window.")
    print("Steps:")
    print("1. Make sure your External Program is running")
    print("2. Focus on the External Program window (click on it)")
    print("3. Come back to this terminal and press Enter")
    print("4. CUS will use Alt+Tab to switch back to ExtP")
    print("="*60)
    
    input("Press Enter when ExtP is focused and you're ready to continue...")
    
    print("\nNow CUS will use Alt+Tab to switch to ExtP...")
    print("Simulating Alt+Tab (in test mode - not actually switching)")
    time.sleep(1)
    
    print("✓ Alt+Tab focus test complete")
    return True

if __name__ == "__main__":
    test_main_flow()
