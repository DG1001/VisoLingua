# VisoLingua Deployment Guide

## 📦 Antwort auf deine Frage: Config-Datei

### ✅ **NEU: Automatische config.ini Erstellung**

Nach dem Update erstellt VisoLingua automatisch eine `config.ini` **neben der EXE-Datei**, wenn keine vorhanden ist.

### 🎯 **Zwei Deployment-Optionen:**

## Option 1: Nur EXE (Minimalist)
```
# Einfach kopieren:
VisoLingua.exe

# Was passiert:
# ✅ Beim ersten Start wird config.ini automatisch erstellt
# ✅ Funktioniert sofort (mit Standard-Einstellungen)
# ⚠️  Benutzer muss API-Keys in Settings eingeben
```

## Option 2: Portable Package (Empfohlen)
```batch
# Vollständiges Package erstellen:
create_portable.bat

# Ergebnis: VisoLingua-Portable/ Ordner mit:
# ✅ VisoLingua.exe
# ✅ config.ini (vorkonfiguriert)
# ✅ Start VisoLingua.bat (Launcher)
# ✅ Create Desktop Shortcut.bat
# ✅ PORTABLE_README.txt
# ✅ Dokumentation
```

## 🔧 **Technische Details:**

### Config-Speicherort:
- **Als EXE**: `config.ini` im gleichen Ordner wie `VisoLingua.exe`
- **Als Python**: `config/config.ini` (wie bisher)

### Erste Verwendung:
1. **EXE starten** → `config.ini` wird automatisch erstellt
2. **Settings öffnen** → API-Keys eingeben
3. **Fertig!** → App ist konfiguriert

## 🚀 **Empfohlener Workflow:**

### Für dich (Entwickler):
```batch
# 1. Neue EXE mit Config-Fix bauen
python build_exe.py

# 2. Portable Package erstellen
create_portable.bat

# 3. Testen
cd VisoLingua-Portable
"Start VisoLingua.bat"
```

### Für Endbenutzer:
```batch
# Option A: Nur EXE
VisoLingua.exe  # → config.ini wird automatisch erstellt

# Option B: Portable Package (empfohlen)
"Start VisoLingua.bat"  # → Alles vorbereitet
```

## 📋 **Deployment-Szenarien:**

### 🎯 **Szenario 1: Einfache Distribution**
**Was weitergeben**: Nur `VisoLingua.exe`
- ✅ **Vorteil**: Einzelne Datei
- ✅ **Config**: Wird automatisch erstellt
- ⚠️  **Setup**: Benutzer muss API-Keys selbst eingeben

### 🎯 **Szenario 2: Benutzerfreundlich**
**Was weitergeben**: Ganzer `VisoLingua-Portable/` Ordner
- ✅ **Vorteil**: Sofort startklar
- ✅ **Launcher**: "Start VisoLingua.bat"
- ✅ **Anleitung**: PORTABLE_README.txt
- ✅ **Shortcuts**: Desktop-Icon Creator

### 🎯 **Szenario 3: Mit vorkonfigurierten API-Keys**
```batch
# 1. Portable Package erstellen
create_portable.bat

# 2. config.ini bearbeiten (API-Keys eintragen)
notepad VisoLingua-Portable\config.ini

# 3. Verteilen → Sofort einsatzbereit!
```

## 🛠️ **Nach dem Update:**

Du musst die **EXE neu bauen**, damit die Config-Änderungen wirksam werden:

```batch
# Wichtig: EXE neu bauen für Config-Fix!
python build_exe.py

# Dann portable Package erstellen
create_portable.bat
```

## 💡 **Antwort auf deine Frage:**

> **"Wird automatisch eine ini angelegt?"**

**✅ JA!** Nach dem Update:
- EXE irgendwo ablegen → `config.ini` wird beim ersten Start automatisch neben der EXE erstellt
- **ODER** das portable Package verwenden → `config.ini` ist bereits dabei

**Empfehlung**: Portable Package verwenden für beste Benutzererfahrung! 🎉