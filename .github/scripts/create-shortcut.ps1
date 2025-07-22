param($portableDir)

$shortcutContent = @'
@echo off
REM Create Desktop Shortcut for VisoLingua Portable

set "CURRENT_DIR=%CD%"
set "SHORTCUT_NAME=VisoLingua.lnk"

echo Creating desktop shortcut...
echo Target: %CURRENT_DIR%\VisoLingua.exe

REM Try to find the correct desktop path (OneDrive or local)
set "DESKTOP_DIR=%USERPROFILE%\Desktop"
if not exist "%DESKTOP_DIR%" (
    set "DESKTOP_DIR=%USERPROFILE%\OneDrive\Desktop"
)
if not exist "%DESKTOP_DIR%" (
    set "DESKTOP_DIR=%PUBLIC%\Desktop"
)

echo Desktop path: %DESKTOP_DIR%

REM Check if desktop folder exists
if not exist "%DESKTOP_DIR%" (
    echo ❌ Desktop folder not found. Checked:
    echo    - %USERPROFILE%\Desktop
    echo    - %USERPROFILE%\OneDrive\Desktop  
    echo    - %PUBLIC%\Desktop
    pause
    exit /b 1
)

REM Check if executable exists
if not exist "%CURRENT_DIR%\VisoLingua.exe" (
    echo ❌ VisoLingua.exe not found in current directory
    pause
    exit /b 1
)

REM Create shortcut with proper error handling
powershell -ExecutionPolicy Bypass -Command "try { $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_DIR%\%SHORTCUT_NAME%'); $Shortcut.TargetPath = '%CURRENT_DIR%\VisoLingua.exe'; $Shortcut.WorkingDirectory = '%CURRENT_DIR%'; $Shortcut.Description = 'VisoLingua - Live Translation Overlay Tool'; $Shortcut.Save(); Write-Host 'Shortcut created successfully' } catch { Write-Host 'Error:' $_.Exception.Message; exit 1 }"

if %errorlevel% equ 0 (
    echo ✅ Desktop shortcut created successfully!
    echo    Location: %DESKTOP_DIR%\%SHORTCUT_NAME%
) else (
    echo ❌ Failed to create desktop shortcut
    echo    Try running as administrator if the problem persists
)

pause
'@

Set-Content -Path "$portableDir/Create Desktop Shortcut.bat" -Value $shortcutContent -Encoding ASCII
Write-Host "✅ Shortcut script created"