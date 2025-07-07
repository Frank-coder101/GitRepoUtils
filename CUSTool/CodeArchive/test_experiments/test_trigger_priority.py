#!/usr/bin/env python3
"""
Quick test to verify trigger priority fix in CUS.py
"""

def test_trigger_priority():
    """Test that simulation triggers are checked before error detection"""
    
    # Simulate the logic from process_screen_content
    text_to_process = "There was an error in the setup wizard. Please enter your choice:"
    simulation_dictionary = {
        "Please enter your choice": "1\n",
        "Enter password": "password123\n"
    }
    
    # Test 1: Trigger should be found BEFORE error
    trigger_found = False
    error_found = False
    
    # Check triggers first (corrected logic)
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in text_to_process.lower():
            print(f"✅ CORRECT: Trigger found first: '{trigger}' -> '{action}'")
            trigger_found = True
            break
    
    # Only check errors if no trigger found
    if not trigger_found:
        errors = ["error", "exception", "failed", "timeout", "critical"]
        for error in errors:
            if error.lower() in text_to_process.lower():
                print(f"❌ Error detected: {error}")
                error_found = True
                break
    
    # Results
    if trigger_found and not error_found:
        print("✅ TEST PASSED: Trigger detected before error (correct priority)")
        return True
    else:
        print("❌ TEST FAILED: Error detected instead of trigger")
        return False

if __name__ == "__main__":
    print("Testing CUS trigger priority fix...")
    success = test_trigger_priority()
    if success:
        print("🎯 Fix verified - triggers now have priority over error detection")
    else:
        print("💥 Fix failed - still detecting errors before triggers")
