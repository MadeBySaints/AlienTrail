@echo off
setlocal enabledelayedexpansion

:: Configuration - Set your desired version or leave blank for auto-increment
set MANUAL_VERSION=
set APP_NAME=Alien Trail
set ICON_FILE=png.png
set SOURCE_FILE=AlienTrail.py

:: Auto-versioning logic
if not exist version.txt (
    echo 0.0.0 > version.txt
)

if "%MANUAL_VERSION%"=="" (
    :: Auto-increment patch version
    for /f "tokens=1-3 delims=." %%a in (version.txt) do (
        set /a patch=%%c + 1
        set NEW_VERSION=%%a.%%b.!patch!
    )
) else (
    set NEW_VERSION=%MANUAL_VERSION%
)

:: Update version file
echo %NEW_VERSION% > version.txt

:: Build executable
echo Building %APP_NAME% v%NEW_VERSION%...
pyinstaller --onefile --icon=%ICON_FILE% --name "%APP_NAME% v.%NEW_VERSION%" %SOURCE_FILE%

:: Clean up build artifacts
rmdir /s /q build
del /q %APP_NAME%.spec

echo Build complete. Version: %NEW_VERSION%
pause