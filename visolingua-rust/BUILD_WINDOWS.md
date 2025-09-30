# Building VisoLingua for Windows

## Why Cross-Compilation from Linux Doesn't Work

Cross-compiling Tauri apps from Linux to Windows is **not supported** because:

1. **WebView2 Runtime**: Windows builds require Microsoft Edge WebView2, which has no Linux equivalent
2. **Platform-Specific APIs**: Tauri uses completely different UI frameworks:
   - Linux: GTK3/webkit2gtk
   - Windows: Win32 API + WebView2
3. **Build System**: Tauri's Windows bundler requires Windows-native tools (NSIS, WiX)

## Solution: Build on Windows

You have **3 options** to build the Windows binary:

---

## Option 1: Build on Windows Machine (Recommended)

### Prerequisites

1. **Install Rust**
   ```powershell
   # Download from https://rustup.rs/ or use winget:
   winget install Rustlang.Rustup
   ```

2. **Install Node.js**
   ```powershell
   winget install OpenJS.NodeJS
   ```

3. **Install WebView2** (usually pre-installed on Windows 11)
   - Download: https://go.microsoft.com/fwlink/p/?LinkId=2124703

### Build Steps

```powershell
# Clone or copy the project to Windows
cd path\to\visolingua-rust

# Install npm dependencies
npm install

# Build for Windows
npm run tauri build

# Binary will be at:
# src-tauri\target\release\visolingua.exe
# Installer at:
# src-tauri\target\release\bundle\msi\VisoLingua_1.0.0_x64_en-US.msi
```

**Expected output:**
- `visolingua.exe` (~6-8 MB)
- MSI installer (~8-10 MB)

---

## Option 2: GitHub Actions (Automated)

Create `.github/workflows/build.yml`:

```yaml
name: Build Windows Binary

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Setup Rust
        uses: dtolnay/rust-toolchain@stable

      - name: Install dependencies
        run: npm install
        working-directory: ./visolingua-rust

      - name: Build Tauri app
        run: npm run tauri build
        working-directory: ./visolingua-rust

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: visolingua-windows
          path: |
            visolingua-rust/src-tauri/target/release/visolingua.exe
            visolingua-rust/src-tauri/target/release/bundle/msi/*.msi
```

After pushing this, GitHub will automatically build Windows binaries for you!

---

## Option 3: Use Windows VM or WSL with Windows Host

### On WSL (if you have Windows host):

Since you're already on WSL2, you can access Windows from within WSL:

```bash
# From WSL, call Windows tools directly
cd /mnt/c/path/to/visolingua-rust

# Install via Windows PowerShell (from WSL):
powershell.exe -Command "winget install Rustlang.Rustup"
powershell.exe -Command "winget install OpenJS.NodeJS"

# Build using Windows tools:
cmd.exe /c "npm install && npm run tauri build"
```

---

## Expected Windows Build Results

After successful build on Windows:

```
src-tauri/target/release/
├── visolingua.exe          # ~6-8 MB (main executable)
├── bundle/
│   └── msi/
│       └── VisoLingua_1.0.0_x64_en-US.msi  # ~8-10 MB (installer)
```

### Binary Comparison

| Platform | Binary Size | Installer Size |
|----------|-------------|----------------|
| **Windows** | 6-8 MB | 8-10 MB (MSI) |
| **Linux** | 9 MB | - |
| **Python (PyInstaller)** | ~50 MB | ~50 MB |

All native builds are **80-85% smaller** than Python version!

---

## Troubleshooting Windows Build

### "WebView2 not found"
```powershell
# Install WebView2 Runtime:
winget install Microsoft.EdgeWebView2Runtime
```

### "MSVC not found"
```powershell
# Install Visual Studio Build Tools:
winget install Microsoft.VisualStudio.2022.BuildTools --override "--add Microsoft.VisualStudio.Workload.VCTools"
```

### Build takes too long
- First build: 5-10 minutes (downloads dependencies)
- Subsequent builds: 2-3 minutes

---

## Why This Approach is Best

1. ✅ **Native Windows binary** with optimal performance
2. ✅ **Proper WebView2 integration** (uses system Edge)
3. ✅ **MSI installer** for professional deployment
4. ✅ **Code signing** support (can add in Tauri config)
5. ✅ **No antivirus false positives** (native compilation)

---

## Alternative: Docker with Wine (Not Recommended)

While theoretically possible to use Wine in Docker for cross-compilation, it's:
- ❌ Extremely unreliable
- ❌ Produces buggy binaries
- ❌ Doesn't support WebView2
- ❌ Not officially supported by Tauri

**Stick with Options 1-3 above for production-quality builds.**

---

## I Can Help With:

If you have access to a Windows machine, I can:
1. Create automated build scripts
2. Set up GitHub Actions for continuous builds
3. Configure code signing
4. Create custom installers (NSIS/WiX)

Just run the project on Windows and the build will work perfectly!