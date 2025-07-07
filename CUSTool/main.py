import subprocess
import time
import os
import pyautogui

# Configuration
MAIN_SCRIPT = "main.py"  # Path to main.py
OUTPUT_LOG_FILE = "default_output.log"  # New log file name
WORKING_DIRECTORY = "C:\\Users\\gibea\\Documents\\Personal Finance\\PromptHandler\\CUSTool"
POLL_INTERVAL = 2  # Polling interval in seconds
ERROR_FOLDER = "./NewErrors"  # Folder for error files
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors

# Mapping of main.py outputs to expected user inputs
OUTPUT_TO_INPUT = {
    "Select an option:": "5\n",  # Example: Exit wizard
    "Invalid input": "1\n",  # Example: Retry with valid input
    "BackTesting": "2\n",  # Example: Select BackTesting mode
    "Live": "3\n"  # Example: Select Live mode
}

# Ensure the log file exists
if not os.path.exists(OUTPUT_LOG_FILE):
    with open(OUTPUT_LOG_FILE, "w") as log_file:
        log_file.write("Simulated log content for testing purposes.\nSelect an option:\nInvalid input\nERROR: Simulated error for testing.")

def write_to_file(file_path, content):
    """Write content to a file."""
    with open(file_path, "a") as file:
        file.write(content + "\n")

def monitor_log_and_simulate_inputs():
    """Monitor the log file and simulate user inputs based on main.py output."""
    try:
        write_to_file("error_summary.log", "Starting CLI User Simulator...")

        # Ensure error folder exists
        os.makedirs(ERROR_FOLDER, exist_ok=True)

        # Launch main.py
        process = subprocess.Popen(
            ["python", MAIN_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            cwd=WORKING_DIRECTORY
        )

        write_to_file("error_summary.log", "Subprocess launched. Monitoring output...")

        while True:
            time.sleep(POLL_INTERVAL)

            # Read log file
            try:
                if not os.path.exists(os.path.join(WORKING_DIRECTORY, OUTPUT_LOG_FILE)):
                    with open(os.path.join(WORKING_DIRECTORY, OUTPUT_LOG_FILE), "w") as log_file:
                        log_file.write("Simulated log content for testing purposes.\nSelect an option:\nInvalid input\nERROR: Simulated error for testing.")

                with open(os.path.join(WORKING_DIRECTORY, OUTPUT_LOG_FILE), "r") as log_file:
                    log_content = log_file.read()

                # Check for expected outputs and simulate input
                for output, simulated_input in OUTPUT_TO_INPUT.items():
                    if output in log_content:
                        write_to_file("error_summary.log", f"Detected output: {output}. Simulating input: {simulated_input.strip()}")
                        process.stdin.write(simulated_input)
                        process.stdin.flush()

                # Check for errors
                if "ERROR" in log_content:
                    write_to_file("error_summary.log", "Error detected. Capturing log...")
                    error_content = log_content[-MAX_LOG_SIZE:]
                    error_file_path = os.path.join(ERROR_FOLDER, f"CUS_error_event_{int(time.time())}.txt")
                    with open(error_file_path, "w") as error_file:
                        error_file.write(error_content)

                    write_to_file("error_summary.log", f"Error logged to {error_file_path}. Terminating main.py...")
                    process.terminate()

                    # Wait for error folder to be cleared
                    while os.listdir(ERROR_FOLDER):
                        write_to_file("error_summary.log", "Waiting for error folder to be cleared...")
                        time.sleep(POLL_INTERVAL)

                    # Relaunch main.py
                    write_to_file("error_summary.log", "Relaunching main.py...")
                    process = subprocess.Popen(
                        ["python", MAIN_SCRIPT],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        text=True,
                        cwd=WORKING_DIRECTORY
                    )

            except FileNotFoundError:
                write_to_file("error_summary.log", "Log file not found. Ensure main.py is running and generating output.")
            except IOError as e:
                write_to_file("error_summary.log", f"Error reading log file: {e}")

    except subprocess.SubprocessError as e:
        write_to_file("error_summary.log", f"Error launching main.py: {e}")
    except Exception as e:
        write_to_file("error_summary.log", f"Unexpected error: {e}")

if __name__ == "__main__":
    monitor_log_and_simulate_inputs()
