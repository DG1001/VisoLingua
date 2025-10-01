# VisoLingua Windows Installation Guide

VisoLingua can be installed as a real Windows app in various ways. Here are all available options:

## 🚀 Option 1: Standalone EXE (Recommended)

### Step 1: Create EXE
```batch
# Easiest method - everything automatic
build.bat

# Or manually
python build_exe.py
```

**Result**: `dist/VisoLingua.exe` (~50-100MB) - Single file, works on any Windows PC

### Step 2: Create Desktop Icon (Optional)
```batch
# Change to dist/ folder
cd dist

# Create desktop shortcut
..\create_shortcut.bat
```

## 🏗️ Option 2: Full Windows Installation

### Automatic Installation with Admin Rights
```batch
# 1. Create EXE (if not already done)
build.bat

# 2. Change to dist/ folder
cd dist

# 3. Run as Administrator
..\install_windows.bat
```

**What happens:**
- ✅ Installation to `C:\Program Files\VisoLingua\`
- ✅ Desktop shortcut
- ✅ Start Menu entry
- ✅ Windows "Add/Remove Programs" integration
- ✅ Automatic uninstaller

## 🎯 Option 3: Professional Installer (Advanced)

### Prerequisites
1. Install [NSIS](https://nsis.sourceforge.io/)
2. Add NSIS to Windows PATH

### Create Installer
```batch
# 1. Create EXE
build.bat

# 2. Create professional installer
build_installer.bat
```

**Result**: `VisoLingua-Setup-1.0.0.exe` - Professional installer with wizard

## 📋 Available Files

After building, you'll find the following files:

```
VisoLingua/
├── build.bat                    # Create EXE
├── build_exe.py                 # Python build script
├── create_shortcut.bat          # Create desktop icon
├── install_windows.bat          # Full installation
├── installer.nsi               # NSIS installer configuration
├── build_installer.bat         # Create professional installer
├── assets/icons/app.ico        # Windows app icon
└── dist/
    ├── VisoLingua.exe          # Standalone application
    └── Start_VisoLingua.bat    # Launcher with error detection
```

## 🎮 Usage

### Simple (Option 1)
1. Run `build.bat`
2. Double-click `dist/VisoLingua.exe`
3. Done! 🎉

### With Desktop Icon
1. Above steps + `create_shortcut.bat`
2. Double-click VisoLingua icon on desktop

### Full Installation (Option 2)
1. `build.bat` → `cd dist` → `install_windows.bat` (as Admin)
2. Start VisoLingua via Start Menu or Desktop

### Professional Installer (Option 3)
1. Run `build_installer.bat`
2. Share `VisoLingua-Setup-1.0.0.exe` with others
3. Recipients run setup → Automatic installation

## 🔧 Advanced Features

### Autostart with Windows (Option 3)
The professional installer offers option for automatic start with Windows.

### System Tray Integration
Planned for future versions - VisoLingua minimizes to taskbar.

### Global Hotkeys
Planned - call VisoLingua from anywhere via keyboard shortcuts.

## 🛠️ Troubleshooting

### "Python not found"
- Install Python 3.8+ and add to PATH

### "PyInstaller not found"
```batch
pip install pyinstaller
```

### "makensis not found"
- Install [NSIS](https://nsis.sourceforge.io/)
- Or use Option 1/2 (no NSIS needed)

### EXE doesn't start
- Disable Windows Defender/Antivirus (false positive)
- Use `Start_VisoLingua.bat` for better error messages

### Admin rights required
- Right-click on batch file → "Run as Administrator"

## 📦 Distribution

### For End Users
- **Simple**: `VisoLingua.exe` + `create_shortcut.bat`
- **Professional**: `VisoLingua-Setup-1.0.0.exe`

### For Developers
- Complete repository with all build scripts

## 🎯 Recommended Workflow

1. **Development**: Use Python version
2. **Testing**: `build.bat` → test EXE
3. **Distribution**: `build_installer.bat` → distribute Setup.exe
4. **End Users**: Run Setup.exe → Installed and ready

## 💡 Next Steps

After successful installation:
1. Configure API keys in Settings
2. Read README.md for usage instructions
3. Read SETUP.md for detailed configuration

VisoLingua is now a real Windows app! 🎉
