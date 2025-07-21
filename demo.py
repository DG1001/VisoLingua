#!/usr/bin/env python3
"""
Demo script to test VisoLingua fixes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_screenshot_fixes():
    """Test screenshot functionality with fixes"""
    print("Testing screenshot fixes...")
    
    try:
        from core.screenshot import ScreenCapture
        capture = ScreenCapture()
        
        # Test screen info
        screen_info = capture.get_screen_info()
        print(f"✅ Screen info: {screen_info['monitors'][0] if screen_info['monitors'] else 'None'}")
        
        # Test screenshot capture (with fallback)
        bbox = (0, 0, 200, 100)  # Small test area
        img = capture.capture_area(bbox)
        print(f"✅ Screenshot captured: {img.size}, mode: {img.mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Screenshot test failed: {e}")
        return False

def test_transparency_settings():
    """Test transparency settings"""
    print("Testing transparency settings...")
    
    try:
        from config.settings import Settings
        settings = Settings()
        
        transparency = settings.getfloat('ui', 'overlay_transparency', 0.05)
        print(f"✅ Transparency setting: {transparency} (should be 0.7 or higher)")
        
        if transparency >= 0.3:
            print("✅ Transparency is visible enough")
            return True
        else:
            print("⚠️  Transparency might be too low")
            return False
            
    except Exception as e:
        print(f"❌ Transparency test failed: {e}")
        return False

def test_ui_creation():
    """Test UI creation without display errors"""
    print("Testing UI components...")
    
    try:
        import tkinter as tk
        from config.settings import Settings
        from utils.helpers import get_safe_cursor
        
        # Test cursor safety
        cursor = get_safe_cursor('sizing', 'hand2')
        print(f"✅ Safe cursor found: {cursor}")
        
        # Test basic UI creation (without showing)
        root = tk.Tk()
        root.withdraw()  # Don't show
        
        # Test transparency
        settings = Settings()
        transparency = settings.getfloat('ui', 'overlay_transparency', 0.7)
        
        test_window = tk.Toplevel(root)
        test_window.withdraw()
        test_window.attributes('-alpha', transparency)
        
        print(f"✅ UI components work with transparency: {transparency}")
        
        test_window.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        return False

def main():
    """Run all demo tests"""
    print("VisoLingua Fix Demo")
    print("=" * 40)
    
    tests = [
        test_transparency_settings,
        test_screenshot_fixes,
        test_ui_creation
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Demo tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All fixes working! App should start correctly now.")
        print("\n💡 Key fixes applied:")
        print("   • Transparency increased from 0.05 to 0.7 (window now visible)")
        print("   • MSS threading issues fixed with thread-local storage")
        print("   • Fallback screenshot methods added (PIL ImageGrab)")
        print("   • Safe cursor detection implemented")
        print("\n🚀 Try: python main.py")
    else:
        print("⚠️  Some issues remain. Check output above.")

if __name__ == "__main__":
    main()