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
    def __init__(self, exclude_patterns=None):
        self.version = "1.0.0"
        self.max_file_size = 1024 * 5  # 5KB per file to stay under limits
        self.total_context_limit = 1024 * 20  # 20KB total to be safe
        self.exclude_patterns = exclude_patterns or []
        
    def discover_requirements_sources(self, extp_path, requirements_file=None, requirements_folder=None):
        """Discover all requirements sources"""
        print(f"[DEBUG] Discovering requirements sources in: {extp_path}")
        sources = []
        
        # User-specified requirements file
        if requirements_file and os.path.exists(requirements_file):
            print(f"[DEBUG] Including user-specified requirements file: {requirements_file}")
            sources.append(("requirements_file", requirements_file))
        else:
            if requirements_file:
                print(f"[DEBUG] User-specified requirements file not found: {requirements_file}")
        
        # User-specified requirements folder
        if requirements_folder and os.path.exists(requirements_folder):
            print(f"[DEBUG] Including user-specified requirements folder: {requirements_folder}")
            for pattern in ["*.md", "*.txt", "*.rst"]:
                files = glob.glob(os.path.join(requirements_folder, "**", pattern), recursive=True)
                for file in files[:5]:  # Limit to avoid size issues
                    print(f"[DEBUG] Found in requirements folder: {file}")
                    sources.append(("requirements_folder", file))
        else:
            if requirements_folder:
                print(f"[DEBUG] User-specified requirements folder not found: {requirements_folder}")
        
        # Auto-discovery in ExtP directory
        auto_patterns = [
            "**/README*.md", "**/requirements*.md", "**/REQUIREMENTS*",
            "**/docs/**/*.md", "**/spec/**/*.md", "**/design/**/*.md"
        ]
        
        for pattern in auto_patterns:
            files = glob.glob(os.path.join(extp_path, pattern), recursive=True)
            for file in files[:3]:  # Limit auto-discovered files
                print(f"[DEBUG] Auto-discovered requirements file: {file}")
                sources.append(("auto_discovered", file))
        
        print(f"[DEBUG] Final requirements sources: {sources}")
        return sources
    
    def scan_extp_codebase(self, extp_path):
        """Scan ExtP codebase for key files"""
        print(f"[DEBUG] Scanning codebase at: {extp_path}")
        important_files = []
        
        # Look for main entry points
        entry_patterns = ["main.py", "app.py", "run.py", "start.py", "__main__.py"]
        for pattern in entry_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            print(f"[DEBUG] Entry pattern '{pattern}' found: {files}")
            important_files.extend(files[:2])  # Max 2 of each type
        
        # Look for configuration files
        config_patterns = ["config.py", "settings.py", "*.ini", "*.yaml", "*.yml", "*.json"]
        for pattern in config_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            print(f"[DEBUG] Config pattern '{pattern}' found: {files}")
            important_files.extend(files[:2])  # Max 2 of each type
        
        # Look for CLI/wizard files (specific to our use case)
        cli_patterns = ["*cli*.py", "*wizard*.py", "*menu*.py", "*interface*.py"]
        for pattern in cli_patterns:
            files = glob.glob(os.path.join(extp_path, "**", pattern), recursive=True)
            print(f"[DEBUG] CLI pattern '{pattern}' found: {files}")
            important_files.extend(files[:3])  # Max 3 CLI files
        
        # Add all Python files in all subdirectories
        all_py_files = glob.glob(os.path.join(extp_path, "**", "*.py"), recursive=True)
        print(f"[DEBUG] All .py files found: {all_py_files}")
        # Exclude files matching any exclude pattern
        filtered_py_files = []
        for f in all_py_files:
            if not any(pat.lower() in f.lower() for pat in self.exclude_patterns):
                filtered_py_files.append(f)
            else:
                print(f"[DEBUG] Excluded by pattern: {f}")
        important_files.extend(filtered_py_files)
        print(f"[DEBUG] Important files after filtering: {important_files}")
        
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
        """Generate a compact directory structure view for the ExtP target directory only"""
        print(f"[DEBUG] Scanning directory structure at: {extp_path}")
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
    
    def _chunk_markdown_file(self, filepath, max_chunk_size=4096):
        """Split a markdown file into logical chunks at headings, each chunk <= max_chunk_size bytes"""
        print(f"[DEBUG] Chunking markdown file: {filepath}")
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        chunks = []
        current_chunk = []
        current_size = 0
        for line in lines:
            if line.strip().startswith('#') and current_chunk:
                # Start new chunk at heading
                if current_size > max_chunk_size:
                    # If chunk is too big, split at previous heading
                    print(f"[DEBUG] Chunk exceeded max size at heading: {line.strip()}")
                chunks.append(''.join(current_chunk))
                current_chunk = []
                current_size = 0
            current_chunk.append(line)
            current_size += len(line.encode('utf-8'))
        if current_chunk:
            chunks.append(''.join(current_chunk))
        # Further split any chunk that is still too large
        final_chunks = []
        for chunk in chunks:
            if len(chunk.encode('utf-8')) <= max_chunk_size:
                final_chunks.append(chunk)
            else:
                # Split by paragraphs if still too large
                paras = chunk.split('\n\n')
                para_chunk = []
                para_size = 0
                for para in paras:
                    para_size += len(para.encode('utf-8')) + 2
                    para_chunk.append(para)
                    if para_size > max_chunk_size:
                        final_chunks.append('\n\n'.join(para_chunk))
                        para_chunk = []
                        para_size = 0
                if para_chunk:
                    final_chunks.append('\n\n'.join(para_chunk))
        print(f"[DEBUG] Markdown file {filepath} split into {len(final_chunks)} chunks.")
        return final_chunks
    
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

SUMMARY OF INCLUDED/SKIPPED/CHUNKED FILES:
{json.dumps(context_data.get('summary', {}), indent=2)}

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

---
If this is part 1 of a multi-part prompt, the next part will be in a file named copilot_analysis_prompt_part2.txt in the same folder. Continue reading the next part for additional requirements/code context.
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

    def print_full_directory_structure(self, extp_path):
        """Print the full directory structure for developer validation (one-time step)"""
        for root, dirs, files in os.walk(extp_path):
            level = root.replace(extp_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")

    def generate_summary(self, included_files, skipped_files, chunked_files):
        """Generate a summary of what was included, skipped, or chunked and why"""
        summary = {
            "included_files": included_files,
            "skipped_files": skipped_files,
            "chunked_files": chunked_files
        }
        return summary

    def generate_multi_part_prompts(self, extp_path, requirements_file=None, requirements_folder=None, output_dir=None, base_filename="copilot_analysis_prompt.txt"):
        """Generate multi-part prompts with semantic chunking for large requirements files"""
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "ExternalProjectPrompts")
        os.makedirs(output_dir, exist_ok=True)

        # Discover requirements sources
        requirements_sources = self.discover_requirements_sources(
            extp_path, requirements_file, requirements_folder
        )
        # Scan codebase
        important_files = self.scan_extp_codebase(extp_path)
        # Generate directory structure
        directory_structure = self.generate_directory_structure(extp_path)

        # Print full directory structure for developer validation
        print("\n[DEVELOPER VALIDATION] Full ExtP directory structure:")
        self.print_full_directory_structure(extp_path)

        # Batch requirements sources with semantic chunking for markdown
        req_batches = []
        req_batch = {}
        req_batch_size = 0
        included_files = []
        skipped_files = []
        chunked_files = []
        for source_type, filepath in requirements_sources:
            ext = os.path.splitext(filepath)[1].lower()
            if ext in [".md", ".markdown"]:
                # Use semantic chunking for markdown
                chunks = self._chunk_markdown_file(filepath, max_chunk_size=self.max_file_size)
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{os.path.relpath(filepath, extp_path)}::chunk_{i+1}"
                    chunk_meta = {
                        "source_type": source_type,
                        "chunk_index": i+1,
                        "total_chunks": len(chunks),
                        "content": chunk
                    }
                    chunk_len = len(chunk)
                    if chunk_len > self.max_file_size:
                        chunked_files.append(chunk_id)
                    included_files.append(chunk_id)
                    # ...existing code...
            else:
                # Non-markdown: treat as a single chunk, but truncate if too large
                content = self.read_file_safely(filepath)
                rel_path = os.path.relpath(filepath, extp_path)
                content_len = len(content)
                if content_len > self.max_file_size:
                    chunked_files.append(rel_path)
                included_files.append(rel_path)
                # ...existing code...
        # Now batch code files (unchanged for now, but can add chunking for code later)
        code_file_batches = []
        code_batch = {}
        code_batch_size = 0
        for filepath in important_files:
            content = self.read_file_safely(filepath)
            rel_path = os.path.relpath(filepath, extp_path)
            content_len = len(content)
            if code_batch_size + content_len > self.total_context_limit and code_batch:
                code_file_batches.append(code_batch)
                code_batch = {}
                code_batch_size = 0
            code_batch[rel_path] = content
            code_batch_size += content_len
        if code_batch:
            code_file_batches.append(code_batch)

        # Calculate total parts
        total_parts = len(req_batches) + len(code_file_batches)
        is_multi_part = total_parts > 1

        # Add summary to each context_data
        summary = self.generate_summary(included_files, skipped_files, chunked_files)

        # Interleave requirements and code files in batching
        interleaved_batches = []
        max_batches = max(len(req_batches), len(code_file_batches))
        for i in range(max_batches):
            if i < len(req_batches):
                interleaved_batches.append(("requirements", req_batches[i]))
            if i < len(code_file_batches):
                interleaved_batches.append(("code", code_file_batches[i]))
        # Write each batch as a separate prompt file (interleaved)
        prompt_files = []
        part_number = 1
        for batch_type, batch in interleaved_batches:
            if batch_type == "requirements":
                context_data = {
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "version": self.version,
                        "extp_path": str(extp_path),
                        "generator": "ExtPRequirementsGenerator",
                        "is_multi_part": is_multi_part,
                        "total_parts": len(interleaved_batches)
                    },
                    "directory_structure": directory_structure if part_number == 1 else {},
                    "requirements_sources": batch,
                    "code_files": {},
                    "total_context_size": sum(len(v["content"]) for v in batch.values()),
                    "summary": summary
                }
                if part_number == 1:
                    prompt = self._build_prompt_template(context_data)
                    filename = base_filename
                else:
                    prompt = self._build_requirements_continuation_prompt_template(context_data, part_number)
                    filename = base_filename.replace(".txt", f"_part{part_number}.txt")
            else:
                context_data = {
                    "metadata": {
                        "is_multi_part": is_multi_part,
                        "total_parts": len(interleaved_batches)
                    },
                    "directory_structure": {},
                    "requirements_sources": {},
                    "code_files": batch,
                    "total_context_size": sum(len(v) for v in batch.values()),
                    "summary": summary
                }
                prompt = self._build_continuation_prompt_template(context_data, part_number)
                filename = base_filename.replace(".txt", f"_part{part_number}.txt")
            output_path = os.path.join(output_dir, filename)
            self.save_prompt_to_file(prompt, output_path)
            prompt_files.append(output_path)
            part_number += 1
        print(f"\n📝 Multi-part prompts written: {prompt_files}")
        return prompt_files

    def _build_requirements_continuation_prompt_template(self, context_data, part_number):
        """Build a continuation prompt template for additional requirements sources"""
        prompt = f"""
=== GITHUB COPILOT: ExtP REQUIREMENTS ANALYSIS CONTINUATION (PART {part_number}) ===\n\nThis is a continuation. Please use this together with the previous part(s) for full context.\n\nREQUIREMENTS SOURCES (CONTINUED):\n{json.dumps(context_data["requirements_sources"], indent=2)}\n\nSUMMARY OF INCLUDED/SKIPPED/CHUNKED FILES:\n{json.dumps(context_data.get('summary', {}), indent=2)}\n\n(Do not repeat instructions. Continue as if this is appended to the previous prompt.)\n---\nIf there is another part, continue reading the next file (copilot_analysis_prompt_part{part_number+1}.txt) for more context.\n"""
        return prompt.strip()

    def _build_continuation_prompt_template(self, context_data, part_number):
        """Build a continuation prompt template for additional code files"""
        prompt = f"""
=== GITHUB COPILOT: ExtP REQUIREMENTS ANALYSIS CONTINUATION (PART {part_number}) ===\n\nThis is a continuation. Please use this together with the previous part(s) for full context.\n\nKEY CODE FILES (CONTINUED):\n{json.dumps(context_data['code_files'], indent=2)}\n\nSUMMARY OF INCLUDED/SKIPPED/CHUNKED FILES:\n{json.dumps(context_data.get('summary', {}), indent=2)}\n\n(Do not repeat instructions. Continue as if this is appended to the previous prompt.)\n---\nIf there is another part, continue reading the next file (copilot_analysis_prompt_part{part_number+1}.txt) for more context.\n"""
        return prompt.strip()

def load_llm_limits(llm_name, config_path="llm_limits.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        limits = json.load(f)
    if llm_name not in limits:
        raise ValueError(f"LLM '{llm_name}' not found in {config_path}")
    return limits[llm_name]

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
        "--exclude-patterns",
        nargs="*",
        default=["test", "tests"],
        help="List of substrings; any code file containing one will be excluded (default: test, tests)"
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
    parser.add_argument(
        "--llm",
        default="gpt-4o",
        help="Target LLM name (must match an entry in llm_limits.json)"
    )
    args = parser.parse_args()
    # Load LLM limits
    llm_limits = load_llm_limits(args.llm)
    # Set batching/chunking limits from config
    ExtPRequirementsGenerator.max_file_size = llm_limits["recommended_prompt_bytes"] // 8  # e.g. 1/8th of prompt
    ExtPRequirementsGenerator.total_context_limit = llm_limits["recommended_prompt_bytes"]
    # Validate ExtP path
    if not os.path.exists(args.extp_path):
        print(f"❌ Error: ExtP path does not exist: {args.extp_path}")
        return 1
    generator = ExtPRequirementsGenerator(exclude_patterns=args.exclude_patterns)
    try:
        generator.generate_multi_part_prompts(
            extp_path=args.extp_path,
            requirements_file=args.requirements_file,
            requirements_folder=args.requirements_folder,
            output_dir=os.path.join(os.getcwd(), "ExternalProjectPrompts"),
            base_filename=os.path.basename(args.output_prompt)
        )
        print("\n✅ SUCCESS!")
        print("Next steps:")
        print(f"1. Copy the content of the generated prompt file(s) in 'ExternalProjectPrompts' to GitHub Copilot Chat")
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
