# VisoLingua Rust - Setup Guide

## Prerequisites Installation

### 1. Install Rust

**Windows:**
```powershell
# Download and run rustup-init.exe from https://rustup.rs/
# Or use winget:
winget install Rustlang.Rustup
```

**macOS:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**Linux:**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install additional dependencies for Tauri
# Ubuntu/Debian:
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev \
  build-essential \
  curl \
  wget \
  file \
  libssl-dev \
  libayatana-appindicator3-dev \
  librsvg2-dev

# Fedora:
sudo dnf install webkit2gtk4.1-devel \
  openssl-devel \
  curl \
  wget \
  file \
  libappindicator-gtk3-devel \
  librsvg2-devel

# Arch:
sudo pacman -S webkit2gtk base-devel curl wget file openssl appmenu-gtk-module gtk3 libappindicator-gtk3 librsvg
```

### 2. Install Node.js

**All platforms:**
Download from https://nodejs.org/ (v18 or higher)

Or use package managers:
```bash
# Windows (winget):
winget install OpenJS.NodeJS

# macOS (homebrew):
brew install node

# Linux:
# Use your distribution's package manager
```

### 3. Platform-Specific Requirements

**Windows:**
- WebView2 Runtime (usually pre-installed on Windows 11)
- If needed: Download from https://developer.microsoft.com/microsoft-edge/webview2/

**macOS:**
```bash
xcode-select --install
```

**Linux:**
- Dependencies listed above in step 1

## Building and Running

### Development Mode

```bash
cd visolingua-rust

# Install npm dependencies
npm install

# Run in development mode (with hot reload)
npm run tauri dev
```

### Production Build

```bash
# Build optimized binary
npm run tauri build

# Outputs will be in:
# src-tauri/target/release/visolingua (executable)
# src-tauri/target/release/bundle/ (installers)
```

**Build artifacts:**
- **Windows**: `.exe` and `.msi` installer in `src-tauri/target/release/bundle/`
- **macOS**: `.app` bundle and `.dmg` in `src-tauri/target/release/bundle/`
- **Linux**: `.AppImage`, `.deb`, and `.rpm` in `src-tauri/target/release/bundle/`

## Configuration

### First Run

On first run, VisoLingua creates a config file at:
- **Windows**: `%APPDATA%\visolingua\config.toml`
- **macOS**: `~/Library/Application Support/visolingua/config.toml`
- **Linux**: `~/.config/visolingua/config.toml`

### Manual Configuration

Edit the config file directly:

```toml
[llm]
provider = "gemini"  # Options: "gemini", "openai", "ollama"
gemini_model = "gemini-2.0-flash-exp"
openai_model = "gpt-4o-mini"
ollama_url = "http://localhost:11434"
ollama_model = "llava"

[api_keys]
gemini = "your-gemini-api-key-here"
openai = "your-openai-api-key-here"

[translation]
target_language = "German"

[ui]
overlay_transparency = "0.3"
```

### Getting API Keys

**Gemini (Recommended):**
1. Visit https://aistudio.google.com/
2. Sign in with Google account
3. Click "Get API Key" → "Create API Key"
4. Copy the key to config.toml

**OpenAI:**
1. Visit https://platform.openai.com/
2. Sign up/login
3. Go to API Keys section
4. Create new secret key
5. Copy the key to config.toml

**Ollama (Local, Free):**
1. Install Ollama: https://ollama.ai/
2. Pull a vision model: `ollama pull llava`
3. Set provider to "ollama" in config
4. No API key needed!

## Usage

1. **Launch**: Run the application
2. **Position**: Drag the red overlay window over text to translate
3. **Capture**: Click inside the red area
4. **View**: Translation appears in result window
5. **Ask AI**: Type questions about the translation
6. **Return**: Click "Back to Capture" or press Escape

### Keyboard Shortcuts

- **Escape**: Close result window (return to capture)
- **Ctrl+C**: Copy translation (when focused in result window)

## Troubleshooting

### "Cargo command not found"
- Restart terminal after installing Rust
- Run `source $HOME/.cargo/env` (Linux/macOS)

### "WebView2 not found" (Windows)
- Install WebView2: https://go.microsoft.com/fwlink/p/?LinkId=2124703

### "Cannot capture screenshot"
- On Linux: May need to grant permission or disable Wayland restrictions
- Try running with: `GDK_BACKEND=x11 ./visolingua`

### "API request failed"
- Check API key in config file
- Verify internet connection
- Check API quota/billing

### Linux: Transparent window not working
- Requires compositor (GNOME, KDE with effects enabled)
- Try different window manager settings

## Performance Comparison

| Metric | Python Version | Rust Version |
|--------|---------------|--------------|
| Binary Size | ~50MB (with PyInstaller) | ~3-5MB |
| Startup Time | ~2-3s | ~0.5s |
| Memory Usage | ~100-150MB | ~20-40MB |
| False Positives | Common | Rare |
| Build Time | Fast | Moderate |

## Next Steps

- Configure your preferred LLM provider in settings
- Adjust overlay transparency if needed
- Set up Ollama for completely private translation
- Report issues at: https://github.com/[your-repo]/issues

## Development

### Project Structure

```
src-tauri/src/
├── main.rs          # Tauri commands, app entry
├── screenshot.rs    # Cross-platform screenshot capture
├── translator.rs    # LLM API integration
└── config.rs        # Configuration management

src/
├── overlay.html     # Transparent capture overlay UI
└── result.html      # Translation result window UI
```

### Adding New Features

1. **Backend (Rust)**: Add functions in `src-tauri/src/`
2. **Commands**: Expose with `#[tauri::command]` in `main.rs`
3. **Frontend**: Call via `invoke('command_name', { args })` in HTML/JS

### Testing

```bash
# Run Rust tests
cd src-tauri
cargo test

# Run in debug mode
npm run tauri dev
```