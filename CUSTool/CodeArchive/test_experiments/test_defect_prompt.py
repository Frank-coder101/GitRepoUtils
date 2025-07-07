#!/usr/bin/env python3
"""
Test script to verify defect prompt generation
"""

import os
import sys
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing defect prompt generation...")

try:
    from IssuePromptGenerator import IssuePromptGenerator, IssueSeverity, FailureType, TestCaseContext, DocumentationReference
    print("✓ IssuePromptGenerator imported successfully")
    
    # Initialize with external program path
    external_program_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
    config = {
        "external_program_path": external_program_path,
        "annotate_screenshots": True,
        "capture_before_after": False,
        "capture_sequence": False,
        "severity_mapping": {
            "external_crash": IssueSeverity.CRITICAL,
            "external_error": IssueSeverity.ERROR,
            "cus_failure": IssueSeverity.ERROR,
            "ocr_mismatch": IssueSeverity.WARNING,
            "timeout": IssueSeverity.WARNING
        }
    }
    
    issue_generator = IssuePromptGenerator(config)
    print("✓ IssuePromptGenerator initialized successfully")
    print(f"✓ Defect prompts directory: {issue_generator.defect_prompts_path}")
    
    # Test prompt generation
    test_context = TestCaseContext(
        test_case_name="Test Defect Prompt Generation",
        test_sequence_id=f"TEST_DEFECT_{int(time.time())}",
        expected_behavior="System should generate defect prompts when issues occur",
        actual_behavior="Testing defect prompt generation system",
        failure_step=1,
        reproduction_steps=["Run test script", "Generate test defect prompt", "Check DefectPrompts directory"],
        documentation_refs=[
            DocumentationReference(
                file_path="CUS Requirements.md",
                reference_type="requirement",
                reference_id="CUS-001",
                section_title="Defect Prompt Generation"
            )
        ],
        related_test_cases=["CUS Integration Test"],
        dependency_chain=["CUS", "ExtP", "DefectPrompts"]
    )
    
    prompt_id = issue_generator.generate_issue_prompt(
        test_case_context=test_context,
        error_context={
            "error_type": "cus_simulation",
            "error_message": "Testing defect prompt generation system",
            "test_type": "defect_prompt_generation",
            "description": "Testing if defect prompt generation system is working",
            "timestamp": time.time()
        }
    )
    
    print(f"✓ Test defect prompt generated successfully: {prompt_id}")
    
    # Save the prompt to file
    saved_path = issue_generator.save_issue_prompt(prompt_id)
    print(f"✓ Defect prompt saved to: {saved_path}")
    
    # Check if files were created
    if os.path.exists(issue_generator.defect_prompts_path):
        files = os.listdir(issue_generator.defect_prompts_path)
        print(f"✓ DefectPrompts directory contains {len(files)} files/folders")
        for item in files:
            print(f"  - {item}")
            if os.path.isdir(os.path.join(issue_generator.defect_prompts_path, item)):
                subfiles = os.listdir(os.path.join(issue_generator.defect_prompts_path, item))
                print(f"    ({len(subfiles)} items)")
                for subfile in subfiles[:5]:  # Show first 5 items
                    print(f"      - {subfile}")
    else:
        print("✗ DefectPrompts directory not found")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
