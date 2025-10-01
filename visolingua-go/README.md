# VisoLingua Go - Native Translation Overlay

Go + Wails implementation of VisoLingua for native cross-platform apps.

## Why Go + Wails?

- **Simple syntax** - Easiest migration from Python
- **Single binary** - No runtime dependencies
- **Fast compilation** - Builds in ~30 seconds
- **Web UI** - HTML/CSS/JS for interface (like Tauri)
- **Good size** - ~10-15 MB (smaller than Python, larger than Rust)

## Prerequisites

- [Go](https://go.dev/dl/) 1.21+
- [Wails](https://wails.io/) v2.8+
- Platform dependencies:
  - **Windows**: WebView2 (usually pre-installed on Windows 11)
  - **macOS**: Xcode Command Line Tools
  - **Linux**: `webkit2gtk-4.0`

## Installation

### 1. Install Go

```bash
# Download from https://go.dev/dl/
# Or use package manager:

# macOS
brew install go

# Linux (Ubuntu/Debian)
sudo apt-get install golang-go

# Windows
winget install GoLang.Go
```

### 2. Install Wails CLI

```bash
go install github.com/wailsapp/wails/v2/cmd/wails@latest
```

### 3. Install Platform Dependencies

**Linux:**
```bash
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev
```

**macOS:**
```bash
xcode-select --install
```

**Windows:**
- WebView2 pre-installed on Windows 11
- Download for Windows 10: https://go.microsoft.com/fwlink/p/?LinkId=2124703

## Build

### Development Mode:
```bash
cd visolingua-go
wails dev
```

### Production Build:
```bash
wails build
```

**Output:**
- **Linux**: `build/bin/visolingua` (~12-15 MB)
- **Windows**: `build/bin/visolingua.exe` (~10-12 MB)
- **macOS**: `build/bin/VisoLingua.app` (~12-15 MB)

## Configuration

Same as other versions - config file at:
- **Windows**: `%APPDATA%\visolingua\config.toml`
- **macOS**: `~/Library/Application Support/visolingua/config.toml`
- **Linux**: `~/.config/visolingua/config.toml`

## Features

- ✅ **Control panel window** - Small always-on-top window
- ✅ **Manual coordinate capture** - Enter X, Y, Width, Height or capture center
- ✅ **LLM integration** - Supports Gemini, OpenAI, Ollama
- ✅ **Ask AI feature** - Ask questions about translations
- ✅ **Small binary** - Only ~12MB
- ✅ **Cross-platform** - Windows, macOS, Linux

## How to Use

### Method 1: Capture Center of Screen
1. Position text in the center of your screen
2. Click "Capture Area" button
3. It captures 800x600 from screen center

### Method 2: Custom Coordinates
1. Find the screen coordinates of your text area
   - Use Windows Snipping Tool or similar to find X, Y position
2. Enter X, Y, Width, Height in the input fields
3. Click "Capture Custom"

**Note:** Unlike the Rust version, this uses a control panel approach instead of a transparent overlay. The Go version captures specific screen coordinates rather than "what's under the window".

## Size Comparison

| Version | Binary Size | Startup Time |
|---------|-------------|--------------|
| **Python** | ~50 MB | ~2-3s |
| **Rust** | ~8 MB | ~0.5s |
| **Go** | **~12 MB** | **~1s** |

**Go is the middle ground** - easier to develop than Rust, much smaller than Python!

## Advantages of Go Version

### vs Python:
- ✅ **75% smaller** (~12 MB vs ~50 MB)
- ✅ **No Python runtime needed**
- ✅ **Faster startup** (1s vs 2-3s)
- ✅ **No antivirus false positives**

### vs Rust:
- ✅ **Easier syntax** (more Python-like)
- ✅ **Faster builds** (30s vs 5 min)
- ✅ **Simpler error handling**
- ❌ Slightly larger binaries

## Project Structure

```
visolingua-go/
├── main.go              # Entry point
├── app.go               # Main app logic
├── config.go            # Configuration management
├── translator.go        # LLM integration
├── go.mod               # Go dependencies
├── frontend/
│   └── dist/
│       └── index.html   # UI (overlay + result)
└── build/
    └── bin/             # Compiled binaries
```

## Development

```bash
# Run in dev mode with hot reload
wails dev

# Build for current platform
wails build

# Build for specific platform
wails build -platform windows/amd64
wails build -platform darwin/universal
wails build -platform linux/amd64
```

## Troubleshooting

### "wails: command not found"
```bash
# Add Go bin to PATH
export PATH=$PATH:$(go env GOPATH)/bin

# Or add permanently to ~/.bashrc or ~/.zshrc
```

### Build fails on Linux
```bash
# Install required dependencies
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev gcc pkg-config
```

### WebView2 error on Windows
Download and install: https://go.microsoft.com/fwlink/p/?LinkId=2124703

## Why Choose Go?

**Choose Go if:**
- ✅ You prefer Go's simple syntax over Rust
- ✅ You want faster build times
- ✅ Binary size of 12 MB is acceptable
- ✅ You're comfortable with ~1s startup time

**Choose Rust if:**
- You need the absolute smallest binary (~8 MB)
- You need the fastest startup (~0.5s)
- You're okay with longer build times

**Choose Python if:**
- You need to iterate quickly
- Binary size doesn't matter
- You don't want to learn Go/Rust

All three versions have **identical features**!