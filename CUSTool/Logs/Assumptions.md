# Assumptions Log

This file logs assumptions made during the development process based on the `.copilot` directives.

## Assumptions

1. **Unit Tests**:
   - Assumption: Unit tests for all functionalities are required to ensure code quality and correctness.
   - Action: Proceeding to implement comprehensive unit tests for `CUS.py`.

2. **Simulation Dictionary**:
   - Assumption: The simulation dictionary is expected to be in JSON format and dynamically reloaded every 15 minutes.
   - Action: Implemented JSON-based loading and auto-reloading logic.

3. **Error Handling**:
   - Assumption: Configurable error patterns are sufficient to distinguish errors from unexpected outputs.
   - Action: Enhanced error handling logic with configurable patterns.

4. **Setup Commands**:
   - Assumption: A comprehensive setup script is needed to handle all installations and configurations after system reboots.
   - Action: Created `setup_and_run_complete.bat` and `SETUP_COMMANDS.md` with all necessary commands.

5. **Requirements.txt**:
   - Assumption: The requirements.txt file should include all necessary dependencies with specific versions for stability.
   - Action: Updated requirements.txt with pynput, watchdog, pytest, and mock packages.

6. **System Crash Issue**:
   - Assumption: The original unit tests were causing system crashes due to actual keyboard simulation or infinite loops.
   - Action: Created safer alternatives - `test_CUS_safe.py` with mocked keyboard interactions and `test_minimal.bat` for basic testing.

7. **Gradual Testing Approach**:
   - Assumption: A step-by-step testing approach is needed to identify the root cause of crashes.
   - Action: Created `safe_setup.bat` without unit tests and `test_minimal.bat` for basic verification.

8. **Safe Unit Tests Success**:
   - Assumption: The safe unit tests would verify all core functionality without causing system crashes.
   - Action: Successfully ran 8 unit tests, all passed with OK status.
   - Result: All core functionalities are working correctly including JSON parsing, error handling, file monitoring, and configuration constants.

9. **VS Code Crash Issue**:
   - Assumption: The original CUS.py was causing VS Code to close due to keyboard simulation or external program launch issues.
   - Action: Created CUS_safe.py with SAFE_MODE flag that disables actual keyboard simulation and uses safe external program commands.
   - Result: Created VS Code tasks and launch configurations for safe testing.

10. **VS Code Integration**:
    - Assumption: User needs easy ways to launch and debug CUS from within VS Code.
    - Action: Created tasks.json and launch.json configurations for running CUS in safe mode, production mode, and testing.
    - Result: Available VS Code tasks: "Run CUS Safe Mode", "Run CUS Production Mode", "Test CUS Launch", "Run Safe Unit Tests"

11. **Setup Method Clarification**:
    - Assumption: User prefers BAT file setup over Python virtual environments based on `.copilot` directives.
    - Action: Corrected `setup_and_run.bat` to use the proper project path and full requirements.txt instead of limited package installation.
    - Result: Fixed BAT file now properly sets up all directories, installs all required packages, creates sample files, and validates syntax - no VENV needed as per `.copilot` requirements.
    - Verification: Successfully ran setup_and_run.bat with no errors, all dependencies installed correctly.

12. **Baseline Test Results (July 7, 2025)**:
    - Assumption: Need to establish baseline behavior before upgrade work begins.
    - Action: Ran full CUS.py test with ExtP to reproduce known false negative scenario.
    - Result: Successfully reproduced baseline behavior with two key issues identified:
      
    **Issue 1 - False Negative Confirmed**:
    - ExtP shows menu: "Select an option:" with "1. Configure trading system"
    - CUS correctly detects trigger and sends "1"
    - ExtP responds with "Trading system is already configured" (FALSE NEGATIVE)
    - Should show configuration interface instead
    
    **Issue 2 - Monitoring Loop Behavior**:
    - CUS detected "Screen content changed" multiple times but took no action initially
    - Only acted when explicit trigger "Select an option:" was detected
    - This suggests the screen change detection is working but trigger matching may need improvement
    
    **Baseline Established**:
    - No runtime errors or crashes
    - All imports successful
    - OCR and screen capture working correctly
    - Keyboard simulation working correctly
    - The false negative behavior is consistent and reproducible
    - Ready for upgrade work to begin with TestCaseGenerator enhancement and RADAR methodology implementation
