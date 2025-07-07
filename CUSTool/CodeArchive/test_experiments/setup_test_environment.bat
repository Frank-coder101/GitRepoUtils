@echo off
REM =========================================================================
REM CUS System Test Setup Script
REM This script ensures the system Python environment is properly configured
REM and all dependencies are available for running CUS.py
REM =========================================================================

echo.
echo =========================================================================
echo CUS SYSTEM TEST SETUP
echo =========================================================================
echo This script will verify and setup the CUS environment for testing
echo.

REM Navigate to CUS directory
cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"
echo Current directory: %CD%

echo.
echo -------------------------------------------------------------------------
echo STEP 1: VERIFY PYTHON ENVIRONMENT
echo -------------------------------------------------------------------------

REM Verify we're using system Python (not venv)
echo Checking Python version and executable path...
python --version
python -c "import sys; print('Python executable:', sys.executable); print('Python version:', sys.version)"

REM Verify no virtual environment is active
echo.
echo Checking for virtual environment interference...
if defined VIRTUAL_ENV (
    echo WARNING: VIRTUAL_ENV is set to: %VIRTUAL_ENV%
    echo Clearing VIRTUAL_ENV variable...
    set VIRTUAL_ENV=
) else (
    echo ✓ No VIRTUAL_ENV variable detected
)

REM Check if .venv directory exists (should not)
if exist ".venv" (
    echo WARNING: .venv directory found - this should not exist
    echo To remove: rmdir /s /q .venv
) else (
    echo ✓ No .venv directory found
)

echo.
echo -------------------------------------------------------------------------
echo STEP 2: INSTALL/VERIFY DEPENDENCIES
echo -------------------------------------------------------------------------

echo Installing/updating all required dependencies from requirements.txt...
python -m pip install -r requirements.txt

echo.
echo Verifying individual critical dependencies...

REM Test each critical dependency
python -c "
import sys
print('Testing all CUS dependencies...')
dependencies = [
    ('pynput', 'pynput'),
    ('pyautogui', 'pyautogui'), 
    ('pygetwindow', 'pygetwindow'),
    ('pytesseract', 'pytesseract'),
    ('PIL', 'PIL'),
    ('psutil', 'psutil'),
    ('win32gui', 'win32gui'),
    ('win32con', 'win32con'),
    ('win32process', 'win32process')
]

missing = []
for display_name, import_name in dependencies:
    try:
        __import__(import_name)
        print(f'✓ {display_name} available')
    except ImportError as e:
        print(f'✗ {display_name} MISSING: {e}')
        missing.append(display_name)

if missing:
    print(f'\n❌ Missing dependencies: {', '.join(missing)}')
    print('Please install missing dependencies manually')
    sys.exit(1)
else:
    print('\n✅ All dependencies are available!')
"

if errorlevel 1 (
    echo.
    echo ❌ DEPENDENCY CHECK FAILED
    echo Some dependencies are missing. Please install them manually.
    pause
    exit /b 1
)

echo.
echo -------------------------------------------------------------------------
echo STEP 3: VERIFY TESSERACT OCR
echo -------------------------------------------------------------------------

echo Checking for Tesseract OCR installation...
python -c "
import os
tesseract_paths = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\gibea\AppData\Local\Microsoft\WinGet\Packages\UB-Mannheim.TesseractOCR_Microsoft.Winget.Source_8wekyb3d8bbwe\tesseract.exe'
]

found = False
for path in tesseract_paths:
    if os.path.exists(path):
        print(f'✓ Tesseract found at: {path}')
        found = True
        break

if not found:
    print('⚠️  Tesseract OCR not found in common locations')
    print('OCR functionality may not work properly')
    print('Please install Tesseract OCR if you need OCR features')
else:
    print('✅ Tesseract OCR is properly installed')
"

echo.
echo -------------------------------------------------------------------------
echo STEP 4: VERIFY CUS.PY SYNTAX
echo -------------------------------------------------------------------------

echo Checking CUS.py for syntax errors...
python -m py_compile CUS.py
if errorlevel 1 (
    echo ❌ SYNTAX ERROR found in CUS.py
    echo Please fix syntax errors before running tests
    pause
    exit /b 1
) else (
    echo ✅ CUS.py syntax is valid
)

echo.
echo -------------------------------------------------------------------------
echo STEP 5: CREATE/VERIFY DIRECTORIES
echo -------------------------------------------------------------------------

echo Creating necessary directories...
if not exist "Logs" mkdir Logs
if not exist "Logs\CUSEvents" mkdir Logs\CUSEvents
if not exist "Logs\Screenshots" mkdir Logs\Screenshots
if not exist "NewErrors" mkdir NewErrors

echo ✓ Directory structure verified

echo.
echo -------------------------------------------------------------------------
echo STEP 6: VERIFY SIMULATION DICTIONARY
echo -------------------------------------------------------------------------

if exist "simulation_dictionary.txt" (
    echo ✓ simulation_dictionary.txt found
    python -c "
import json
try:
    with open('simulation_dictionary.txt', 'r') as f:
        data = json.load(f)
    print(f'✓ Dictionary is valid JSON with {len(data)} entries')
except json.JSONDecodeError as e:
    print(f'⚠️  Dictionary JSON is invalid: {e}')
except Exception as e:
    print(f'⚠️  Could not read dictionary: {e}')
"
) else (
    echo ⚠️  simulation_dictionary.txt not found
    echo Creating sample dictionary...
    echo {> simulation_dictionary.txt
    echo   "test trigger": "press_enter",>> simulation_dictionary.txt
    echo   "continue": "press_enter",>> simulation_dictionary.txt
    echo   "press any key": "press_space">> simulation_dictionary.txt
    echo }>> simulation_dictionary.txt
    echo ✓ Sample dictionary created
)

echo.
echo =========================================================================
echo SETUP COMPLETE!
echo =========================================================================
echo.
echo All checks passed. CUS is ready for testing.
echo.
echo To run CUS:
echo   python CUS.py
echo.
echo To run quick dependency test:
echo   python test_deps.py
echo.
echo =========================================================================
pause
