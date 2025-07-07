@echo off
setlocal enabledelayedexpansion

REM ===============================================================
REM Enhanced CUS Setup and Run with Requirements Management
REM ===============================================================

echo ===============================================================
echo       CUS (CLI User Simulator) - Enhanced Setup
echo ===============================================================
echo.

REM Check if ExternalRequirementsManagement directory exists
if not exist "ExternalRequirementsManagement" (
    echo Creating ExternalRequirementsManagement directory...
    mkdir "ExternalRequirementsManagement"
    mkdir "ExternalRequirementsManagement\generated"
    mkdir "ExternalRequirementsManagement\generated\backup"
    mkdir "ExternalRequirementsManagement\active"
    mkdir "ExternalRequirementsManagement\templates"
    echo ✓ Directory structure created
    echo.
)

REM Display menu
echo What would you like to do?
echo.
echo 1. Update/Generate Test Cases (Requirements Analysis)
echo 2. Run CUS (Standard Operation)
echo 3. View Current Requirements Status
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto UPDATE_REQUIREMENTS
if "%choice%"=="2" goto RUN_CUS
if "%choice%"=="3" goto VIEW_STATUS
if "%choice%"=="4" goto EXIT
goto INVALID_CHOICE

:UPDATE_REQUIREMENTS
echo.
echo ===============================================================
echo          Requirements Analysis and Test Case Generation
echo ===============================================================
echo.

REM Check if ExtP path is configured
set EXTP_PATH=C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem
if not exist "%EXTP_PATH%" (
    echo ❌ ExtP path not found: %EXTP_PATH%
    echo Please update the EXTP_PATH variable in this batch file.
    pause
    goto MENU
)

echo 📍 ExtP Path: %EXTP_PATH%
echo.

REM Step 1: Generate analysis prompt
echo Step 1: Generating analysis prompt...
python ExternalRequirementsManagement\generate_extp_requirements.py "%EXTP_PATH%" --output-prompt "ExternalRequirementsManagement\generated\analysis_prompt.txt" --output-metadata "ExternalRequirementsManagement\generated\prompt_metadata.json"

if errorlevel 1 (
    echo ❌ Failed to generate analysis prompt
    pause
    goto MENU
)

echo ✓ Analysis prompt generated successfully
echo.

REM Step 2: Backup existing requirements files
echo Step 2: Backing up existing requirements...
if exist "ExternalRequirementsManagement\active\requirements.json" (
    set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    set timestamp=!timestamp: =0!
    
    copy "ExternalRequirementsManagement\active\*.json" "ExternalRequirementsManagement\generated\backup\backup_!timestamp!_*.json" >nul 2>&1
    echo ✓ Existing files backed up with timestamp: !timestamp!
) else (
    echo ℹ No existing requirements files to backup
)
echo.

REM Step 3: Display prompt for user
echo Step 3: Analysis prompt ready for GitHub Copilot
echo.
echo The analysis prompt has been generated at:
echo   ExternalRequirementsManagement\generated\analysis_prompt.txt
echo.
echo ===============================================================
echo                    MANUAL STEPS REQUIRED
echo ===============================================================
echo.
echo 1. Copy the content of the analysis prompt file
echo 2. Paste it into GitHub Copilot Chat in VS Code
echo 3. Wait for Copilot to generate the three JSON files
echo 4. Save the generated files as:
echo    - requirements.json
echo    - validation_rules.json  
echo    - test_scenarios.json
echo 5. Place them in: ExternalRequirementsManagement\active\
echo.

REM Option to open the prompt file
set /p open_prompt="Would you like to open the prompt file now? (y/n): "
if /i "%open_prompt%"=="y" (
    start notepad "ExternalRequirementsManagement\generated\analysis_prompt.txt"
    echo ✓ Prompt file opened in Notepad
)

echo.
set /p continue_setup="Press Enter when you have saved the JSON files to continue..."

REM Step 4: Validate JSON files
echo.
echo Step 4: Validating JSON files...

set json_files_valid=true

if not exist "ExternalRequirementsManagement\active\requirements.json" (
    echo ❌ Missing: requirements.json
    set json_files_valid=false
)

if not exist "ExternalRequirementsManagement\active\validation_rules.json" (
    echo ❌ Missing: validation_rules.json
    set json_files_valid=false
)

if not exist "ExternalRequirementsManagement\active\test_scenarios.json" (
    echo ❌ Missing: test_scenarios.json
    set json_files_valid=false
)

if "%json_files_valid%"=="false" (
    echo.
    echo ⚠ Some JSON files are missing. Please ensure all three files are saved
    echo   in the ExternalRequirementsManagement\active\ directory.
    pause
    goto MENU
)

REM Validate JSON syntax
echo Validating JSON syntax...
python -c "import json; json.load(open('ExternalRequirementsManagement/active/requirements.json'))" 2>nul
if errorlevel 1 (
    echo ❌ Invalid JSON syntax in requirements.json
    set json_files_valid=false
)

python -c "import json; json.load(open('ExternalRequirementsManagement/active/validation_rules.json'))" 2>nul
if errorlevel 1 (
    echo ❌ Invalid JSON syntax in validation_rules.json
    set json_files_valid=false
)

python -c "import json; json.load(open('ExternalRequirementsManagement/active/test_scenarios.json'))" 2>nul
if errorlevel 1 (
    echo ❌ Invalid JSON syntax in test_scenarios.json
    set json_files_valid=false
)

if "%json_files_valid%"=="false" (
    echo.
    echo ⚠ JSON syntax errors detected. Please check the files and try again.
    pause
    goto MENU
)

echo ✓ All JSON files are valid
echo.

REM Step 5: Copy files to CUS directory (optional)
echo Step 5: Making requirements available to CUS...
copy "ExternalRequirementsManagement\active\*.json" "." >nul 2>&1
echo ✓ Requirements files copied to CUS directory
echo.

echo ===============================================================
echo                    REQUIREMENTS UPDATE COMPLETE
echo ===============================================================
echo.
echo ✓ Analysis prompt generated
echo ✓ JSON files validated
echo ✓ Requirements ready for CUS
echo.
echo You can now run CUS with enhanced requirements validation!
echo.

set /p run_cus_now="Would you like to run CUS now? (y/n): "
if /i "%run_cus_now%"=="y" goto RUN_CUS

goto MENU

:RUN_CUS
echo.
echo ===============================================================
echo                    Running CUS
echo ===============================================================
echo.

REM Check if requirements files exist
set has_requirements=false
if exist "requirements.json" (
    if exist "validation_rules.json" (
        if exist "test_scenarios.json" (
            set has_requirements=true
        )
    )
)

if "%has_requirements%"=="true" (
    echo ✓ Requirements files detected - CUS will run with enhanced validation
) else (
    echo ℹ No requirements files found - CUS will run in standard mode
    echo   Use option 1 to generate requirements for enhanced validation
)

echo.
echo Starting CUS...
python CUS.py

echo.
echo CUS execution completed.
pause
goto MENU

:VIEW_STATUS
echo.
echo ===============================================================
echo                Requirements Status Report
echo ===============================================================
echo.

REM Check directory structure
if exist "ExternalRequirementsManagement" (
    echo ✓ ExternalRequirementsManagement directory exists
) else (
    echo ❌ ExternalRequirementsManagement directory missing
    echo   Run option 1 to initialize the requirements system
    pause
    goto MENU
)

REM Check for prompt generation capability
if exist "ExternalRequirementsManagement\generate_extp_requirements.py" (
    echo ✓ Requirements generator available
) else (
    echo ❌ Requirements generator missing
)

REM Check for active requirements
echo.
echo Active Requirements Files:
if exist "ExternalRequirementsManagement\active\requirements.json" (
    echo ✓ requirements.json
) else (
    echo ❌ requirements.json (missing)
)

if exist "ExternalRequirementsManagement\active\validation_rules.json" (
    echo ✓ validation_rules.json
) else (
    echo ❌ validation_rules.json (missing)
)

if exist "ExternalRequirementsManagement\active\test_scenarios.json" (
    echo ✓ test_scenarios.json
) else (
    echo ❌ test_scenarios.json (missing)
)

REM Check for CUS-accessible files
echo.
echo CUS Directory Files:
if exist "requirements.json" (
    echo ✓ requirements.json (accessible to CUS)
) else (
    echo ❌ requirements.json (not accessible to CUS)
)

if exist "validation_rules.json" (
    echo ✓ validation_rules.json (accessible to CUS)
) else (
    echo ❌ validation_rules.json (not accessible to CUS)
)

if exist "test_scenarios.json" (
    echo ✓ test_scenarios.json (accessible to CUS)
) else (
    echo ❌ test_scenarios.json (not accessible to CUS)
)

REM Check for recent backups
echo.
echo Recent Backups:
if exist "ExternalRequirementsManagement\generated\backup" (
    dir /b "ExternalRequirementsManagement\generated\backup\backup_*.json" 2>nul | findstr "backup_" >nul
    if not errorlevel 1 (
        echo ✓ Backup files available
        dir /b "ExternalRequirementsManagement\generated\backup\backup_*.json" 2>nul
    ) else (
        echo ℹ No backup files found
    )
) else (
    echo ❌ Backup directory missing
)

echo.
pause
goto MENU

:INVALID_CHOICE
echo.
echo ❌ Invalid choice. Please enter 1, 2, 3, or 4.
echo.
goto MENU

:MENU
echo.
echo ===============================================================
echo       CUS (CLI User Simulator) - Enhanced Setup
echo ===============================================================
echo.
echo What would you like to do?
echo.
echo 1. Update/Generate Test Cases (Requirements Analysis)
echo 2. Run CUS (Standard Operation)
echo 3. View Current Requirements Status
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto UPDATE_REQUIREMENTS
if "%choice%"=="2" goto RUN_CUS
if "%choice%"=="3" goto VIEW_STATUS
if "%choice%"=="4" goto EXIT
goto INVALID_CHOICE

:EXIT
echo.
echo Goodbye!
exit /b 0
