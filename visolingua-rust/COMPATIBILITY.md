# VisoLingua - Linux Compatibility Guide

## The Issue

The current build uses **Tauri v2** which requires `webkit2gtk-4.1`, only available on:
- Ubuntu 22.04+
- Debian 12+
- Recent Fedora/Arch

Your system (Ubuntu 20.04) has `webkit2gtk-4.0`, which is incompatible.

## Solutions

### Option 1: Upgrade System (Recommended)
```bash
# Upgrade to Ubuntu 22.04 or later
sudo do-release-upgrade
```

### Option 2: Build Tauri v1 Version (Compatible with Ubuntu 20.04)

I can create a Tauri v1 branch that uses webkit2gtk-4.0. However, this requires:
- Downgrading Tauri dependencies
- Adjusting some API calls
- Rebuilding (~5 minutes)

**Would you like me to create this version?**

### Option 3: Install webkit2gtk-4.1 on Ubuntu 20.04 (Advanced)

Add Ubuntu 22.04 repository (risky, may break dependencies):
```bash
# NOT RECOMMENDED - may cause system instability
sudo add-apt-repository ppa:webkit-team/ppa
sudo apt-get update
sudo apt-get install libwebkit2gtk-4.1-0
```

### Option 4: Use Docker Container

Run the app in a container with newer Ubuntu:
```bash
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/app \
  ubuntu:22.04 \
  /app/visolingua
```

### Option 5: Run Python Version Instead

Since your system is Ubuntu 20.04, the Python version will work perfectly:
```bash
cd /workspace  # (the original Python version)
pip3 install -r requirements.txt
python3 main.py
```

---

## Checking Your System

```bash
# Check Ubuntu version
lsb_release -a

# Check available webkit versions
apt-cache search libwebkit2gtk

# Check what the binary needs
ldd /path/to/visolingua | grep webkit
```

---

## Recommended Path Forward

**For production use on Ubuntu 20.04:**
1. **Upgrade to Ubuntu 22.04** (cleanest solution)
2. **Use Python version** (works now, no compatibility issues)
3. **Wait for Tauri v1 build** (I can create this if needed)

Let me know which option you'd prefer!