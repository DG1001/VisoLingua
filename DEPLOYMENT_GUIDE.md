# VisoLingua Deployment Guide

## 📦 Answer to Your Question: Config File

### ✅ **NEW: Automatic config.ini Creation**

After the update, VisoLingua automatically creates a `config.ini` **next to the EXE file** if none exists.

### 🎯 **Two Deployment Options:**

## Option 1: EXE Only (Minimalist)
```
# Simply copy:
VisoLingua.exe

# What happens:
# ✅ On first start, config.ini is automatically created
# ✅ Works immediately (with default settings)
# ⚠️  User must enter API keys in Settings
```

## Option 2: Portable Package (Recommended)
```batch
# Create complete package:
create_portable.bat

# Result: VisoLingua-Portable/ folder with:
# ✅ VisoLingua.exe
# ✅ config.ini (pre-configured)
# ✅ Start VisoLingua.bat (Launcher)
# ✅ Create Desktop Shortcut.bat
# ✅ PORTABLE_README.txt
# ✅ Documentation
```

## 🔧 **Technical Details:**

### Config Location:
- **As EXE**: `config.ini` in same folder as `VisoLingua.exe`
- **As Python**: `config/config.ini` (as before)

### First Use:
1. **Start EXE** → `config.ini` is automatically created
2. **Open Settings** → Enter API keys
3. **Done!** → App is configured

## 🚀 **Recommended Workflow:**

### For You (Developer):
```batch
# 1. Build new EXE with config fix
python build_exe.py

# 2. Create portable package
create_portable.bat

# 3. Test
cd VisoLingua-Portable
"Start VisoLingua.bat"
```

### For End Users:
```batch
# Option A: EXE only
VisoLingua.exe  # → config.ini is automatically created

# Option B: Portable package (recommended)
"Start VisoLingua.bat"  # → Everything prepared
```

## 📋 **Deployment Scenarios:**

### 🎯 **Scenario 1: Simple Distribution**
**What to share**: Only `VisoLingua.exe`
- ✅ **Advantage**: Single file
- ✅ **Config**: Automatically created
- ⚠️  **Setup**: User must enter API keys themselves

### 🎯 **Scenario 2: User-Friendly**
**What to share**: Entire `VisoLingua-Portable/` folder
- ✅ **Advantage**: Ready to start immediately
- ✅ **Launcher**: "Start VisoLingua.bat"
- ✅ **Instructions**: PORTABLE_README.txt
- ✅ **Shortcuts**: Desktop icon creator

### 🎯 **Scenario 3: With Pre-configured API Keys**
```batch
# 1. Create portable package
create_portable.bat

# 2. Edit config.ini (enter API keys)
notepad VisoLingua-Portable\config.ini

# 3. Distribute → Ready to use immediately!
```

## 🛠️ **After the Update:**

You must **rebuild the EXE** for the config changes to take effect:

```batch
# Important: Rebuild EXE for config fix!
python build_exe.py

# Then create portable package
create_portable.bat
```

## 💡 **Answer to Your Question:**

> **"Will an ini be created automatically?"**

**✅ YES!** After the update:
- Place EXE anywhere → `config.ini` is automatically created next to the EXE on first start
- **OR** use the portable package → `config.ini` is already included

**Recommendation**: Use portable package for best user experience! 🎉
