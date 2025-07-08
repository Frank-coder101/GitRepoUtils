# NextPromptFG.md

## Chat State Summary (as of 2025-07-08)

### Context
- Workspace: CUSTool
- ExtP Target: ExternalProjectTarget/DeFiHuddleTradingSystem
- Main script: generate_extp_requirements.py
- Output prompt: ExternalProjectPrompts/copilot_analysis_prompt.txt (multi-part)
- LLM config: llm_limits.json

### Key Issues Identified
1. DIRECTORY STRUCTURE in prompt does not match actual ExtP folder contents (likely wrong path or incomplete recursion).
2. KEY CODE FILES is empty in prompt output (code files not included/chunked as required).
3. Only requirements sources are present; code files missing from prompt parts.
4. No summary/metadata in prompt about what was included/skipped/chunked.
5. No explicit pointer to next prompt part or what will be included there.

### User Feedback
- Persistent failure to include code files and correct directory structure is a critical bug.
- The script logic must be fixed once and for all to always use the correct ExtP target directory and include all relevant files.
- The quality of the analysis is seriously impacted by missing code context.
- Improvements needed: summary of included/skipped files, interleaving requirements and code in batching, robust directory scanning.

### Remaining Tasks
1. Audit and fix the code that sets the ExtP target directory path in generate_extp_requirements.py.
2. Update directory scanning logic to always use the correct ExtP path and recurse all subfolders/files.
3. Ensure code files are discovered, chunked (if large), and included in prompt output (not just requirements).
4. Add a summary section in the prompt output indicating what was included, skipped, or chunked, and why.
5. Ensure batching logic interleaves requirements and code files as needed, maximizing context usage.
6. Add a one-time developer validation step to print the discovered directory structure for verification.
7. After fixing, verify the output prompt always matches the real ExtP directory structure and includes both requirements and code files.

---

**To resume:**
- Continue from these tasks and context in the next chat session.
- Reference this file: /NextPromptFG.md
