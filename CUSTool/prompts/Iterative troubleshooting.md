# Iterative Troubleshooting Process for CUS.py development

## CRITICAL DIRECTIVES
1. Do not stop or ask for confirmation between steps; proceed automatically until all features and funtionalities are implemented, all tests pass and all errors and defects are fixed

2. Log each error, test update, and fix in a summary file for traceability

## Start Iterative Process
1. Launch the tests and log all errors automatically to a summary file.
   - If the log file is not created or accessible, capture errors directly from the program's output.

2. For each error:
   - Identify if any test case is reporting a false negative (i.e., the error is not being caught or asserted).
   - Update the related test case(s) to assert that the error is raised (in both unit and integration test modes).
   - Run the test(s) to ensure the error is now caught and not silenced.
   - Fix the underlying error in the code.
   - Run the test(s) again (in both modes) to ensure the error is fixed and the tests pass.

3. Relaunch the tests and repeat the process until no errors remain.

