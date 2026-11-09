@echo off
chcp 65001 >nul
title XPWeb OS Uninstaller
color 0C
cls

echo ===================================================
echo   error OS - FULL UNINSTALL
echo ===================================================
echo.
set /p IP="Enter IP address: "

echo.
echo [*] Connecting...
adb connect %IP%:5555
timeout /t 2 >nul

echo [*] Killing Python processes...
adb -s %IP%:5555 shell "killall python3 2>/dev/null"

echo [*] Removing OS folder...
adb -s %IP%:5555 shell "rm -rf /data/myos"

echo [*] Checking...
adb -s %IP%:5555 shell "if [ -d /data/myos ]; then echo 'ERROR: Folder still exists!'; else echo 'SUCCESS: Folder deleted.'; fi"

echo.
echo ===================================================
echo   DONE!
echo ===================================================
pause