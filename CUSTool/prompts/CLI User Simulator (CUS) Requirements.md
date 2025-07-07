# CLI User Simulator (CUS)

# Goal

Create the software for only 1 executable process (CUS), that will be tasked with reading the output file of an `external program` (not in the scope if this project) and in response to what can be detected in that content, CUS will be simulating keyboard events to the window of the external process or capturing runtime error data.


#### Key Features:
1. **Configurable Setup**:
   - At the top of the `CUS.py` file, include configurable parameters for:
     - `External Program` information to be used by CUS to launch the `external program`
     - Absolute path to the output file location of the external target program (`"C:\Users\gibea\Documents\Personal Finance\PromptHandler\CUSTool\output.log"`)
     - Polling interval.
     - Maximum log size for error capture.
     - Path where simulated events (by CUS) are captured (`.\CUSEvents`) 
     - `NewErrorsPath` Absolute path where captured and extracted runtime error data (by CUS) from external program's output file will be recorded (`C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem\CUSErrors`)
     - Location of the `simulation dictionary` file (approach and format is to be determined) path can be relative to CUS folder

2. **Robust Log Monitoring**:
   - Use reliable file monitoring techniques to detect changes in the log file instead of constant polling.

3. **Input Simulation**:
   - Maintain a dictionary mapping outputs from the external target program to expected user inputs that CUS.py must simulate. This file is expected to change very often, at least once every 15 minutes. A file reload is the most likely, so CUS should detect the change and reload the dictionary automatically.
   - Consider (`from pynput.keyboard import Controller, Key`) libraries to simulate keyboard events for user input

4. **Startup Logic**:
   - When CUS is launched, and after initialization routines are complete launch the external program into a command line window
   WITH
   - the necessary command line parameters to redirect the `external program`'s command line output to the output file location

5. **CUS Monitoring Process Logic**:   
- Loop through this logic until CUS process is terminated by user 
    - Detected if there was a change in the output file of the external program
    - If the new data is a cli user interface display of a prompt
        - CUS must find all the available possible expected outputs in the `simulation dictionary` and chose the next logical one
        - CUS must then simulate (with 0 to 0.2 second random delays) the corresponding keyboard inputs
        - CUS must log internally what was detected in the output file, with what was found in the dictionary in a timestamped `CUS_simulation_event` file in the `./NewEvents` folder.
    - Else
        - Assume an error is detected in the `external program`'s output log:
        - Capture only the new error data information (up to 5000 characters).
        - Save the error details in a timestamped `CUS_error_event` file in the `NewErrorsPath` folder.
        - Simulate the keyboard short cut in windows 10 to terminate the external program window.
     -End If

    Check every 5 seconds if the `NewErrorsPath` folder is empty, if it is empty then Loop Back, otherwise wait another 5 seconds

6. **Extensibility**:
   - Design the simulator to be easily extendable for future CLI commands and outputs.
   - Include a configuration file or database for mapping outputs to inputs.



## Answers to the below AI Code Generator QUestions
1 manually edited in file
2) go idea, but we will do that later
3) your call which is best
4) ok
5) i don't how to implement that, but if external program fails on startup, CUS can terminate
6) ok to both
7) no, this is intended and necessary
8) ok


### Logic Improvement Recommendations

1. **Clarify the Role of the Simulation Dictionary**:
   - The requirements mention that the simulation dictionary will change every 15 minutes. This implies dynamic updates. Consider specifying:
     - How the dictionary will be updated (e.g., via a file reload or an API call).
     - Whether the CUS process should reload the dictionary automatically or require a manual restart.

2. **Error Handling Logic**:
   - The current logic assumes that any unexpected output is an error. This could lead to false positives. Consider:
     - Adding a more robust mechanism to distinguish between errors and other unexpected outputs.
     - Allowing configurable error patterns to improve flexibility.

3. **Keyboard Simulation**:
   - The requirements suggest using `pynput` for keyboard simulation. However, `pyautogui` might also be suitable. Ensure the library chosen can handle the required precision and timing for CLI interactions.

4. **File Monitoring**:
   - The requirements suggest using reliable file monitoring techniques. Consider explicitly recommending `watchdog` for its efficiency and cross-platform support.
   - Include a fallback mechanism for environments where `watchdog` is unavailable (e.g., polling).

5. **Startup Logic**:
   - The requirement to launch the external program with command-line parameters to redirect output to a file is clear. However:
     - Ensure the external program's output redirection is compatible with the monitoring logic.
     - Specify how CUS will handle cases where the external program fails to launch or crashes.

6. **Simulation Event Logging**:
   - The requirements mention logging detected prompts and simulated inputs in `CUS_simulation_event` files. Consider:
     - Including a unique identifier for each event to facilitate debugging.
     - Adding an option to aggregate logs into a single file for easier analysis.

7. **Error Folder Monitoring**:
   - The logic to wait until the `NewErrorsPath` folder is empty before resuming could lead to unnecessary delays. Consider:
     - Adding a timeout or a maximum wait duration.
     - Allowing the user to override this behavior via a configuration parameter.

8. **Extensibility**:
   - The requirements mention extensibility for future CLI commands. Consider:
     - Using a modular design to separate core logic (e.g., file monitoring, keyboard simulation) from application-specific logic (e.g., dictionary mapping, error handling).
     - Including unit tests to ensure new features do not break existing functionality.

---

### Code Regeneration vs. Modification

#### **Regenerate All Code**
- **Pros**:
  - Ensures a clean slate, reducing the risk of inheriting existing bugs.
  - Allows for a more modular and maintainable design based on the clarified requirements.
  - Easier to implement best practices and modern techniques (e.g., dependency injection, logging frameworks).
- **Cons**:
  - Requires more time and effort to rewrite and test the entire codebase.
  - Risk of introducing new bugs if the requirements are not fully understood.

#### **Modify Existing Code**
- **Pros**:
  - Faster than rewriting from scratch.
  - Retains any working functionality, reducing the need for extensive testing.
- **Cons**:
  - Higher risk of introducing bugs due to the complexity of modifying existing logic.
  - May result in a less maintainable codebase if the modifications are not well-structured.

---

### Recommendation
Given your concern about creating more bugs, I recommend **regenerating all the code**. This approach ensures that the new implementation aligns with the clarified requirements and avoids the pitfalls of modifying potentially flawed logic. Additionally, a clean implementation will be easier to maintain and extend in the future.

Would you like me to proceed with regenerating the code based on the updated requirements?