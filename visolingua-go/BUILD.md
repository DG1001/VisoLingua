# Building VisoLingua Go

## Quick Start

```bash
# Install Wails CLI
go install github.com/wailsapp/wails/v2/cmd/wails@latest

# Build for your platform
cd visolingua-go
wails build
```

## Build for All Platforms

### From Linux (cross-compile):

```bash
# Windows
GOOS=windows GOARCH=amd64 wails build -platform windows/amd64

# macOS (requires macOS SDK)
# Cross-compilation to macOS requires additional setup

# Linux
wails build -platform linux/amd64
```

### From Windows:

```powershell
# Windows
wails build

# Linux (requires MinGW)
$Env:GOOS="linux"; $Env:GOARCH="amd64"; wails build
```

### From macOS:

```bash
# macOS Universal (Intel + Apple Silicon)
wails build -platform darwin/universal

# Windows
GOOS=windows GOARCH=amd64 wails build -platform windows/amd64

# Linux
GOOS=linux GOARCH=amd64 wails build -platform linux/amd64
```

## Build Output Locations

After running `wails build`:

```
build/bin/
├── visolingua           # Linux binary
├── visolingua.exe       # Windows binary
└── VisoLingua.app/      # macOS app bundle
```

## Expected Binary Sizes

| Platform | Size | With Compression |
|----------|------|------------------|
| Linux    | ~12-15 MB | ~8 MB |
| Windows  | ~10-12 MB | ~7 MB |
| macOS    | ~12-15 MB | ~8 MB |

## Build Flags

### Release Build (optimized):
```bash
wails build -clean -upx
```

Flags:
- `-clean`: Clean build directory first
- `-upx`: Compress binary with UPX (requires UPX installed)
- `-ldflags "-s -w"`: Strip debug info (smaller binary)

### Debug Build:
```bash
wails dev  # With hot reload
```

## Platform-Specific Notes

### Linux

**Required packages:**
```bash
sudo apt-get install libgtk-3-dev libwebkit2gtk-4.0-dev gcc pkg-config
```

**Binary works on:**
- Ubuntu 20.04+
- Debian 11+
- Fedora 35+
- Arch Linux

### Windows

**No additional dependencies** needed for building on Windows.

**Runtime requirement:** WebView2 (pre-installed on Windows 11)

### macOS

**Required:**
```bash
xcode-select --install
```

**Universal Binary:**
```bash
wails build -platform darwin/universal
```

Creates a single `.app` that works on both Intel and Apple Silicon Macs.

## Troubleshooting

### "wails: command not found"

Add Go bin to PATH:
```bash
export PATH=$PATH:$(go env GOPATH)/bin
```

### Linux: "Package webkit2gtk-4.0 was not found"

```bash
sudo apt-get install libwebkit2gtk-4.0-dev
```

### Windows: "gcc: command not found"

Install MinGW-w64 or use Windows native build (no gcc needed for Windows target).

### Build too slow?

Use incremental builds:
```bash
wails build -skipbindings  # Skip JS binding generation if unchanged
```

## Size Optimization

### 1. UPX Compression

```bash
# Install UPX
sudo apt-get install upx  # Linux
brew install upx          # macOS

# Build with compression
wails build -upx
```

**Result:** ~40-50% size reduction

### 2. Strip Debug Symbols

```bash
wails build -ldflags "-s -w"
```

### 3. Both Combined

```bash
wails build -clean -upx -ldflags "-s -w"
```

**Final size:** ~8 MB (comparable to Rust!)

## Comparison: Build Times

| Platform | First Build | Cached Build |
|----------|-------------|--------------|
| Linux    | ~45s        | ~15s         |
| Windows  | ~60s        | ~20s         |
| macOS    | ~50s        | ~18s         |

Much faster than Rust (5-10 minutes), slower than Python (~instant).