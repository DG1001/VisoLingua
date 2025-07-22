@echo off
REM Create portable VisoLingua package for distribution

echo ============================================================
echo    Creating Portable VisoLingua Package
echo ============================================================
echo.

REM Check if EXE exists
if not exist "dist\VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found!
    echo Please build it first with: build.bat
    pause
    exit /b 1
)

REM Create portable directory
set "PORTABLE_DIR=VisoLingua-Portable"
if exist "%PORTABLE_DIR%" rmdir /s /q "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%"

echo Creating portable package...

REM Copy main executable
copy "dist\VisoLingua.exe" "%PORTABLE_DIR%\" >nul
echo   ✅ VisoLingua.exe copied

REM Copy default config file
copy "config\config.ini" "%PORTABLE_DIR%\" >nul
echo   ✅ Default config.ini copied

REM Copy documentation
copy "README.md" "%PORTABLE_DIR%\" >nul 2>nul
copy "SETUP.md" "%PORTABLE_DIR%\" >nul 2>nul
copy "WINDOWS_INSTALLATION.md" "%PORTABLE_DIR%\" >nul 2>nul
echo   ✅ Documentation copied

REM Create launcher script
(
echo @echo off
echo REM VisoLingua Portable Launcher
echo.
echo echo Starting VisoLingua...
echo.
echo REM Check if config exists, create if not
echo if not exist "config.ini" ^(
echo     echo First run - creating default config...
echo     echo Please configure your API keys in the Settings window.
echo     echo.
echo ^)
echo.
echo REM Start the application
echo start "" "VisoLingua.exe"
echo.
echo REM Optional: Wait and check if it started
echo timeout /t 2 /nobreak ^>nul
echo tasklist /fi "imagename eq VisoLingua.exe" ^| find /i "VisoLingua.exe" ^>nul
echo if %%errorlevel%% equ 0 ^(
echo     echo ✅ VisoLingua started successfully!
echo ^) else ^(
echo     echo ⚠️  VisoLingua may have failed to start.
echo     echo Check for error messages or missing dependencies.
echo     pause
echo ^)
) > "%PORTABLE_DIR%\Start VisoLingua.bat"
echo   ✅ Launcher script created

REM Create desktop shortcut script
(
echo @echo off
echo REM Create Desktop Shortcut for VisoLingua Portable
echo.
echo set "CURRENT_DIR=%%CD%%"
echo set "SHORTCUT_NAME=VisoLingua.lnk"
echo.
echo echo Creating desktop shortcut...
echo echo Target: %%CURRENT_DIR%%\VisoLingua.exe
echo.
echo REM Try to find the correct desktop path ^(OneDrive or local^)
echo set "DESKTOP_DIR=%%USERPROFILE%%\Desktop"
echo if not exist "%%DESKTOP_DIR%%" ^(
echo     set "DESKTOP_DIR=%%USERPROFILE%%\OneDrive\Desktop"
echo ^)
echo if not exist "%%DESKTOP_DIR%%" ^(
echo     set "DESKTOP_DIR=%%PUBLIC%%\Desktop"
echo ^)
echo.
echo echo Desktop path: %%DESKTOP_DIR%%
echo.
echo REM Check if desktop folder exists
echo if not exist "%%DESKTOP_DIR%%" ^(
echo     echo ❌ Desktop folder not found. Checked:
echo     echo    - %%USERPROFILE%%\Desktop
echo     echo    - %%USERPROFILE%%\OneDrive\Desktop  
echo     echo    - %%PUBLIC%%\Desktop
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Check if executable exists
echo if not exist "%%CURRENT_DIR%%\VisoLingua.exe" ^(
echo     echo ❌ VisoLingua.exe not found in current directory
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Create shortcut with proper error handling
echo powershell -ExecutionPolicy Bypass -Command "try { $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%%DESKTOP_DIR%%\%%SHORTCUT_NAME%%'); $Shortcut.TargetPath = '%%CURRENT_DIR%%\VisoLingua.exe'; $Shortcut.WorkingDirectory = '%%CURRENT_DIR%%'; $Shortcut.Description = 'VisoLingua - Live Translation Overlay Tool'; $Shortcut.Save(); Write-Host 'Shortcut created successfully' } catch { Write-Host 'Error:' $_.Exception.Message; exit 1 }"
echo.
echo if %%errorlevel%% equ 0 ^(
echo     echo ✅ Desktop shortcut created successfully!
echo     echo    Location: %%DESKTOP_DIR%%\%%SHORTCUT_NAME%%
echo ^) else ^(
echo     echo ❌ Failed to create desktop shortcut
echo     echo    Try running as administrator if the problem persists
echo ^)
echo.
echo pause
) > "%PORTABLE_DIR%\Create Desktop Shortcut.bat"
echo   ✅ Shortcut creator added

REM Create README for portable version
(
echo # VisoLingua Portable
echo.
echo Diese portable Version von VisoLingua benötigt keine Installation.
echo.
echo ## Erste Verwendung:
echo.
echo 1. **Starten**: Doppelklick auf "Start VisoLingua.bat"
echo 2. **API-Keys**: Einstellungen öffnen und API-Schlüssel eingeben
echo 3. **Desktop-Icon** ^(optional^): "Create Desktop Shortcut.bat" ausführen
echo.
echo ## Dateien:
echo.
echo - `VisoLingua.exe` - Hauptanwendung
echo - `config.ini` - Konfigurationsdatei ^(wird beim ersten Start erstellt^)
echo - `Start VisoLingua.bat` - Empfohlener Starter
echo - `Create Desktop Shortcut.bat` - Desktop-Icon erstellen
echo.
echo ## API-Keys konfigurieren:
echo.
echo 1. VisoLingua starten
echo 2. Settings-Button klicken
echo 3. API-Keys eingeben:
echo    - **Gemini**: https://aistudio.google.com/
echo    - **OpenAI**: https://platform.openai.com/
echo 4. Standard-LLM auswählen ^(empfohlen: Gemini 2.5 Flash^)
echo 5. Speichern
echo.
echo ## Verwendung:
echo.
echo 1. Rotes Overlay-Fenster über Text positionieren
echo 2. In das Fenster klicken
echo 3. Übersetzung wird automatisch angezeigt
echo 4. "Back to Capture" für neue Übersetzung
echo.
echo Vollständige Anleitung: README.md
) > "%PORTABLE_DIR%\PORTABLE_README.txt"
echo   ✅ Portable README created

echo.
echo ============================================================
echo PORTABLE PACKAGE CREATED SUCCESSFULLY!
echo ============================================================
echo.
echo 📁 Package location: %PORTABLE_DIR%\
echo.
echo 📦 Package contents:
echo   • VisoLingua.exe ^(Main application^)
echo   • config.ini ^(Default configuration^)
echo   • Start VisoLingua.bat ^(Recommended launcher^)
echo   • Create Desktop Shortcut.bat ^(Desktop icon creator^)
echo   • PORTABLE_README.txt ^(Quick start guide^)
echo   • Documentation files
echo.
echo 🚀 To use:
echo   1. Copy entire '%PORTABLE_DIR%' folder anywhere
echo   2. Run "Start VisoLingua.bat"
echo   3. Configure API keys in Settings
echo.
echo 💾 To distribute:
echo   - ZIP the '%PORTABLE_DIR%' folder
echo   - Send to users - no installation required!
echo.

pause