@echo off
REM VisoLingua Installer Builder
REM This script creates a professional Windows installer using NSIS

echo ============================================================
echo    VisoLingua Professional Installer Builder
echo ============================================================
echo.

REM Check if makensis (NSIS) is available
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NSIS (Nullsoft Scriptable Install System) not found!
    echo.
    echo Please install NSIS from: https://nsis.sourceforge.io/
    echo Make sure makensis.exe is in your PATH.
    echo.
    echo Alternative: Use the simple install_windows.bat script instead.
    pause
    exit /b 1
)

REM Check if VisoLingua.exe exists in dist folder
if not exist "dist\VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found in dist folder!
    echo.
    echo Please build the executable first using: build.bat
    pause
    exit /b 1
)

REM Check if installer script exists
if not exist "installer.nsi" (
    echo ERROR: installer.nsi not found!
    echo Please make sure the NSIS installer script is present.
    pause
    exit /b 1
)

echo Building professional installer...
echo.

REM Build the installer
makensis installer.nsi

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo INSTALLER BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo Professional installer created:
    echo   📦 VisoLingua-Setup-1.0.0.exe
    echo.
    echo Features included:
    echo   • Professional installation wizard
    echo   • Start Menu integration
    echo   • Desktop shortcut option
    echo   • Proper Windows uninstaller
    echo   • Registry entries for Add/Remove Programs
    echo   • Optional autostart with Windows
    echo.
    echo You can now distribute this installer to any Windows computer.
    echo.
) else (
    echo.
    echo ============================================================
    echo INSTALLER BUILD FAILED!
    echo ============================================================
    echo Please check the error messages above.
    echo.
    echo Alternative: Use install_windows.bat for a simpler installation.
)

pause