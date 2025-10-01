# VisoLingua Rust - Native Translation Overlay

Rust + Tauri version of VisoLingua with transparent overlay for Windows/Mac/Linux.

## Features

- ✅ **Transparent red overlay window** - Position over text and click to capture
- ✅ **Multi-monitor support** - Works correctly with multiple displays
- ✅ **Screenshot capture** - Captures exactly what's under the window
- ✅ **LLM integration** - Supports Gemini, OpenAI, and Ollama
- ✅ **Ask AI feature** - Ask questions about the translation
- ✅ **Small binary** - Only ~8-10MB (vs 50MB Python version)
- ✅ **No antivirus issues** - Native compilation, no false positives
- ✅ **Cross-platform** - Windows, macOS, Linux

## How to Use

1. **Configure API Key**
   - Edit `%APPDATA%\visolingua\config.toml` (Windows)
   - Or `~/.config/visolingua/config.toml` (Linux/Mac)
   - Add your Gemini or OpenAI API key

2. **Position the Overlay**
   - Move and resize the red transparent window
   - Position it over the text you want to translate

3. **Capture & Translate**
   - Click anywhere inside the red overlay
   - Wait for translation to appear
   - Use "Ask AI" to ask questions about the translation

## Configuration

Config file location:
- **Windows**: `%APPDATA%\visolingua\config.toml`
- **Linux/Mac**: `~/.config/visolingua/config.toml`

Example:
```toml
[llm]
provider = "gemini"
gemini_model = "gemini-2.0-flash-exp"

[api_keys]
gemini = "your-api-key-here"

[translation]
target_language = "German"
```

Get API keys:
- **Gemini** (Free): https://aistudio.google.com/
- **OpenAI** (Paid): https://platform.openai.com/

## Building from Source

### Prerequisites

- [Rust](https://rustup.rs/) 1.70+
- [Node.js](https://nodejs.org/) 18+
- Platform-specific:
  - **Windows**: WebView2 (pre-installed on Win 11)
  - **macOS**: Xcode Command Line Tools
  - **Linux**: `webkit2gtk-4.1`, `libayatana-appindicator3-dev`

### Build

```bash
npm install
npm run tauri build
```

Binary will be in `src-tauri/target/release/`

## Multi-Monitor Notes

The app automatically detects which monitor contains the window and captures from the correct screen. If you have multiple monitors, just position the overlay on any screen and it will work correctly.