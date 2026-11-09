@echo off
chcp 65001 >nul
title XPWeb OS Installer
color 0A
cls

echo ===================================================
echo   error OS - INSTALLER
echo ===================================================
echo.
set /p IP="Enter IP address (e.g. 192.168.1.133): "

echo.
echo [*] Connecting via ADB...
adb connect %IP%:5555
timeout /t 2 >nul
adb -s %IP%:5555 shell "echo OK" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Connection failed. Check ADB and network.
    pause
    exit /b
)

echo [*] Creating directories on device...
adb -s %IP%:5555 shell "mkdir -p /data/myos/www"

echo [*] Copying files to device...
adb -s %IP%:5555 push files\server.py /data/myos/server.py
adb -s %IP%:5555 push files\index.html /data/myos/www/index.html

echo [*] Checking Python...
adb -s %IP%:5555 shell "python3 --version" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Python not found. Installing...
    adb -s %IP%:5555 shell "echo y | yse install python3"
)

echo [*] Creating start script on device...
adb -s %IP%:5555 shell "echo '#!/bin/sh' > /data/myos/start_os.sh"
adb -s %IP%:5555 shell "echo 'nohup python3 /data/myos/server.py > /data/myos/log.txt 2>&1 &' >> /data/myos/start_os.sh"
adb -s %IP%:5555 shell "chmod +x /data/myos/start_os.sh"

echo.
echo ===================================================
echo   INSTALLATION COMPLETE!
echo ===================================================
echo.
echo Now you can use start.bat to launch the OS.
pause