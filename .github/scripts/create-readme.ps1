param($portableDir)

$readmeContent = @'
# VisoLingua Portable

Diese portable Version von VisoLingua benötigt keine Installation.

## Erste Verwendung:

1. **Starten**: Doppelklick auf "Start VisoLingua.bat"
2. **API-Keys**: Einstellungen öffnen und API-Schlüssel eingeben
3. **Desktop-Icon** (optional): "Create Desktop Shortcut.bat" ausführen

## Dateien:

- `VisoLingua.exe` - Hauptanwendung
- `config.ini` - Konfigurationsdatei (wird beim ersten Start erstellt)
- `Start VisoLingua.bat` - Empfohlener Starter
- `Create Desktop Shortcut.bat` - Desktop-Icon erstellen

## API-Keys konfigurieren:

1. VisoLingua starten
2. Settings-Button klicken
3. API-Keys eingeben:
   - **Gemini**: https://aistudio.google.com/
   - **OpenAI**: https://platform.openai.com/
4. Standard-LLM auswählen (empfohlen: Gemini 2.5 Flash)
5. Speichern

## Verwendung:

1. Rotes Overlay-Fenster über Text positionieren
2. In das Fenster klicken
3. Übersetzung wird automatisch angezeigt
4. "Back to Capture" für neue Übersetzung

Vollständige Anleitung: README.md
'@

Set-Content -Path "$portableDir/PORTABLE_README.txt" -Value $readmeContent -Encoding UTF8
Write-Host "✅ Portable README created"