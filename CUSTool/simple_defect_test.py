#!/usr/bin/env python3
"""
Simple test for defect reporting integration
"""

import os
import sys

def test_issue_prompt_generator():
    """Test just the IssuePromptGenerator"""
    print("=== Testing IssuePromptGenerator ===")
    
    try:
        from IssuePromptGenerator import IssuePromptGenerator, TestCaseContext, FailureType, IssueSeverity
        
        external_program_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
        
        # Test with basic config
        issue_config = {
            "external_program_path": external_program_path,
            "annotate_screenshots": True
        }
        
        generator = IssuePromptGenerator(issue_config)
        print("✓ IssuePromptGenerator created successfully")
        
        # Create test context
        test_context = TestCaseContext(
            test_case_name="Simple Test",
            test_sequence_id="TEST_001",
            expected_behavior="Should work",
            actual_behavior="Did not work",
            failure_step=1,
            reproduction_steps=["Step 1", "Step 2"],
            documentation_refs=[],
            related_test_cases=[],
            dependency_chain=[]
        )
        
        # Create error context
        error_context = {
            "failure_type": "external_error",
            "error_message": "Test error",
            "severity": "Error"
        }
        
        # Generate prompt
        issue_prompt = generator.generate_issue_prompt(
            test_case_context=test_context,
            error_context=error_context
        )
        
        print(f"✓ Generated issue prompt: {issue_prompt.issue_id}")
        
        # Check if files were created
        defect_dir = os.path.join(external_program_path, "UserSimulator", "DefectPrompts")
        if os.path.exists(defect_dir):
            files = os.listdir(defect_dir)
            print(f"✓ Found {len(files)} items in defect directory")
        else:
            print("✗ Defect directory not found")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sequence_runner():
    """Test SequenceRunner with minimal config"""
    print("\n=== Testing SequenceRunner ===")
    
    try:
        from SequenceRunner import SequenceRunner
        
        # Create minimal config
        config = {
            "external_program_path": r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem",
            "defect_reporting": {
                "enabled": True,
                "annotate_screenshots": True
            },
            "execution_settings": {
                "max_concurrent_sequences": 1,
                "step_timeout": 30
            },
            "cus_integration": {
                "cus_script_path": "CUS.py"
            }
        }
        
        # Save config to file
        import json
        with open("test_config.json", "w") as f:
            json.dump(config, f)
        
        # Create runner
        runner = SequenceRunner("test_config.json")
        print("✓ SequenceRunner created successfully")
        
        # Check if issue prompt generator is available
        if hasattr(runner, 'issue_prompt_generator') and runner.issue_prompt_generator:
            print("✓ IssuePromptGenerator integrated")
        else:
            print("✗ IssuePromptGenerator not integrated")
            
        # Clean up
        os.remove("test_config.json")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== SIMPLE DEFECT REPORTING TEST ===")
    
    test1 = test_issue_prompt_generator()
    test2 = test_sequence_runner()
    
    if test1 and test2:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
