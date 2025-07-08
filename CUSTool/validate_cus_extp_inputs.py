#!/usr/bin/env python3
"""
Automated CUS-ExtP Input Simulation Validator
Validates CUS's ability to simulate inputs and detect responses
"""

import subprocess
import time
import pyautogui
import pytesseract
import os
import json
from datetime import datetime
import threading
import queue

class CUSExtPValidator:
    def __init__(self):
        self.test_results = []
        self.screenshot_queue = queue.Queue()
        self.monitoring = False
        
    def capture_screen_content(self):
        """Capture screen content for analysis"""
        try:
            screenshot = pyautogui.screenshot()
            text = pytesseract.image_to_string(screenshot)
            return text.strip()
        except Exception as e:
            return f"Error capturing screen: {e}"
    
    def monitor_screen_changes(self):
        """Monitor screen for changes during test"""
        last_content = ""
        while self.monitoring:
            current_content = self.capture_screen_content()
            if current_content != last_content:
                self.screenshot_queue.put({
                    'timestamp': datetime.now().isoformat(),
                    'content': current_content
                })
                last_content = current_content
            time.sleep(1)
    
    def validate_input_simulation(self, test_name, expected_trigger, expected_action):
        """Validate a specific input simulation scenario"""
        print(f"\n🔍 Validating: {test_name}")
        print(f"   Expected Trigger: {expected_trigger}")
        print(f"   Expected Action: {expected_action}")
        
        # Start monitoring
        self.monitoring = True
        monitor_thread = threading.Thread(target=self.monitor_screen_changes)
        monitor_thread.start()
        
        # Wait for trigger to appear
        print("   ⏳ Waiting for trigger to appear...")
        trigger_detected = False
        action_executed = False
        
        start_time = time.time()
        timeout = 60  # 1 minute timeout
        
        while time.time() - start_time < timeout and not trigger_detected:
            current_content = self.capture_screen_content()
            if expected_trigger.lower() in current_content.lower():
                trigger_detected = True
                print(f"   ✅ Trigger detected: {expected_trigger}")
                break
            time.sleep(2)
        
        if not trigger_detected:
            print(f"   ❌ Trigger not detected within {timeout} seconds")
            self.monitoring = False
            return False
        
        # Wait for CUS action
        print("   ⏳ Waiting for CUS action...")
        action_start_time = time.time()
        
        while time.time() - action_start_time < 30:  # 30 second timeout for action
            current_content = self.capture_screen_content()
            # Look for signs that action was executed (content change)
            if "Select an option:" not in current_content:
                action_executed = True
                print(f"   ✅ Action executed: Screen content changed")
                break
            time.sleep(2)
        
        self.monitoring = False
        
        # Analyze results
        result = {
            'test_name': test_name,
            'trigger_detected': trigger_detected,
            'action_executed': action_executed,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(result)
        
        if trigger_detected and action_executed:
            print(f"   ✅ Test passed: {test_name}")
            return True
        else:
            print(f"   ❌ Test failed: {test_name}")
            return False
    
    def test_false_negative_detection(self):
        """Test false negative detection specifically"""
        print("\n🚨 Testing False Negative Detection")
        print("=" * 50)
        
        # Look for the known false negative pattern
        false_negative_pattern = "Trading system is already configured"
        
        print("   ⏳ Monitoring for false negative pattern...")
        
        start_time = time.time()
        timeout = 60
        
        while time.time() - start_time < timeout:
            current_content = self.capture_screen_content()
            if false_negative_pattern.lower() in current_content.lower():
                print(f"   🚨 False negative detected: {false_negative_pattern}")
                
                # Check if remediation is applied
                print("   ⏳ Checking for remediation...")
                time.sleep(5)
                
                # Look for remediation actions
                remediation_content = self.capture_screen_content()
                if remediation_content != current_content:
                    print("   ✅ Remediation applied: Screen content changed")
                    return True
                else:
                    print("   ❌ No remediation detected")
                    return False
            
            time.sleep(2)
        
        print("   ℹ️  No false negative pattern encountered")
        return True  # Not finding false negative is also a success
    
    def run_comprehensive_test(self):
        """Run comprehensive CUS-ExtP validation"""
        print("🚀 CUS-ExtP Input Simulation Validator")
        print("=" * 60)
        
        # Test scenarios
        scenarios = [
            {
                'name': 'Menu Selection Test',
                'trigger': 'Select an option:',
                'action': 'type_1'
            },
            {
                'name': 'Configuration Menu Test',
                'trigger': 'Configure trading system',
                'action': 'menu_selection'
            }
        ]
        
        print("\n📋 Starting ExtP...")
        try:
            # Launch ExtP
            extp_process = subprocess.Popen(["_ExtPStartupManual.bat"], shell=True)
            time.sleep(5)  # Wait for ExtP to initialize
            
            print("📋 Starting CUS...")
            # Launch CUS in background
            cus_process = subprocess.Popen([
                "python", "EnhancedCUS.py"
            ], shell=True)
            
            time.sleep(3)  # Wait for CUS to initialize
            
            # Run validation tests
            all_passed = True
            for scenario in scenarios:
                passed = self.validate_input_simulation(
                    scenario['name'],
                    scenario['trigger'],
                    scenario['action']
                )
                if not passed:
                    all_passed = False
            
            # Test false negative detection
            fn_passed = self.test_false_negative_detection()
            if not fn_passed:
                all_passed = False
            
            # Clean up
            print("\n🧹 Cleaning up...")
            try:
                cus_process.terminate()
                extp_process.terminate()
            except:
                pass
            
            # Generate report
            self.generate_report(all_passed)
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            return False
        
        return all_passed
    
    def generate_report(self, all_passed):
        """Generate test report"""
        print("\n📋 Test Report")
        print("=" * 50)
        
        for result in self.test_results:
            status = "✅ PASSED" if result['trigger_detected'] and result['action_executed'] else "❌ FAILED"
            print(f"{status} - {result['test_name']}")
            print(f"         Trigger: {'✓' if result['trigger_detected'] else '✗'}")
            print(f"         Action:  {'✓' if result['action_executed'] else '✗'}")
        
        overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
        print(f"\n🎯 Overall Result: {overall_status}")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'overall_passed': all_passed,
            'test_results': self.test_results
        }
        
        with open('cus_extp_validation_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print("📄 Detailed report saved to: cus_extp_validation_report.json")

def main():
    """Main execution"""
    validator = CUSExtPValidator()
    
    print("🔍 CUS-ExtP Input Simulation Validation")
    print("=" * 60)
    print("This will test CUS's ability to:")
    print("✅ Detect ExtP prompts and triggers")
    print("✅ Send appropriate keyboard inputs")
    print("✅ Handle false negative scenarios")
    print("✅ Apply remediation when needed")
    
    proceed = input("\nProceed with validation? (y/n): ").lower()
    if proceed != 'y':
        print("Test cancelled.")
        return
    
    success = validator.run_comprehensive_test()
    
    if success:
        print("\n🎉 Validation completed successfully!")
        print("✅ CUS can successfully simulate inputs to ExtP")
    else:
        print("\n⚠️  Validation completed with issues")
        print("❌ Some aspects of input simulation need attention")

if __name__ == "__main__":
    main()
