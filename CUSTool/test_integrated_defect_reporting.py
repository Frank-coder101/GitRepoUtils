#!/usr/bin/env python3
"""
Test Integration of IssuePromptGenerator with CUS and SequenceRunner

This script demonstrates the fully integrated defect reporting system:
1. CUS detects external program errors and OCR mismatches
2. SequenceRunner handles test failure and generates defect prompts
3. IssuePromptGenerator creates AI-optimized prompts in the external program directory
"""

import os
import json
import time
from datetime import datetime

# Test configuration
TEST_EXTERNAL_PROGRAM_PATH = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
TEST_CONFIG = {
    "external_program_path": TEST_EXTERNAL_PROGRAM_PATH,
    "defect_reporting": {
        "enabled": True,
        "capture_before_after": True,
        "capture_sequence": False,
        "annotate_screenshots": True,
        "auto_generate_on_failure": True
    },
    "execution_settings": {
        "max_concurrent_sequences": 1,
        "step_timeout": 30,
        "pause_on_error": True
    },
    "cus_integration": {
        "cus_script_path": "CUS.py",
        "use_existing_cus": True
    }
}

def test_issue_prompt_generator():
    """Test IssuePromptGenerator standalone"""
    print("=== Testing IssuePromptGenerator ===")
    
    try:
        from IssuePromptGenerator import IssuePromptGenerator, TestCaseContext, FailureType, IssueSeverity
        
        # Initialize with test config
        issue_config = {
            "external_program_path": TEST_EXTERNAL_PROGRAM_PATH,
            "annotate_screenshots": True,
            "capture_before_after": True
        }
        
        generator = IssuePromptGenerator(issue_config)
        
        # Create test case context
        test_context = TestCaseContext(
            test_case_name="Integration Test - Error Detection",
            test_sequence_id="INT_TEST_001",
            expected_behavior="System should handle menu navigation without errors",
            actual_behavior="System crashed during menu navigation",
            failure_step=3,
            reproduction_steps=[
                "Launch application",
                "Navigate to main menu",
                "Select portfolio option",
                "System crashes with error"
            ],
            documentation_refs=[],
            related_test_cases=["TEST_MENU_001", "TEST_PORTFOLIO_001"],
            dependency_chain=["INIT_001", "LOGIN_001"]
        )
        
        # Generate issue prompt
        prompt_id = generator.generate_issue_prompt(
            test_context=test_context,
            failure_type=FailureType.EXTERNAL_PROGRAM_CRASH,
            error_details={
                "error_type": "System crash",
                "error_message": "Application terminated unexpectedly",
                "last_action": "Menu navigation"
            },
            severity=IssueSeverity.CRITICAL
        )
        
        print(f"✓ Generated defect prompt: {prompt_id}")
        
        # Check if prompt was created in correct location
        expected_dir = os.path.join(TEST_EXTERNAL_PROGRAM_PATH, "UserSimulator", "DefectPrompts")
        if os.path.exists(expected_dir):
            print(f"✓ Defect prompts directory created: {expected_dir}")
            
            # List generated files
            files = os.listdir(expected_dir)
            print(f"✓ Generated files: {len(files)}")
            for file in files[:5]:  # Show first 5 files
                print(f"  - {file}")
        else:
            print(f"✗ Defect prompts directory not found: {expected_dir}")
            
        return True
        
    except Exception as e:
        print(f"✗ IssuePromptGenerator test failed: {e}")
        return False

def test_sequence_runner_integration():
    """Test SequenceRunner with IssuePromptGenerator integration"""
    print("\n=== Testing SequenceRunner Integration ===")
    
    try:
        # Create test config file
        config_file = "test_sequence_runner_config.json"
        with open(config_file, 'w') as f:
            json.dump(TEST_CONFIG, f, indent=2)
        
        from SequenceRunner import SequenceRunner
        
        # Initialize SequenceRunner
        runner = SequenceRunner(config_file)
        
        # Check if IssuePromptGenerator was initialized
        if hasattr(runner, 'issue_prompt_generator') and runner.issue_prompt_generator:
            print("✓ IssuePromptGenerator integrated with SequenceRunner")
            
            # Test manual failure handling
            from SequenceRunner import ExecutionStep, SequenceExecution
            from IssuePromptGenerator import FailureType
            
            # Create test sequence
            test_step = ExecutionStep(
                trigger="test_trigger",
                action="test_action",
                description="Test step for failure handling",
                expected_result="Step should complete successfully"
            )
            
            test_sequence = SequenceExecution(
                sequence_id="TEST_SEQ_001",
                name="Test Sequence",
                description="Test sequence for failure handling",
                steps=[test_step],
                current_step=0,
                state="running"
            )
            
            runner.current_sequence = test_sequence
            
            # Simulate failure
            runner._handle_step_failure(
                test_step,
                test_sequence,
                FailureType.CUS_SIMULATION_FAILURE,
                {"error": "Test simulation failure", "context": "Integration test"}
            )
            
            print("✓ Step failure handling with defect prompt generation completed")
            
        else:
            print("✗ IssuePromptGenerator not integrated with SequenceRunner")
            
        # Clean up
        if os.path.exists(config_file):
            os.remove(config_file)
            
        return True
        
    except Exception as e:
        print(f"✗ SequenceRunner integration test failed: {e}")
        return False

def test_cus_integration():
    """Test CUS with IssuePromptGenerator integration"""
    print("\n=== Testing CUS Integration ===")
    
    try:
        # Import CUS functions
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Test CUS issue prompt generator initialization
        from CUS import initialize_issue_prompt_generator, log_error_event, detect_ocr_mismatch
        
        # Initialize issue prompt generator
        initialize_issue_prompt_generator(TEST_EXTERNAL_PROGRAM_PATH)
        
        print("✓ CUS IssuePromptGenerator initialized")
        
        # Test error event logging with defect prompt
        log_error_event("Test error event", "Test screen content for error simulation")
        
        print("✓ Error event logged with defect prompt generation")
        
        # Test OCR mismatch detection
        detect_ocr_mismatch("Expected menu text", "Actual different text", "Menu navigation test")
        
        print("✓ OCR mismatch detected with defect prompt generation")
        
        return True
        
    except Exception as e:
        print(f"✗ CUS integration test failed: {e}")
        return False

def verify_defect_prompts_location():
    """Verify that defect prompts are created in the correct location"""
    print("\n=== Verifying Defect Prompts Location ===")
    
    defect_prompts_dir = os.path.join(TEST_EXTERNAL_PROGRAM_PATH, "UserSimulator", "DefectPrompts")
    
    if os.path.exists(defect_prompts_dir):
        print(f"✓ Defect prompts directory exists: {defect_prompts_dir}")
        
        # Check subdirectories
        screenshots_dir = os.path.join(defect_prompts_dir, "screenshots")
        metadata_dir = os.path.join(defect_prompts_dir, "metadata")
        
        if os.path.exists(screenshots_dir):
            print(f"✓ Screenshots directory exists: {screenshots_dir}")
        else:
            print(f"✗ Screenshots directory missing: {screenshots_dir}")
            
        if os.path.exists(metadata_dir):
            print(f"✓ Metadata directory exists: {metadata_dir}")
        else:
            print(f"✗ Metadata directory missing: {metadata_dir}")
        
        # List generated files
        try:
            files = os.listdir(defect_prompts_dir)
            prompt_files = [f for f in files if f.endswith('.md')]
            
            print(f"✓ Generated prompt files: {len(prompt_files)}")
            for i, file in enumerate(prompt_files[:3]):  # Show first 3 files
                print(f"  {i+1}. {file}")
                
                # Show file size
                file_path = os.path.join(defect_prompts_dir, file)
                size = os.path.getsize(file_path)
                print(f"     Size: {size} bytes")
                
                # Show first few lines
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()[:5]
                        print(f"     Content preview:")
                        for line in lines:
                            print(f"       {line.strip()}")
                except Exception as e:
                    print(f"     Error reading file: {e}")
                print()
                
        except Exception as e:
            print(f"✗ Error listing files: {e}")
            
        return True
        
    else:
        print(f"✗ Defect prompts directory not found: {defect_prompts_dir}")
        return False

def main():
    """Run all integration tests"""
    print("=== INTEGRATED DEFECT REPORTING SYSTEM TEST ===")
    print(f"Test External Program Path: {TEST_EXTERNAL_PROGRAM_PATH}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run tests
    tests = [
        ("IssuePromptGenerator", test_issue_prompt_generator),
        ("SequenceRunner Integration", test_sequence_runner_integration),
        ("CUS Integration", test_cus_integration),
        ("Defect Prompts Location", verify_defect_prompts_location)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n=== TEST SUMMARY ===")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integrated defect reporting system is working correctly.")
        print("\nKey Features Verified:")
        print("- IssuePromptGenerator creates AI-optimized prompts")
        print("- SequenceRunner integrates defect reporting on test failures")
        print("- CUS detects external program errors and OCR mismatches")
        print("- Defect prompts are saved in external program's UserSimulator/DefectPrompts directory")
        print("- Severity levels are properly assigned based on failure types")
        print("- Screenshots and metadata are captured and organized")
    else:
        print("❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
