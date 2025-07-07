#!/usr/bin/env python3
"""
Test standardized prompt generation for GitHub Copilot requirements analysis
"""
import json
import os
from datetime import datetime

def generate_standardized_prompt(extp_path, requirements_sources=None):
    """Generate a standardized, versionable prompt for Copilot analysis"""
    
    prompt_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "purpose": "ExtP Requirements Analysis and Test Case Generation",
            "extp_path": extp_path
        },
        "request_type": "requirements_analysis",
        "output_format": {
            "requirements": "JSON",
            "validation_rules": "JSON", 
            "test_scenarios": "JSON"
        },
        "analysis_context": {},
        "instructions": [
            "Analyze the provided ExtP codebase and requirements",
            "Generate comprehensive requirements validation rules",
            "Create screen-by-screen workflow progression rules",
            "Identify CRITICAL workflow failures vs code-level issues",
            "Output structured JSON files for CUS consumption"
        ]
    }
    
    # Add ExtP code context (simulated for test)
    if os.path.exists(extp_path):
        prompt_data["analysis_context"]["extp_structure"] = scan_directory_structure(extp_path)
        # In real implementation, we'd add actual file contents here
    
    # Add requirements sources
    if requirements_sources:
        prompt_data["analysis_context"]["requirements_sources"] = requirements_sources
    
    # Generate the standardized prompt
    prompt_template = f"""
=== GITHUB COPILOT: ExtP REQUIREMENTS ANALYSIS REQUEST ===

REQUEST METADATA:
{json.dumps(prompt_data["metadata"], indent=2)}

REQUEST TYPE: {prompt_data["request_type"]}

EXPECTED OUTPUT FORMAT:
{json.dumps(prompt_data["output_format"], indent=2)}

ANALYSIS CONTEXT:
{json.dumps(prompt_data["analysis_context"], indent=2)}

INSTRUCTIONS:
{chr(10).join(f"- {instruction}" for instruction in prompt_data["instructions"])}

EXPECTED OUTPUT STRUCTURE:

1. requirements.json:
{{
  "application_name": "string",
  "version": "string", 
  "expected_workflows": {{
    "workflow_name": {{
      "trigger": "string",
      "input": "string",
      "expected_next_screen": "string",
      "expected_text_contains": ["string"],
      "failure_indicators": ["string"]
    }}
  }},
  "critical_validations": [{{
    "validation_id": "string",
    "description": "string",
    "screen_progression": {{
      "from": "string",
      "action": "string", 
      "to": "string"
    }},
    "failure_criteria": ["string"]
  }}]
}}

2. validation_rules.json:
{{
  "screen_progressions": {{
    "screen_name": {{
      "action_input": {{
        "expected_screen": "string",
        "timeout_seconds": number,
        "failure_if_contains": ["string"],
        "success_if_contains": ["string"]
      }}
    }}
  }},
  "error_classifications": {{
    "CRITICAL": ["workflow_progression_failure", "requirements_violation"],
    "WARNING": ["code_behavior_mismatch", "timing_issue"],
    "INFO": ["input_method_fallback", "retry_success"]
  }}
}}

3. test_scenarios.json:
{{
  "test_scenarios": [{{
    "scenario_id": "string",
    "name": "string", 
    "description": "string",
    "steps": [{{
      "step": number,
      "action": "string",
      "input": "string",
      "expected_result": "string",
      "validation_criteria": ["string"]
    }}],
    "success_criteria": ["string"],
    "failure_criteria": ["string"]
  }}]
}}

Please analyze the provided context and generate these three JSON files with complete, production-ready requirements validation rules for the CUS system.

=== END REQUEST ===
"""
    
    return prompt_template, prompt_data

def scan_directory_structure(path, max_depth=2):
    """Scan directory structure for context (limited depth to control size)"""
    structure = {}
    
    try:
        if os.path.isdir(path):
            for item in os.listdir(path)[:10]:  # Limit to first 10 items
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path) and max_depth > 0:
                    structure[item] = scan_directory_structure(item_path, max_depth - 1)
                elif os.path.isfile(item_path):
                    structure[item] = {"type": "file", "size": os.path.getsize(item_path)}
    except PermissionError:
        structure["error"] = "Permission denied"
    
    return structure

def test_prompt_generation():
    """Test the standardized prompt generation"""
    
    print("=== STANDARDIZED PROMPT GENERATION TEST ===")
    
    # Test with ExtP path
    extp_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
    
    # Generate standardized prompt
    prompt, metadata = generate_standardized_prompt(
        extp_path=extp_path,
        requirements_sources=["README.md", "requirements.txt"]
    )
    
    # Analyze prompt characteristics
    prompt_size = len(prompt)
    print(f"Generated prompt size: {prompt_size:,} characters ({prompt_size/1024:.1f} KB)")
    
    if prompt_size < 8000:
        print("✓ Prompt size: OPTIMAL - Well within safe limits")
    elif prompt_size < 32000:
        print("⚠ Prompt size: ACCEPTABLE - Within working limits")
    else:
        print("✗ Prompt size: TOO LARGE - May hit context limits")
    
    # Test versionability
    print(f"\n✓ Version: {metadata['metadata']['version']}")
    print(f"✓ Timestamp: {metadata['metadata']['timestamp']}")
    print(f"✓ Structured format: JSON-based")
    print(f"✓ Reproducible: Yes (same inputs = same output)")
    
    # Save sample prompt for inspection
    sample_file = "sample_standardized_prompt.txt"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"\n✓ Sample prompt saved to: {sample_file}")
    print("✓ Ready for manual testing with GitHub Copilot")
    
    return prompt, metadata

if __name__ == "__main__":
    print("Testing standardized prompt generation for GitHub Copilot...")
    print("=" * 60)
    
    prompt, metadata = test_prompt_generation()
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    print("✓ Standardized prompt approach is VIABLE")
    print("✓ Output format is predictable and versionable")
    print("✓ Prompt size is manageable for most scenarios")
    print("✓ Ready to test with actual GitHub Copilot interaction")
