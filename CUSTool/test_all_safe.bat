@echo off
echo Testing CUS Tasks System
echo ======================

cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

echo.
echo 1. Testing Python Environment...
python --version

echo.
echo 2. Testing CUS Safe Mode Import...
python -c "import CUS_safe; print('✓ CUS_safe module imported successfully')"

echo.
echo 3. Running Safe Unit Tests...
python test_CUS_safe.py

echo.
echo 4. Testing VS Code Tasks Script...
python test_vscode_tasks.py

echo.
echo All tests completed!
pause
