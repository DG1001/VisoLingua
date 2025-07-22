param($portableDir)

$launcherContent = @'
@echo off
REM VisoLingua Portable Launcher

echo Starting VisoLingua...

REM Check if config exists, create if not
if not exist "config.ini" (
    echo First run - creating default config...
    echo Please configure your API keys in the Settings window.
    echo.
)

REM Start the application
start "" "VisoLingua.exe"

REM Optional: Wait and check if it started
timeout /t 2 /nobreak >nul
tasklist /fi "imagename eq VisoLingua.exe" | find /i "VisoLingua.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ VisoLingua started successfully!
) else (
    echo ⚠️  VisoLingua may have failed to start.
    echo Check for error messages or missing dependencies.
    pause
)
'@

Set-Content -Path "$portableDir/Start VisoLingua.bat" -Value $launcherContent -Encoding ASCII
Write-Host "✅ Launcher script created"