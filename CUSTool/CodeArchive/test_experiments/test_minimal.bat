@echo off
echo Minimal Test for CUS Project
echo ============================

:: Navigate to the project directory
cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

:: Check Python version
echo Checking Python version...
"C:\Program Files\Python313\python.exe" --version

:: Check if CUS.py has syntax errors
echo Checking CUS.py syntax...
"C:\Program Files\Python313\python.exe" -m py_compile CUS.py
if errorlevel 1 (
    echo ERROR: Syntax errors found in CUS.py
    pause
    exit /b 1
) else (
    echo SUCCESS: No syntax errors found in CUS.py
)

:: Test imports only
echo Testing imports...
"C:\Program Files\Python313\python.exe" -c "import os, time, subprocess, random; print('Basic imports OK')"
"C:\Program Files\Python313\python.exe" -c "import json; print('JSON import OK')"

:: Test if required packages are installed
echo Testing required packages...
"C:\Program Files\Python313\python.exe" -c "import pynput; print('pynput OK')" 2>nul || echo "pynput NOT INSTALLED"
"C:\Program Files\Python313\python.exe" -c "import watchdog; print('watchdog OK')" 2>nul || echo "watchdog NOT INSTALLED"
"C:\Program Files\Python313\python.exe" -c "import pytest; print('pytest OK')" 2>nul || echo "pytest NOT INSTALLED"

:: Test CUS module import
echo Testing CUS module import...
"C:\Program Files\Python313\python.exe" -c "import CUS; print('CUS module import OK')" 2>nul || echo "CUS module import FAILED"

echo.
echo Basic tests complete!
echo If all tests passed, you can try running the safe unit tests:
echo "C:\Program Files\Python313\python.exe" test_CUS_safe.py
echo.
pause
