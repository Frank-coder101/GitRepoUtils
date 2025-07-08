@echo off
echo ================================================
echo CUS Launch - Enhanced Monitoring
echo ================================================
echo.

echo PREREQUISITE: ExtP must already be running manually
echo CUS will detect and monitor ExtP automatically
echo.

echo Launching Enhanced CUS in main Python environment...
echo You will see all CUS output in this terminal window.
echo.

cd c:\Users\gibea\Documents\GitRepoUtils\CUSTool

echo Current directory: %cd%
echo.
pause

echo Starting Enhanced CUS...
echo Enhanced CUS will now:
echo [✓] Monitor ExtP window content
echo [✓] Detect menu prompts automatically  
echo [✓] Simulate keyboard inputs
echo [✓] Generate defect prompts for false negatives
echo [✓] Log all validation events
echo.
pause

python EnhancedCUS.py

echo.
echo ================================================
echo CUS Execution Complete
echo ================================================
pause
