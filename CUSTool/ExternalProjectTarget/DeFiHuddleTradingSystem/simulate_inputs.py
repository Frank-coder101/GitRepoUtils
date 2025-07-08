import pexpect

def simulate_cli_inputs():
    # Define the inputs to simulate
    inputs = ["1", "5"]  # Example: Select option 1, then exit with option 5

    # Launch the CLI wizard
    child = pexpect.spawn("python main.py", cwd="c:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem")

    # Interact with the program
    for input_value in inputs:
        child.expect("Select an option:")
        child.sendline(input_value)

    # Capture the output
    child.expect(pexpect.EOF)
    output = child.before.decode()

    # Print the output for review
    print("--- OUTPUT ---")
    print(output)

if __name__ == "__main__":
    simulate_cli_inputs()
