@echo off
echo Running Safe Unit Tests for CUS
echo =================================

:: Navigate to the correct directory
cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

:: Show current directory
echo Current directory: %CD%

:: List test files
echo Available test files:
dir test_*.py

:: Run the safe unit tests
echo.
echo Running test_CUS_safe.py...
"C:\Program Files\Python313\python.exe" test_CUS_safe.py

echo.
echo Alternatively, you can run with pytest:
"C:\Program Files\Python313\python.exe" -m pytest test_CUS_safe.py -v

pause
