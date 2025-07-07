@echo off
echo ===================================
echo Enhanced CUS - Auto-Generation Suite
echo ===================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

:MENU
echo Choose an option:
echo.
echo 1. Auto-generate simulation dictionary from ExtP source code
echo 2. Run Enhanced CUS in interactive mode
echo 3. Run Enhanced CUS in systematic exploration mode
echo 4. Generate coverage report only
echo 5. View current simulation dictionary
echo 6. View exploration plan
echo 7. Clean up old logs and reports
echo 8. Install/update required packages
echo 9. Exit
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto AUTO_GENERATE
if "%choice%"=="2" goto INTERACTIVE_MODE
if "%choice%"=="3" goto SYSTEMATIC_MODE
if "%choice%"=="4" goto GENERATE_REPORT
if "%choice%"=="5" goto VIEW_DICTIONARY
if "%choice%"=="6" goto VIEW_PLAN
if "%choice%"=="7" goto CLEANUP
if "%choice%"=="8" goto INSTALL_PACKAGES
if "%choice%"=="9" goto EXIT

echo Invalid choice. Please try again.
goto MENU

:AUTO_GENERATE
echo.
echo ===================================
echo Auto-Generating Simulation Dictionary
echo ===================================
echo.
echo This will analyze ExtP's source code and generate:
echo - simulation_dictionary_generated.json
echo - exploration_plan.json
echo.
python auto_generate_dictionary.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Auto-generation failed.
    pause
) else (
    echo.
    echo SUCCESS: Auto-generation completed.
    echo.
    echo Files created:
    if exist simulation_dictionary_generated.json (
        echo - simulation_dictionary_generated.json
    )
    if exist exploration_plan.json (
        echo - exploration_plan.json
    )
    echo.
    pause
)
goto MENU

:INTERACTIVE_MODE
echo.
echo ===================================
echo Running Enhanced CUS - Interactive Mode
echo ===================================
echo.
echo This mode will:
echo - Monitor screen using OCR
echo - Respond to prompts automatically
echo - Use the auto-generated simulation dictionary
echo.
echo Make sure ExtP is running before continuing.
echo Press Ctrl+C to stop the simulation.
echo.
pause
python enhanced_cus.py
pause
goto MENU

:SYSTEMATIC_MODE
echo.
echo ===================================
echo Running Enhanced CUS - Systematic Mode
echo ===================================
echo.
echo This mode will:
echo - Run all test scenarios from the exploration plan
echo - Systematically test all CLI paths
echo - Generate comprehensive coverage reports
echo.
echo Make sure ExtP is running before continuing.
echo This may take a while to complete.
echo.
pause
python enhanced_cus.py
pause
goto MENU

:GENERATE_REPORT
echo.
echo ===================================
echo Generating Coverage Report
echo ===================================
echo.
python -c "from enhanced_cus import EnhancedCUS; cus = EnhancedCUS(); cus.generate_coverage_report(); print('Report generated successfully')"
pause
goto MENU

:VIEW_DICTIONARY
echo.
echo ===================================
echo Current Simulation Dictionary
echo ===================================
echo.
if exist simulation_dictionary_generated.json (
    echo Generated Dictionary:
    type simulation_dictionary_generated.json
    echo.
) else (
    echo No generated dictionary found.
    echo Run option 1 to generate one.
)
echo.
if exist simulation_dictionary.txt (
    echo Manual Dictionary:
    type simulation_dictionary.txt
    echo.
)
pause
goto MENU

:VIEW_PLAN
echo.
echo ===================================
echo Current Exploration Plan
echo ===================================
echo.
if exist exploration_plan.json (
    type exploration_plan.json
    echo.
) else (
    echo No exploration plan found.
    echo Run option 1 to generate one.
)
pause
goto MENU

:CLEANUP
echo.
echo ===================================
echo Cleaning Up Old Logs and Reports
echo ===================================
echo.
echo This will remove old files from:
echo - Logs/Screenshots/
echo - Logs/CUSEvents/
echo - Logs/Reports/
echo.
set /p confirm="Are you sure? (Y/N): "
if /i "%confirm%"=="Y" (
    if exist "Logs\Screenshots" (
        del /q "Logs\Screenshots\*.*" 2>nul
        echo Cleaned Screenshots folder
    )
    if exist "Logs\CUSEvents" (
        del /q "Logs\CUSEvents\*.*" 2>nul
        echo Cleaned CUSEvents folder
    )
    if exist "Logs\Reports" (
        del /q "Logs\Reports\*.*" 2>nul
        echo Cleaned Reports folder
    )
    echo.
    echo Cleanup completed.
) else (
    echo Cleanup cancelled.
)
pause
goto MENU

:INSTALL_PACKAGES
echo.
echo ===================================
echo Installing/Updating Required Packages
echo ===================================
echo.
echo Installing Python packages...
pip install --upgrade pytesseract pillow pynput pyautogui
echo.
echo Checking Tesseract OCR installation...
where tesseract >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Tesseract OCR not found in PATH.
    echo Please install it from: https://github.com/UB-Mannheim/tesseract/wiki
    echo Or run: winget install UB-Mannheim.TesseractOCR
    echo.
) else (
    echo Tesseract OCR found.
)
echo.
echo Package installation/update completed.
pause
goto MENU

:EXIT
echo.
echo Thank you for using Enhanced CUS!
echo.
exit /b 0
