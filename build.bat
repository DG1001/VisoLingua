@echo off
REM VisoLingua Windows Build Script
REM This script builds a standalone Windows executable

echo ============================================================
echo    VisoLingua Windows Executable Builder
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Please run this script from the VisoLingua directory.
    pause
    exit /b 1
)

REM Install PyInstaller if not present
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller!
        pause
        exit /b 1
    )
)

REM Run the build script
echo.
echo Starting build process...
python build_exe.py

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo BUILD COMPLETED SUCCESSFULLY!
    echo ============================================================
    echo.
    echo Your VisoLingua.exe is ready in the 'dist' folder.
    echo You can now distribute this single file to any Windows computer.
    echo.
    echo To test: 
    echo   cd dist
    echo   VisoLingua.exe
    echo.
    echo Or use: dist\VisoLingua.exe
    echo.
) else (
    echo.
    echo ============================================================
    echo BUILD FAILED!
    echo ============================================================
    echo Please check the error messages above.
)

pause