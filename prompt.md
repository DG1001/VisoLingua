# VisoLingua - Live Translation Overlay Tool - Claude Code Prompt

## Projekt-Übersicht

Erstelle ein **Live-Übersetzungs-Overlay-Tool** mit dem Namen "VisoLingua" in Python, das ein transparentes Fenster über andere Anwendungen legt, Screenshots des darunter liegenden Bereichs an LLMs sendet und Übersetzungen in einem separaten Tab anzeigt.

**Basis-Referenz**: [OverText Repository](https://github.com/thiswillbeyourgithub/OverText) - verwende dieses als Inspiration für die transparente Overlay-Funktionalität.

## Kern-Features

### 1. **Transparentes Capture-Fenster**
- **Startverhalten**: Transparentes Fenster öffnet sich automatisch beim Programmstart
- **Verschiebbar**: Drag & Drop über die Titelleiste 
- **Größenänderung**: Resize-Handle in der rechten unteren Ecke
- **Transparenz**: Vollständig transparent, nur Rahmen sichtbar
- **Always-on-Top**: Bleibt über anderen Fenstern

### 2. **Screenshot & LLM-Integration**
- **Trigger**: Klick ins transparente Fenster erfasst den darunter liegenden Bereich
- **LLM-Auswahl**: Konfigurierbar zwischen Gemini 2.5 Flash und GPT-4.1 Mini/Nano
- **Spracherkennung**: Automatische Erkennung der Quellsprache (Fokus: **Chinesisch → Deutsch**)
- **Optimierung**: Bildkompression für schnelle API-Calls

### 3. **Dual-Tab-System**
- **Tab 1 - Capture**: Transparentes Overlay-Fenster
- **Tab 2 - Ergebnis**: Opakes Fenster mit Übersetzungstext
- **Umschaltung**: Platzsparend über **Doppelklick auf Titelleiste** oder Hotkey
- **Ergbnis-Features**: Text kopierbar, scrollbar, formatiert

## Technische Anforderungen

### **Tech-Stack**
# Kern-Dependencies
- tkinter          # GUI & Overlay
- mss              # Ultra-schnelle Screenshots  
- Pillow           # Bildverarbeitung
- requests         # LLM API calls
- asyncio          # Asynchrone Verarbeitung
- configparser     # Settings
- pyperclip        # Clipboard-Integration
- pystray          # System Tray (optional)

### **Projekt-Struktur**
```
translation-overlay/
├── main.py              # Entry point
├── config/
│   ├── settings.py      # Konfiguration & API-Keys
│   └── config.ini       # User settings
├── ui/
│   ├── overlay.py       # Transparentes Capture-Fenster
│   ├── result_window.py # Ergebnis-Tab
│   └── components.py    # UI-Komponenten
├── core/
│   ├── screenshot.py    # Screen capture logic
│   ├── translator.py    # LLM API integration
│   └── cache.py         # Translation caching
├── utils/
│   ├── helpers.py       # Utility functions
│   └── constants.py     # App constants
└── assets/
    ├── icons/           # App icons
    └── styles/          # UI styling
```
## Detaillierte Feature-Spezifikationen

### **Capture-Fenster (Tab 1)**
# Technische Requirements
- Transparenz: 90-95% transparent, nur dünner Rahmen
- Mindestgröße: 200x200 pixels
- Maximale Größe: Bildschirmauflösung
- Rahmenfarbe: Anpassbar (Standard: Rot/Grün für Aktiv/Inaktiv)
- Cursor: Changes to crosshair beim Hover
- Feedback: Kurzer visueller Feedback beim Screenshot

### **LLM-Integration**
```python
# API-Unterstützung
SUPPORTED_LLMS = {
    'gemini-2.5-flash': {
        'endpoint': 'https://generativelanguage.googleapis.com/v1beta/',
        'max_image_size': '4MB',
        'cost_per_1m_tokens': {'input': 0.10, 'output': 0.40}
    },
    'gpt-4.1-mini': {
        'endpoint': 'https://api.openai.com/v1/',
        'max_image_size': '20MB', 
        'cost_per_1m_tokens': {'input': 0.40, 'output': 1.60}
    },
    'gpt-4.1-nano': {
        'endpoint': 'https://api.openai.com/v1/',
        'max_image_size': '20MB',
        'cost_per_1m_tokens': {'input': 0.15, 'output': 0.60}  # geschätzt
    }
}

# Translation Prompt Template
TRANSLATION_PROMPT = """
Du bist ein Experte für Chinesisch-Deutsch-Übersetzung. 
Analysiere das Bild und:
1. Erkenne automatisch die Quellsprache
2. Übersetze ALLEN erkannten Text ins Deutsche
3. Behalte die ursprüngliche Formatierung bei
4. Bei mehreren Textblöcken: nummeriere sie

Ausgabeformat:
**Erkannte Sprache:** [Sprache]
**Übersetzung:**
[übersetzter Text]
"""
```

### **Ergebnis-Fenster (Tab 2)**
# UI-Features
- Scrollbares Textfeld mit letzter Übersetzung
- "Kopieren"-Button für gesamten Text
- "Verlauf"-Dropdown mit letzten 10 Übersetzungen
- "Ergebnis löschen"-Button
- "Einstellungen"-Button für LLM-Konfiguration
- Status-Anzeige: API-Kosten, Verarbeitungszeit, Fehler

# Fenster-Properties
- Größe: 400x300 minimum, resizable
- Position: Zentriert oder letzte Position speichern
- Opacity: 100% (nicht transparent)

### **Konfiguration & Settings**
# config.ini Structure
```
[api]
default_llm = gemini-2.5-flash
gemini_api_key = 
openai_api_key = 

[ui]
overlay_transparency = 0.05
overlay_border_color = #FF0000
overlay_border_width = 2
always_on_top = true
auto_save_position = true

[translation]
source_language = auto
target_language = de
cache_translations = true
max_cache_entries = 100

[hotkeys]
toggle_tabs = ctrl+tab
take_screenshot = click
copy_result = ctrl+c
```

## Implementation-Leitlinien

### **1. Overlay-Architektur**
- Basiere das transparente Fenster auf **OverText-Prinzipien**
- Verwende `tkinter.Toplevel()` mit `attributes('-alpha', 0.05)`  
- Implementiere Custom-Resize-Handles mit Mouse-Events
- Stelle sicher, dass das Fenster interaktiv bleibt trotz Transparenz

### **2. Screenshot-Optimierung**
#### Effizienter Screenshot-Workflow
1. Erfasse nur den Overlay-Bereich (nicht gesamter Bildschirm)
2. Komprimiere Bild für LLM (JPEG, 85% Qualität)
3. Cache identische Screenshots (MD5-Hash)
4. Async processing um UI nicht zu blockieren

### **3. Tab-Switching-Mechanismus**
#### Smart Tab Management
- Ein tkinter.Tk() Hauptfenster
- Dynamisches Umschalten zwischen transparency und opacity
- Behalte Fensterposition beim Umschalten
- Smooth transitions (optional: fade animation)

### **4. Error Handling & UX**
#### Robuste Fehlerbehandlung
- API-Fehler: Fallback auf anderen LLM oder Retry
- Netzwerk-Timeout: User-freundliche Fehlermeldung
- Invalid Screenshots: Validierung vor API-Call
- Rate Limiting: Intelligente Backoff-Strategie

### **5. Performance-Optimierungen**
- **Caching**: Identische Bilder nicht erneut übersetzen
- **Lazy Loading**: LLM-APIs erst bei Bedarf initialisieren  
- **Background Processing**: Screenshots und API-Calls in separaten Threads
- **Memory Management**: Alte Screenshots nach Zeit oder Anzahl löschen

## Spezielle Anforderungen für Chinesisch

### **Font & Rendering**
#### Chinesische Zeichen-Unterstützung
- Font: "Microsoft YaHei", "SimHei", oder System-Standard
- Unicode: Volle UTF-8-Unterstützung
- Rendering: Anti-Aliasing für bessere Lesbarkeit

### **OCR-Optimierung**
```python
# LLM-Prompt-Optimierung für Chinesisch
CHINESE_OPTIMIZED_PROMPT = """
Speziell für chinesischen Text:
- Erkenne sowohl vereinfachte als auch traditionelle Zeichen
- Beachte Kontext für mehrdeutige Zeichen
- Übersetze idiomatische Ausdrücke sinngemäß
- Bei technischen Begriffen: gib auch englische Entsprechung an
"""
```

## Cross-Platform-Kompatibilität

### **Windows-Optimierungen**
#### Windows-spezifische Features
- DPI-Awareness für HiDPI-Displays
- Windows-native Transparenz-APIs
- Taskbar-Integration optional

### **Linux/macOS-Anpassungen**
#### Plattform-spezifische Adjustments
- X11/Wayland-Kompatibilität für Linux
- macOS: Cocoa-Integration für native Overlays
- Cursor-Handling per Plattform anpassen

## Deployment & Distribution

### **PyInstaller-Setup**
```bash
# Build-Command für standalone executable
pyinstaller --onefile --windowed \
  --add-data "config;config" \
  --add-data "assets;assets" \
  --icon="assets/icons/app.ico" \
  --name="TranslationOverlay" \
  main.py
```

### **First-Run-Setup**
#### Initial Setup Wizard
1. API-Keys eingeben (Gemini/OpenAI)
2. Standard-LLM auswählen
3. Hotkeys konfigurieren
4. Quick Tutorial für Bedienung

## Testing & Quality Assurance

### **Test-Cases**
#### Kritische Test-Szenarien
- Screenshot verschiedener Bildschirmregionen
- API-Ausfälle und Timeouts
- Sehr große/kleine Overlay-Fenster
- Schnelle aufeinanderfolgende Screenshots
- Chinesische Zeichen-Rendering
- Tab-Switching unter verschiedenen Bedingungen

**Zusätzliche Referenzen:**
- GitHub: https://github.com/thiswillbeyourgithub/OverText
- Orientiere dich an bewährten Patterns für transparente Overlays

**Ziel:** Ein benutzerfreundliches, performantes Tool für Live-Übersetzung mit Fokus auf chinesische Texte und nahtlose Desktop-Integration.
