#!/usr/bin/env python3
"""
PyInstaller build script for VisoLingua Windows executable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    # Directories to clean
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed: {dir_name}")
    
    # Remove spec file
    spec_file = 'VisoLingua.spec'
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   Removed: {spec_file}")

def check_dependencies():
    """Check if PyInstaller is installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import PyInstaller
        print(f"   ✅ PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("   ❌ PyInstaller not found!")
        print("   Install with: pip install pyinstaller")
        return False

def build_executable():
    """Build the Windows executable"""
    print("🔨 Building VisoLingua.exe...")
    
    # Check if icon exists
    icon_path = "assets/icons/app.ico"
    if not os.path.exists(icon_path):
        print(f"   ⚠️  Icon not found: {icon_path}")
        print("   Creating icon first...")
        try:
            subprocess.run([sys.executable, "create_icon.py"], check=True)
        except:
            print("   ❌ Failed to create icon, continuing without...")
            icon_path = None
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single executable file
        '--windowed',                   # No console window
        '--name=VisoLingua',            # Output name
        '--add-data=config;config',     # Include config directory  
        '--add-data=assets;assets',     # Include assets directory
        '--hidden-import=PIL._tkinter_finder',  # Fix tkinter issues
        '--hidden-import=PIL.ImageTk',  # Fix PIL issues
        '--hidden-import=mss',          # Ensure mss is included
        '--hidden-import=aiohttp',      # Ensure aiohttp is included
        '--hidden-import=pyperclip',    # Ensure pyperclip is included
        '--hidden-import=tkinter',      # Ensure tkinter is included
        '--collect-all=PIL',            # Include all PIL modules
        '--noconfirm',                  # Don't ask for confirmation
        'main.py'                       # Entry point
    ]
    
    # Add icon if available
    if icon_path and os.path.exists(icon_path):
        cmd.insert(4, f'--icon={icon_path}')  # Add after --name
        print(f"   Using icon: {icon_path}")
    else:
        print("   Building without icon")
    
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Build successful!")
            return True
        else:
            print("   ❌ Build failed!")
            print("   STDOUT:", result.stdout)
            print("   STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"   ❌ Build error: {e}")
        return False

def verify_build():
    """Verify the built executable"""
    print("🔍 Verifying build...")
    
    exe_path = Path('dist/VisoLingua.exe')
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ VisoLingua.exe created successfully!")
        print(f"   📁 Location: {exe_path.absolute()}")
        print(f"   📏 Size: {size_mb:.1f} MB")
        
        # Test if executable runs (quick check)
        try:
            result = subprocess.run([str(exe_path), '--help'], 
                                  capture_output=True, text=True, timeout=10)
            if 'VisoLingua' in result.stdout:
                print("   ✅ Executable runs correctly!")
            else:
                print("   ⚠️  Executable runs but output unexpected")
        except subprocess.TimeoutExpired:
            print("   ⚠️  Executable test timed out (GUI app)")
        except Exception as e:
            print(f"   ⚠️  Could not test executable: {e}")
        
        return True
    else:
        print("   ❌ VisoLingua.exe not found!")
        return False

def create_launcher_script():
    """Create a simple launcher script"""
    print("🚀 Creating launcher script...")
    
    launcher_content = '''@echo off
REM VisoLingua Launcher
REM This script starts VisoLingua and handles errors gracefully

echo Starting VisoLingua...
echo.

REM Check if executable exists
if not exist "VisoLingua.exe" (
    echo ERROR: VisoLingua.exe not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Start the application
start "" "VisoLingua.exe"

REM Optional: Wait a moment and check if it's still running
timeout /t 3 /nobreak >nul
tasklist /fi "imagename eq VisoLingua.exe" | find /i "VisoLingua.exe" >nul
if %errorlevel% equ 0 (
    echo VisoLingua started successfully!
) else (
    echo WARNING: VisoLingua may have failed to start.
    echo Check for error messages or missing dependencies.
    pause
)
'''
    
    with open('dist/Start_VisoLingua.bat', 'w') as f:
        f.write(launcher_content)
    
    print("   ✅ Launcher script created: dist/Start_VisoLingua.bat")

def main():
    """Main build process"""
    print("=" * 60)
    print("🏗️  VisoLingua Windows Executable Builder")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ Error: main.py not found!")
        print("   Please run this script from the VisoLingua directory.")
        sys.exit(1)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Clean previous builds
    clean_build()
    
    # Step 3: Build executable
    if not build_executable():
        print("\n❌ Build failed!")
        sys.exit(1)
    
    # Step 4: Verify build
    if not verify_build():
        print("\n❌ Build verification failed!")
        sys.exit(1)
    
    # Step 5: Create launcher
    create_launcher_script()
    
    print("\n" + "=" * 60)
    print("🎉 BUILD SUCCESSFUL!")
    print("=" * 60)
    print("📁 Your executable is ready:")
    print(f"   📂 Location: {Path('dist').absolute()}")
    print("   📄 Files created:")
    print("     • VisoLingua.exe (Main application)")
    print("     • Start_VisoLingua.bat (Launcher script)")
    print()
    print("🚀 To run:")
    print("   • Double-click VisoLingua.exe")
    print("   • Or use Start_VisoLingua.bat for better error handling")
    print()
    print("💡 Next steps:")
    print("   • Test the executable on different Windows machines")
    print("   • Create shortcuts for desktop/start menu")
    print("   • Consider creating an installer for easier distribution")

if __name__ == '__main__':
    main()