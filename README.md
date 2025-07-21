# VisoLingua - Live Translation Overlay Tool

Ein benutzerfreundliches Desktop-Tool für Live-Übersetzung mit transparentem Overlay-Fenster, optimiert für chinesische Texte.

## Features

- **Transparentes Capture-Fenster**: Verschiebbar und größenverstellbar über anderen Anwendungen
- **LLM-Integration**: Unterstützt Gemini 2.5 Flash und GPT-4 Mini/Nano
- **Dual-Tab-System**: Wechsel zwischen Capture- und Ergebnis-Modus
- **Chinesisch-Fokus**: Optimiert für vereinfachte und traditionelle chinesische Zeichen
- **Caching**: Intelligente Zwischenspeicherung für identische Screenshots
- **Verlauf**: Speicherung der letzten Übersetzungen

## Installation

1. Python 3.8+ installieren
2. Dependencies installieren:
```bash
pip install -r requirements.txt
```

## Konfiguration

1. Bei erstem Start werden Standardkonfigurationsdateien erstellt
2. API-Schlüssel in den Einstellungen konfigurieren:
   - Gemini API Key (Google AI Studio)
   - OpenAI API Key (OpenAI Platform)

## Verwendung

1. Anwendung starten:
```bash
python main.py
```

2. **Capture-Modus**: Transparentes Fenster positionieren und auf den zu übersetzenden Bereich klicken
3. **Ergebnis-Modus**: Übersetzung wird automatisch angezeigt
4. **Wechseln**: Doppelklick auf Titelleiste oder Strg+Tab

## Hotkeys

- `Strg+Tab`: Zwischen Modi wechseln
- `Strg+C`: Übersetzung kopieren (im Ergebnis-Modus)
- `Esc`: Ergebnis-Fenster schließen

## Projektstruktur

```
VisoLingua/
├── main.py              # Hauptprogramm
├── config/
│   ├── settings.py      # Konfigurationsverwaltung
│   └── config.ini       # Benutzereinstellungen
├── ui/
│   ├── overlay.py       # Transparentes Overlay
│   └── result_window.py # Ergebnisfenster
├── core/
│   ├── screenshot.py    # Screenshot-Erfassung
│   └── translator.py    # LLM-Integration
├── utils/
│   ├── helpers.py       # Hilfsfunktionen
│   └── constants.py     # Konstanten
└── requirements.txt     # Dependencies
```

## Unterstützte LLMs

- **Gemini 2.5 Flash**: Schnell und kostengünstig
- **GPT-4.1 Mini**: Ausgewogenes Preis-Leistungs-Verhältnis  
- **GPT-4.1 Nano**: Experimentell (verwendet GPT-4o-mini)

## Systemanforderungen

- Python 3.8+
- Windows/Linux/macOS
- Internetverbindung für LLM-APIs
- Mindestens 4GB RAM empfohlen

## Lizenz

Dieses Projekt dient ausschließlich defensiven Sicherheitszwecken und Sprachlernunterstützung.

## Entwicklung

Basiert auf den Prinzipien des [OverText](https://github.com/thiswillbeyourgithub/OverText) Repositories für transparente Overlay-Funktionalität.