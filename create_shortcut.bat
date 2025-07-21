@echo off
REM Create Desktop Shortcut for VisoLingua
REM This script creates a desktop shortcut without full installation

echo Creating VisoLingua desktop shortcut...

REM Check if VisoLingua.exe exists
if not exist "VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found!
    echo Please make sure VisoLingua.exe is in the same directory as this script.
    pause
    exit /b 1
)

REM Get current directory
set "CURRENT_DIR=%CD%"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\VisoLingua.lnk"

REM Create desktop shortcut using PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%CURRENT_DIR%\VisoLingua.exe'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'VisoLingua - Live Translation Overlay Tool'; $Shortcut.Save()"

if %errorlevel% equ 0 (
    echo ✅ Desktop shortcut created successfully!
    echo    📂 Location: %DESKTOP_SHORTCUT%
    echo.
    echo You can now double-click the VisoLingua icon on your desktop to start the app.
) else (
    echo ❌ Failed to create desktop shortcut.
)

echo.
pause