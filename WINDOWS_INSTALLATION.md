# VisoLingua Windows Installation Guide

VisoLingua kann auf verschiedene Weise als echte Windows-App installiert werden. Hier sind alle verfügbaren Optionen:

## 🚀 Option 1: Standalone EXE (Empfohlen)

### Schritt 1: EXE erstellen
```batch
# Einfachste Methode - alles automatisch
build.bat

# Oder manuell
python build_exe.py
```

**Ergebnis**: `dist/VisoLingua.exe` (~50-100MB) - Einzelne Datei, funktioniert auf jedem Windows-PC

### Schritt 2: Desktop-Icon erstellen (Optional)
```batch
# In den dist/ Ordner wechseln
cd dist

# Desktop-Shortcut erstellen
..\create_shortcut.bat
```

## 🏗️ Option 2: Vollständige Windows-Installation

### Automatische Installation mit Admin-Rechten
```batch
# 1. EXE erstellen (falls noch nicht geschehen)
build.bat

# 2. In den dist/ Ordner wechseln
cd dist

# 3. Als Administrator ausführen
..\install_windows.bat
```

**Was passiert:**
- ✅ Installation nach `C:\Program Files\VisoLingua\`
- ✅ Desktop-Shortcut
- ✅ Start Menu Eintrag
- ✅ Windows "Programme hinzufügen/entfernen" Integration
- ✅ Automatischer Uninstaller

## 🎯 Option 3: Professioneller Installer (Erweitert)

### Voraussetzungen
1. [NSIS](https://nsis.sourceforge.io/) installieren
2. NSIS zu Windows PATH hinzufügen

### Installer erstellen
```batch
# 1. EXE erstellen
build.bat

# 2. Professionellen Installer erstellen
build_installer.bat
```

**Ergebnis**: `VisoLingua-Setup-1.0.0.exe` - Professioneller Installer mit Wizard

## 📋 Verfügbare Dateien

Nach dem Erstellen finden Sie folgende Dateien:

```
VisoLingua/
├── build.bat                    # EXE erstellen
├── build_exe.py                 # Python Build-Skript
├── create_shortcut.bat          # Desktop-Icon erstellen
├── install_windows.bat          # Vollinstallation
├── installer.nsi               # NSIS Installer-Konfiguration
├── build_installer.bat         # Professionellen Installer erstellen
├── assets/icons/app.ico        # Windows App-Icon
└── dist/
    ├── VisoLingua.exe          # Standalone Anwendung
    └── Start_VisoLingua.bat    # Launcher mit Fehlererkennung
```

## 🎮 Verwendung

### Einfach (Option 1)
1. `build.bat` ausführen
2. `dist/VisoLingua.exe` doppelklicken
3. Fertig! 🎉

### Mit Desktop-Icon
1. Obige Schritte + `create_shortcut.bat`
2. VisoLingua-Icon auf Desktop doppelklicken

### Vollinstallation (Option 2)
1. `build.bat` → `cd dist` → `install_windows.bat` (als Admin)
2. VisoLingua über Start Menu oder Desktop starten

### Professioneller Installer (Option 3)
1. `build_installer.bat` ausführen
2. `VisoLingua-Setup-1.0.0.exe` an andere weitergeben
3. Empfänger führt Setup aus → Automatische Installation

## 🔧 Erweiterte Features

### Autostart mit Windows (Option 3)
Der professionelle Installer bietet Option für automatischen Start mit Windows.

### System Tray Integration
Geplant für zukünftige Versionen - VisoLingua minimiert in die Taskleiste.

### Globale Hotkeys
Geplant - VisoLingua über Tastenkürzel von überall aufrufen.

## 🛠️ Troubleshooting

### "Python not found"
- Python 3.8+ installieren und zu PATH hinzufügen

### "PyInstaller not found"
```batch
pip install pyinstaller
```

### "makensis not found"
- [NSIS](https://nsis.sourceforge.io/) installieren
- Oder Option 1/2 verwenden (kein NSIS nötig)

### EXE startet nicht
- Windows Defender/Antivirus deaktivieren (false positive)
- `Start_VisoLingua.bat` für bessere Fehlermeldungen verwenden

### Admin-Rechte erforderlich
- Rechtsklick auf Batch-Datei → "Als Administrator ausführen"

## 📦 Distribution

### Für Endbenutzer
- **Einfach**: `VisoLingua.exe` + `create_shortcut.bat`
- **Professionell**: `VisoLingua-Setup-1.0.0.exe`

### Für Entwickler
- Vollständiges Repository mit allen Build-Skripten

## 🎯 Empfohlener Workflow

1. **Entwicklung**: Python-Version verwenden
2. **Testing**: `build.bat` → EXE testen
3. **Distribution**: `build_installer.bat` → Setup.exe verteilen
4. **Endbenutzer**: Setup.exe ausführen → Fertig installiert

## 💡 Next Steps

Nach erfolgreicher Installation:
1. API-Keys in Settings konfigurieren
2. README.md für Bedienungsanleitung lesen
3. SETUP.md für detaillierte Konfiguration

VisoLingua ist jetzt eine echte Windows-App! 🎉