@echo off
chcp 65001 >nul
title XPWeb OS Launcher
color 0A
cls

echo ===================================================
echo   error OS - LAUNCHER
echo ===================================================
echo.
set /p IP="Enter IP address (e.g. 192.168.1.133): "

if "%IP%"=="" (
    echo [ERROR] IP is empty!
    pause
    exit /b
)

echo.
echo [*] Connecting via ADB...
adb connect %IP%:5555
timeout /t 2 >nul
adb -s %IP%:5555 shell "echo OK" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Connection failed.
    pause
    exit /b
)

echo [*] Killing old server...
adb -s %IP%:5555 shell "killall python3 2>/dev/null"
timeout /t 1 >nul

echo [*] Starting OS Server...
start "XPWeb OS Server" cmd /k "adb -s %IP%:5555 shell python3 /data/myos/server.py"

echo [*] Waiting for server...
timeout /t 3 >nul

echo.
echo ===================================================
echo   OS STARTED!
echo ===================================================
echo.
echo Opening browser...
start http://%IP%:8080
pause