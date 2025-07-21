@echo off
REM VisoLingua Windows Installation Script
REM This script installs VisoLingua as a proper Windows application

setlocal EnableDelayedExpansion

echo ============================================================
echo    VisoLingua Windows Installation
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This installation requires administrator privileges.
    echo Please run this script as administrator.
    echo.
    pause
    exit /b 1
)

REM Check if VisoLingua.exe exists
if not exist "VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found!
    echo Please make sure VisoLingua.exe is in the same directory as this script.
    echo.
    echo You can build it using: build.bat
    pause
    exit /b 1
)

REM Define installation paths
set "INSTALL_DIR=%ProgramFiles%\VisoLingua"
set "DESKTOP_SHORTCUT=%USERPROFILE%\Desktop\VisoLingua.lnk"
set "STARTMENU_SHORTCUT=%ProgramData%\Microsoft\Windows\Start Menu\Programs\VisoLingua.lnk"

echo Installing VisoLingua...
echo.

REM Create installation directory
echo Creating installation directory...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create installation directory!
        pause
        exit /b 1
    )
)

REM Copy files
echo Copying application files...
copy "VisoLingua.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: Failed to copy VisoLingua.exe!
    pause
    exit /b 1
)

REM Copy additional files if they exist
if exist "config" xcopy "config" "%INSTALL_DIR%\config\" /E /I /Q >nul
if exist "assets" xcopy "assets" "%INSTALL_DIR%\assets\" /E /I /Q >nul
if exist "README.md" copy "README.md" "%INSTALL_DIR%\" >nul
if exist "SETUP.md" copy "SETUP.md" "%INSTALL_DIR%\" >nul

REM Create uninstaller
echo Creating uninstaller...
(
echo @echo off
echo REM VisoLingua Uninstaller
echo echo Uninstalling VisoLingua...
echo.
echo REM Remove shortcuts
echo if exist "%DESKTOP_SHORTCUT%" del "%DESKTOP_SHORTCUT%"
echo if exist "%STARTMENU_SHORTCUT%" del "%STARTMENU_SHORTCUT%"
echo.
echo REM Remove installation directory
echo rmdir /s /q "%INSTALL_DIR%"
echo.
echo REM Remove registry entries
echo reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /f 2^>nul
echo.
echo echo VisoLingua has been uninstalled.
echo pause
) > "%INSTALL_DIR%\uninstall.bat"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\VisoLingua.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'VisoLingua - Live Translation Overlay Tool'; $Shortcut.Save()}"

REM Create start menu shortcut
echo Creating start menu shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU_SHORTCUT%'); $Shortcut.TargetPath = '%INSTALL_DIR%\VisoLingua.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'VisoLingua - Live Translation Overlay Tool'; $Shortcut.Save()}"

REM Add to Windows registry for proper uninstall
echo Registering with Windows...
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "DisplayName" /t REG_SZ /d "VisoLingua" /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "DisplayVersion" /t REG_SZ /d "1.0.0" /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "Publisher" /t REG_SZ /d "VisoLingua Team" /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "UninstallString" /t REG_SZ /d "%INSTALL_DIR%\uninstall.bat" /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "InstallLocation" /t REG_SZ /d "%INSTALL_DIR%" /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "NoModify" /t REG_DWORD /d 1 /f >nul
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\VisoLingua" /v "NoRepair" /t REG_DWORD /d 1 /f >nul

echo.
echo ============================================================
echo INSTALLATION COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo VisoLingua has been installed to:
echo   %INSTALL_DIR%
echo.
echo Shortcuts created:
echo   • Desktop: VisoLingua.lnk
echo   • Start Menu: VisoLingua.lnk
echo.
echo You can now:
echo   • Double-click the desktop icon to start VisoLingua
echo   • Find VisoLingua in your Start Menu
echo   • Uninstall via "Add or Remove Programs" in Windows Settings
echo.
echo To start VisoLingua now, press any key...
pause >nul
start "" "%INSTALL_DIR%\VisoLingua.exe"