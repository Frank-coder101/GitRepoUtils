#!/usr/bin/env python3
"""
ExtP Requirements Generator for GitHub Copilot Analysis
Generates standardized prompts for GitHub Copilot to analyze ExtP systems
and create comprehensive requirements validation rules for CUS.
"""
import os
import json
import glob
from datetime import datetime
import argparse
from pathlib import Path

class ExtPRequirementsGenerator:
    def __init__(self):
        self.version = "1.0.0"
        self.max_file_size = 1024 * 5  # 5KB per file to stay under limits
        self.total_context_limit = 1024 * 20  # 20KB total to be safe
        
    def discover_requirements_sources(self, extp_path, requirements_file=None, requirements_folder=None):
        """Discover all requirements sources"""
        sources = []
        
        # User-specified requirements file
        if requirements_file and os.path.exists(requirements_file):
            sources.append(("requirements_file", requirements_file))
        
        # User-specified requirements folder
        if requirements_folder and os.path.exists(requirements_folder):
            for pattern in ["*.md", "*.txt", "*.rst"]:
                files = glob.glob(os.path.join(requirements_folder, "**", pattern), recursive=True)
                for file in files[:5]:  # Limit to avoid size issues
                    sources.append(("requirements_folder", file))
        
        # Auto-discovery in ExtP directory
        auto_patterns = [
            "**/README*.md", "**/requirements*.md", "**/REQUIREMENTS*",
            "**/docs/**/*.md", "**/spec/**/*.md", "**/design/**/*.md"
        ]
        
        for pattern in auto_patterns:
            files = glob.glob(os.path.join(extp_path, pattern), recursive=True)
            for file in files[:3]:  # Limit auto-discovered files
                sources.append(("auto_discovered", file))
        
        return sources
    
    def scan_extp_codebase(self, extp_path):
        """Scan ExtP codebase for key files"""
        important_files = []
        
        # Look for main entry points
        entry_patterns = ["main.py", "app.py", "run.py", "start.py", "__main__.py"]
        for pattern in entry_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            important_files.extend(files[:2])  # Max 2 of each type
        
        # Look for configuration files
        config_patterns = ["config.py", "settings.py", "*.ini", "*.yaml", "*.yml", "*.json"]
        for pattern in config_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            important_files.extend(files[:2])  # Max 2 of each type
        
        # Look for CLI/wizard files (specific to our use case)
        cli_patterns = ["*cli*.py", "*wizard*.py", "*menu*.py", "*interface*.py"]
        for pattern in cli_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            important_files.extend(files[:3])  # Max 3 CLI files
        
        return list(set(important_files))  # Remove duplicates
    
    def read_file_safely(self, filepath):
        """Read file content with size limits and error handling"""
        try:
            file_size = os.path.getsize(filepath)
            if file_size > self.max_file_size:
                return f"[FILE TOO LARGE: {file_size} bytes - skipped for size limits]"
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if len(content) > self.max_file_size:
                    content = content[:self.max_file_size] + "\n[TRUNCATED...]"
                return content
        except Exception as e:
            return f"[ERROR READING FILE: {e}]"
    
    def generate_directory_structure(self, extp_path, max_depth=2):
        """Generate a compact directory structure view"""
        structure = {}
        
        def scan_dir(path, current_depth):
            if current_depth > max_depth:
                return {}
            
            items = {}
            try:
                for item in sorted(os.listdir(path))[:8]:  # Limit items per directory
                    if item.startswith('.'):
                        continue
                    
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        items[f"{item}/"] = scan_dir(item_path, current_depth + 1)
                    else:
                        size = os.path.getsize(item_path)
                        items[item] = f"{size} bytes"
            except PermissionError:
                items["error"] = "Permission denied"
            
            return items
        
        return scan_dir(extp_path, 0)
    
    def generate_standardized_prompt(self, extp_path, requirements_file=None, requirements_folder=None):
        """Generate the standardized prompt for GitHub Copilot"""
        
        print(f"🔍 Analyzing ExtP at: {extp_path}")
        
        # Discover requirements sources
        requirements_sources = self.discover_requirements_sources(
            extp_path, requirements_file, requirements_folder
        )
        print(f"📋 Found {len(requirements_sources)} requirements sources")
        
        # Scan codebase
        important_files = self.scan_extp_codebase(extp_path)
        print(f"🗂️  Found {len(important_files)} important code files")
        
        # Generate directory structure
        directory_structure = self.generate_directory_structure(extp_path)
        
        # Build context data
        context_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": self.version,
                "extp_path": str(extp_path),
                "generator": "ExtPRequirementsGenerator"
            },
            "directory_structure": directory_structure,
            "requirements_sources": {},
            "code_files": {},
            "total_context_size": 0
        }
        
        # Add requirements sources content
        current_size = 0
        for source_type, filepath in requirements_sources:
            if current_size > self.total_context_limit:
                break
            
            content = self.read_file_safely(filepath)
            current_size += len(content)
            
            rel_path = os.path.relpath(filepath, extp_path)
            context_data["requirements_sources"][rel_path] = {
                "source_type": source_type,
                "content": content
            }
        
        # Add important code files
        for filepath in important_files:
            if current_size > self.total_context_limit:
                break
            
            content = self.read_file_safely(filepath)
            current_size += len(content)
            
            rel_path = os.path.relpath(filepath, extp_path)
            context_data["code_files"][rel_path] = content
        
        context_data["total_context_size"] = current_size
        
        # Generate the standardized prompt
        prompt = self._build_prompt_template(context_data)
        
        print(f"📏 Generated prompt size: {len(prompt):,} characters ({len(prompt)/1024:.1f} KB)")
        
        return prompt, context_data
    
    def _build_prompt_template(self, context_data):
        """Build the standardized prompt template"""
        
        prompt = f"""
=== GITHUB COPILOT: ExtP REQUIREMENTS ANALYSIS REQUEST ===

REQUEST METADATA:
{json.dumps(context_data["metadata"], indent=2)}

ANALYSIS PURPOSE:
Generate comprehensive requirements validation rules for CUS (CLI User Simulator) to validate ExtP (External Program) behavior against requirements rather than just code implementation.

CRITICAL REQUIREMENT:
The generated rules must distinguish between:
- CRITICAL: Requirements violations and workflow progression failures
- WARNING: Code behavior mismatches and implementation issues
- INFO: Technical details and successful operations

ANALYSIS CONTEXT:

DIRECTORY STRUCTURE:
{json.dumps(context_data["directory_structure"], indent=2)}

REQUIREMENTS SOURCES:
{json.dumps(context_data["requirements_sources"], indent=2)}

KEY CODE FILES:
{json.dumps(context_data["code_files"], indent=2)}

EXPECTED OUTPUT STRUCTURE:

Please generate THREE JSON files with the following exact structure:

1. requirements.json:
{{
  "application_name": "string",
  "version": "string",
  "description": "string",
  "expected_workflows": {{
    "workflow_id": {{
      "name": "string",
      "description": "string",
      "trigger_text": "string",
      "input_action": "string",
      "expected_next_screen": "string",
      "expected_text_contains": ["string"],
      "expected_text_not_contains": ["string"],
      "success_indicators": ["string"],
      "failure_indicators": ["string"],
      "timeout_seconds": number
    }}
  }},
  "screen_definitions": {{
    "screen_id": {{
      "name": "string",
      "description": "string",
      "identifying_text": ["string"],
      "available_actions": ["string"],
      "next_screens": ["string"]
    }}
  }},
  "critical_requirements": [
    {{
      "requirement_id": "string",
      "description": "string",
      "validation_criteria": ["string"],
      "failure_consequences": "string"
    }}
  ]
}}

2. validation_rules.json:
{{
  "screen_progressions": {{
    "from_screen": {{
      "action_input": {{
        "expected_to_screen": "string",
        "max_wait_seconds": number,
        "success_if_contains": ["string"],
        "failure_if_contains": ["string"],
        "critical_if_no_progression": true
      }}
    }}
  }},
  "error_classifications": {{
    "CRITICAL": [
      "workflow_progression_failure",
      "requirements_violation",
      "infinite_loop_detected",
      "expected_screen_not_reached"
    ],
    "WARNING": [
      "unexpected_text_content",
      "slow_response_time",
      "minor_ui_variation"
    ],
    "INFO": [
      "input_method_fallback",
      "retry_success",
      "normal_operation"
    ]
  }},
  "validation_timeouts": {{
    "screen_change_timeout": 10,
    "input_processing_timeout": 5,
    "critical_action_timeout": 30
  }}
}}

3. test_scenarios.json:
{{
  "test_scenarios": [
    {{
      "scenario_id": "string",
      "name": "string",
      "description": "string",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "steps": [
        {{
          "step_number": number,
          "description": "string",
          "action": "wait_for_trigger|send_input|verify_screen",
          "parameters": {{
            "trigger_text": "string",
            "input_value": "string",
            "expected_screen": "string",
            "timeout": number
          }},
          "success_criteria": ["string"],
          "failure_criteria": ["string"]
        }}
      ],
      "overall_success_criteria": ["string"],
      "critical_failure_indicators": ["string"]
    }}
  ]
}}

ANALYSIS INSTRUCTIONS:
1. Focus on REQUIREMENTS-DRIVEN validation, not code-driven behavior
2. Define clear screen progression expectations
3. Identify what constitutes workflow progression failure vs. normal operation
4. Create specific, measurable validation criteria
5. Classify all possible error types appropriately
6. Ensure test scenarios cover critical user workflows
7. Make all timeouts and expectations realistic for production use

Based on the ExtP analysis context provided above, please generate these three JSON files with comprehensive, production-ready requirements validation rules.

=== END REQUEST ===
"""
        
        return prompt.strip()
    
    def save_prompt_to_file(self, prompt, output_file):
        """Save the generated prompt to a file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"💾 Prompt saved to: {output_file}")
    
    def save_context_metadata(self, context_data, output_file):
        """Save context metadata for reference"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(context_data, f, indent=2)
        print(f"📊 Context metadata saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate standardized prompts for GitHub Copilot ExtP analysis"
    )
    parser.add_argument(
        "extp_path",
        help="Path to the ExtP (External Program) directory"
    )
    parser.add_argument(
        "--requirements-file",
        help="Path to a specific requirements file"
    )
    parser.add_argument(
        "--requirements-folder", 
        help="Path to a folder containing requirements documents"
    )
    parser.add_argument(
        "--output-prompt",
        default="copilot_analysis_prompt.txt",
        help="Output file for the generated prompt"
    )
    parser.add_argument(
        "--output-metadata",
        default="prompt_metadata.json",
        help="Output file for context metadata"
    )
    
    args = parser.parse_args()
    
    # Validate ExtP path
    if not os.path.exists(args.extp_path):
        print(f"❌ Error: ExtP path does not exist: {args.extp_path}")
        return 1
    
    # Generate requirements analysis prompt
    generator = ExtPRequirementsGenerator()
    
    try:
        prompt, context_data = generator.generate_standardized_prompt(
            extp_path=args.extp_path,
            requirements_file=args.requirements_file,
            requirements_folder=args.requirements_folder
        )
        
        # Save outputs
        generator.save_prompt_to_file(prompt, args.output_prompt)
        generator.save_context_metadata(context_data, args.output_metadata)
        
        print("\n✅ SUCCESS!")
        print("Next steps:")
        print(f"1. Copy the content of '{args.output_prompt}' to GitHub Copilot Chat")
        print("2. Copilot will generate three JSON files")
        print("3. Save the JSON files for CUS to use")
        print("4. Run CUS with requirements validation enabled")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating prompt: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
