#!/usr/bin/env python3
"""
Simple test script for VisoLingua components
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test if all modules can be imported"""
    try:
        from config.settings import Settings
        from core.screenshot import ScreenCapture
        from core.translator import Translator
        from ui.overlay import OverlayWindow
        from ui.result_window import ResultWindow
        from utils.constants import APP_NAME
        from utils.helpers import format_file_size
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_settings():
    """Test settings loading"""
    try:
        from config.settings import Settings
        settings = Settings()
        print(f"✅ Settings loaded: {settings.get('api', 'default_llm')}")
        return True
    except Exception as e:
        print(f"❌ Settings error: {e}")
        return False

def test_screenshot():
    """Test screenshot capture"""
    try:
        from core.screenshot import ScreenCapture
        capture = ScreenCapture()
        screen_info = capture.get_screen_info()
        print(f"✅ Screenshot module working: {len(screen_info['monitors'])} monitors detected")
        return True
    except Exception as e:
        print(f"❌ Screenshot error: {e}")
        return False

def test_utilities():
    """Test utility functions"""
    try:
        from utils.helpers import format_file_size, safe_int
        from utils.constants import APP_NAME
        
        assert format_file_size(1024) == "1.0KB"
        assert safe_int("123") == 123
        assert APP_NAME == "VisoLingua"
        print("✅ Utilities working correctly")
        return True
    except Exception as e:
        print(f"❌ Utilities error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing VisoLingua components...")
    print("-" * 40)
    
    tests = [
        test_imports,
        test_settings,
        test_screenshot,
        test_utilities
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("-" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! VisoLingua is ready to use.")
        print("\nTo start the app: python main.py")
        print("Don't forget to configure API keys in settings!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()