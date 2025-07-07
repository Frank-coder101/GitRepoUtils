@echo off
echo =============================================================
echo CUS Intelligent Testing System - Demo
echo =============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo Python is available
echo.

REM Check if required packages are installed
echo Checking required packages...
python -c "import json, os, time, random, re, pathlib" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Required standard library packages not available
    pause
    exit /b 1
)

echo Standard library packages available
echo.

REM Check if we're in the right directory
if not exist "CUS.py" (
    echo ERROR: Please run this script from the CUSTool directory
    echo Expected files: CUS.py, TestCaseCreator.py, SequenceRunner.py
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.

REM Create necessary directories
echo Creating necessary directories...
if not exist "Logs" mkdir "Logs"
if not exist "Logs\CUSEvents" mkdir "Logs\CUSEvents"
if not exist "Logs\Screenshots" mkdir "Logs\Screenshots"

echo Directories created
echo.

REM Run the demo
echo =============================================================
echo Running CUS Intelligent Testing System Demo...
echo =============================================================
echo.

python demo.py

echo.
echo =============================================================
echo Demo completed!
echo =============================================================
echo.

REM Show generated files
echo Generated files:
if exist "sample_source" (
    echo   [DIR] sample_source\ - Sample source code for analysis
)
if exist "simulation_dictionary.txt" (
    echo   [FILE] simulation_dictionary.txt - Generated simulation rules
)
if exist "test_sequences.json" (
    echo   [FILE] test_sequences.json - Generated test sequences  
)
if exist "demo_report.html" (
    echo   [FILE] demo_report.html - Execution report
)
if exist "demo_log.json" (
    echo   [FILE] demo_log.json - Detailed execution log
)
echo.

REM Offer to open HTML report
if exist "demo_report.html" (
    echo Would you like to open the HTML report?
    set /p choice="Enter Y to open report, any other key to continue: "
    if /i "%choice%"=="y" (
        start demo_report.html
    )
)

echo.
echo =============================================================
echo Next Steps:
echo =============================================================
echo 1. Review the generated files to understand the system
echo 2. Try running: python MasterController.py
echo 3. Configure your own external program for testing
echo 4. Analyze your program's source code for comprehensive testing
echo.
echo For help, refer to README.md or run:
echo   python MasterController.py --help
echo.

pause
