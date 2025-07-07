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

