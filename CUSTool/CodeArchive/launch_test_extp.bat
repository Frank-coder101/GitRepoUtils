@echo off
title ExtP Test Simulator - DeFi Huddle Trading System
color 0F
mode con: cols=120 lines=40

echo ================================================
echo ExtP Test Simulator - DeFi Huddle Trading System
echo Running in Separate Window for CUS Monitoring
echo ================================================
echo.
echo Current Time: %date% %time%
echo Window Title: ExtP Test Simulator
echo.

cd "%~dp0"

echo Starting ExtP Test Simulator with visible console output...
echo CUS should be able to monitor this window content.
echo.

REM Run ExtP Test Simulator without output redirection so it's visible
python test_extp_simulator.py

echo.
echo ================================================
echo ExtP Test Simulator execution completed.
echo This window will remain open for monitoring.
echo ================================================
pause
