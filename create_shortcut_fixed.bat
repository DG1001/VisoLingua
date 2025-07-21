@echo off
REM Create Desktop Shortcut for VisoLingua - Fixed Version
REM Uses VBScript for better compatibility

echo Creating VisoLingua desktop shortcut...

REM Check if VisoLingua.exe exists
if not exist "VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found!
    echo Please make sure VisoLingua.exe is in the same directory as this script.
    pause
    exit /b 1
)

REM Get current directory and desktop path
set "CURRENT_DIR=%CD%"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\VisoLingua.lnk"

REM Create temporary VBScript for shortcut creation
set "VBS_FILE=%TEMP%\create_shortcut.vbs"

(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo Set oShellLink = WshShell.CreateShortcut^("%DESKTOP_SHORTCUT%"^)
echo oShellLink.TargetPath = "%CURRENT_DIR%\VisoLingua.exe"
echo oShellLink.WorkingDirectory = "%CURRENT_DIR%"
echo oShellLink.Description = "VisoLingua - Live Translation Overlay Tool"
echo oShellLink.Save
) > "%VBS_FILE%"

REM Execute VBScript
cscript //nologo "%VBS_FILE%"

REM Clean up temporary file
del "%VBS_FILE%" 2>nul

REM Check if shortcut was created
if exist "%DESKTOP_SHORTCUT%" (
    echo ✅ Desktop shortcut created successfully!
    echo    📂 Location: %DESKTOP_SHORTCUT%
    echo.
    echo You can now double-click the VisoLingua icon on your desktop to start the app.
) else (
    echo ❌ Failed to create desktop shortcut.
    echo.
    echo Alternative: Manually create a shortcut to:
    echo    %CURRENT_DIR%\VisoLingua.exe
)

echo.
pause