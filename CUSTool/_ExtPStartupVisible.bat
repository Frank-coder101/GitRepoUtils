@echo off
title ExtP - DeFi Huddle Trading System - Separate Window
color 0F
mode con: cols=120 lines=40

echo ================================================
echo ExtP - DeFi Huddle Trading System
echo Running in Separate Window for CUS Monitoring
echo ================================================
echo.
echo Current Time: %date% %time%
echo Window Title: ExtP - DeFi Huddle Trading System
echo.

cd C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem

echo Starting ExtP with visible console output...
echo CUS should be able to monitor this window content.
echo.

REM Run ExtP without output redirection so it's visible
python C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem\main.py

echo.
echo ================================================
echo ExtP execution completed.
echo This window will remain open for monitoring.
echo ================================================
pause
