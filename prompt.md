# VisoLingua - Live Translation Overlay Tool - Claude Code Prompt

## Project Overview

Create a **Live Translation Overlay Tool** named "VisoLingua" in Python that places a transparent window over other applications, sends screenshots of the underlying area to LLMs, and displays translations in a separate tab.

**Base Reference**: [OverText Repository](https://github.com/thiswillbeyourgithub/OverText) - use this as inspiration for transparent overlay functionality.

## Core Features

### 1. **Transparent Capture Window**
- **Startup Behavior**: Transparent window opens automatically at program start
- **Movable**: Drag & drop via title bar
- **Resizable**: Resize handle in bottom-right corner
- **Transparency**: Fully transparent, only border visible
- **Always-on-Top**: Stays above other windows

### 2. **Screenshot & LLM Integration**
- **Trigger**: Click in transparent window captures the underlying area
- **LLM Selection**: Configurable between Gemini 2.5 Flash and GPT-4.1 Mini/Nano
- **Language Detection**: Automatic source language detection (Focus: **Chinese → German**)
- **Optimization**: Image compression for fast API calls

### 3. **Dual-Tab System**
- **Tab 1 - Capture**: Transparent overlay window
- **Tab 2 - Result**: Opaque window with translation text
- **Switching**: Space-saving via **double-click on title bar** or hotkey
- **Result Features**: Text copyable, scrollable, formatted

## Technical Requirements

### **Tech Stack**
# Core Dependencies
- tkinter          # GUI & overlay
- mss              # Ultra-fast screenshots
- Pillow           # Image processing
- requests         # LLM API calls
- asyncio          # Asynchronous processing
- configparser     # Settings
- pyperclip        # Clipboard integration
- pystray          # System tray (optional)

### **Project Structure**
```
translation-overlay/
├── main.py              # Entry point
├── config/
│   ├── settings.py      # Configuration & API keys
│   └── config.ini       # User settings
├── ui/
│   ├── overlay.py       # Transparent capture window
│   ├── result_window.py # Result tab
│   └── components.py    # UI components
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
## Detailed Feature Specifications

### **Capture Window (Tab 1)**
# Technical Requirements
- Transparency: 90-95% transparent, only thin border
- Minimum size: 200x200 pixels
- Maximum size: Screen resolution
- Border color: Customizable (Default: Red/Green for Active/Inactive)
- Cursor: Changes to crosshair on hover
- Feedback: Brief visual feedback on screenshot

### **LLM Integration**
```python
# API Support
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
        'cost_per_1m_tokens': {'input': 0.15, 'output': 0.60}  # estimated
    }
}

# Translation Prompt Template
TRANSLATION_PROMPT = """
You are an expert in Chinese-German translation.
Analyze the image and:
1. Automatically detect the source language
2. Translate ALL detected text to German
3. Maintain original formatting
4. For multiple text blocks: number them

Output format:
**Detected Language:** [Language]
**Translation:**
[translated text]
"""
```

### **Result Window (Tab 2)**
# UI Features
- Scrollable text field with last translation
- "Copy" button for entire text
- "History" dropdown with last 10 translations
- "Clear Result" button
- "Settings" button for LLM configuration
- Status display: API costs, processing time, errors

# Window Properties
- Size: 400x300 minimum, resizable
- Position: Centered or save last position
- Opacity: 100% (not transparent)

### **Configuration & Settings**
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

## Implementation Guidelines

### **1. Overlay Architecture**
- Base the transparent window on **OverText principles**
- Use `tkinter.Toplevel()` with `attributes('-alpha', 0.05)`
- Implement custom resize handles with mouse events
- Ensure window remains interactive despite transparency

### **2. Screenshot Optimization**
#### Efficient Screenshot Workflow
1. Capture only overlay area (not entire screen)
2. Compress image for LLM (JPEG, 85% quality)
3. Cache identical screenshots (MD5 hash)
4. Async processing to avoid blocking UI

### **3. Tab-Switching Mechanism**
#### Smart Tab Management
- One tkinter.Tk() main window
- Dynamic switching between transparency and opacity
- Maintain window position when switching
- Smooth transitions (optional: fade animation)

### **4. Error Handling & UX**
#### Robust Error Handling
- API errors: Fallback to other LLM or retry
- Network timeout: User-friendly error message
- Invalid screenshots: Validation before API call
- Rate limiting: Intelligent backoff strategy

### **5. Performance Optimizations**
- **Caching**: Don't re-translate identical images
- **Lazy Loading**: Initialize LLM APIs only when needed
- **Background Processing**: Screenshots and API calls in separate threads
- **Memory Management**: Delete old screenshots after time or count

## Special Requirements for Chinese

### **Font & Rendering**
#### Chinese Character Support
- Font: "Microsoft YaHei", "SimHei", or system default
- Unicode: Full UTF-8 support
- Rendering: Anti-aliasing for better readability

### **OCR Optimization**
```python
# LLM Prompt Optimization for Chinese
CHINESE_OPTIMIZED_PROMPT = """
Specifically for Chinese text:
- Detect both simplified and traditional characters
- Consider context for ambiguous characters
- Translate idiomatic expressions contextually
- For technical terms: also provide English equivalent
"""
```

## Cross-Platform Compatibility

### **Windows Optimizations**
#### Windows-Specific Features
- DPI awareness for HiDPI displays
- Windows-native transparency APIs
- Taskbar integration optional

### **Linux/macOS Adaptations**
#### Platform-Specific Adjustments
- X11/Wayland compatibility for Linux
- macOS: Cocoa integration for native overlays
- Cursor handling per platform

## Deployment & Distribution

### **PyInstaller Setup**
```bash
# Build command for standalone executable
pyinstaller --onefile --windowed \
  --add-data "config;config" \
  --add-data "assets;assets" \
  --icon="assets/icons/app.ico" \
  --name="TranslationOverlay" \
  main.py
```

### **First-Run Setup**
#### Initial Setup Wizard
1. Enter API keys (Gemini/OpenAI)
2. Select default LLM
3. Configure hotkeys
4. Quick tutorial for usage

## Testing & Quality Assurance

### **Test Cases**
#### Critical Test Scenarios
- Screenshot different screen regions
- API failures and timeouts
- Very large/small overlay windows
- Rapid successive screenshots
- Chinese character rendering
- Tab switching under various conditions

**Additional References:**
- GitHub: https://github.com/thiswillbeyourgithub/OverText
- Follow proven patterns for transparent overlays

**Goal:** A user-friendly, performant tool for live translation with focus on Chinese texts and seamless desktop integration.
