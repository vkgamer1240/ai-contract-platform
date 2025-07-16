@echo off
echo =====================================
echo  Contract Analysis Platform Launcher
echo =====================================
echo.
echo Starting the full platform...
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
echo.
echo Press Ctrl+C to stop both servers
echo.

python start_platform.py start

pause
