@echo off
REM Vibely Music Project - double-click to install into FL Studio.
REM Runs Install-Vibely.ps1 from this folder. Nothing is deleted.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-Vibely.ps1" %*
echo.
pause
