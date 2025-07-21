@echo off
REM Quick launcher for VisoLingua

echo Starting VisoLingua...

if exist "dist\VisoLingua.exe" (
    echo ✅ Found VisoLingua.exe
    start "" "dist\VisoLingua.exe"
    echo 🚀 VisoLingua started!
) else (
    echo ❌ VisoLingua.exe not found in dist folder!
    echo Please build it first with: build.bat
    pause
)