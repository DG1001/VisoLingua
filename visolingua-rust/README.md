# VisoLingua Rust - Native Translation Overlay

Rust + Tauri port of VisoLingua for native Windows/Mac/Linux apps.

## Prerequisites

- [Rust](https://rustup.rs/) 1.70+
- [Node.js](https://nodejs.org/) 18+ (for frontend build)
- Platform-specific dependencies:
  - **Windows**: WebView2 (usually pre-installed on Windows 11)
  - **macOS**: Xcode Command Line Tools
  - **Linux**: `webkit2gtk`, `libayatana-appindicator3-dev`

## Quick Start

```bash
# Install dependencies
npm install

# Run in development mode
npm run tauri dev

# Build for production
npm run tauri build
```

## Project Structure

```
visolingua-rust/
├── src/               # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── overlay.html   # Transparent capture overlay
│   ├── result.html    # Translation result window
│   └── styles.css
├── src-tauri/         # Rust backend
│   ├── src/
│   │   ├── main.rs    # Entry point
│   │   ├── screenshot.rs
│   │   ├── translator.rs
│   │   └── config.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
└── package.json
```

## Features

- ✅ Transparent overlay window
- ✅ Screenshot capture
- ✅ LLM integration (Gemini, OpenAI, Ollama)
- ✅ Multi-window support (overlay + result)
- ✅ Native performance (~3-5MB binary)
- ✅ No antivirus false positives
- ✅ Cross-platform (Windows, macOS, Linux)

## Configuration

Edit `src-tauri/config.toml` or use the Settings UI to configure API keys.