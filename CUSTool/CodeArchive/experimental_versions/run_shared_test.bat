@echo off
echo === Running Log File Shared Access Test ===
echo.
echo This test script uses shared file access to write to the log file
echo while CUS is running, avoiding Windows file locking issues.
echo.

cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

echo Running test script...
python test_log_shared.py

echo.
echo Test complete. Press any key to exit.
pause >nul
