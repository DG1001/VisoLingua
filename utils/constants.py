"""
Application constants
"""

import sys
import platform

# Application Info
APP_NAME = "VisoLingua"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Live Translation Overlay Tool"
APP_AUTHOR = "VisoLingua Team"

# Window Constants
MIN_OVERLAY_WIDTH = 200
MIN_OVERLAY_HEIGHT = 200
MIN_RESULT_WIDTH = 400
MIN_RESULT_HEIGHT = 300

DEFAULT_OVERLAY_WIDTH = 400
DEFAULT_OVERLAY_HEIGHT = 300
DEFAULT_RESULT_WIDTH = 500
DEFAULT_RESULT_HEIGHT = 400

# UI Constants
OVERLAY_TRANSPARENCY = 0.05
BORDER_WIDTH = 2
BORDER_COLOR_ACTIVE = "#FF0000"
BORDER_COLOR_INACTIVE = "#808080"

# Font Settings
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_FONT_SIZE = 10
CHINESE_FONT_FAMILIES = ["Microsoft YaHei", "SimHei", "WenQuanYi Micro Hei", "Noto Sans CJK"]

# Translation Constants
MAX_TRANSLATION_LENGTH = 10000
MAX_HISTORY_ENTRIES = 100
CACHE_CLEANUP_THRESHOLD = 150

# API Constants
API_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 1  # seconds

# Image Processing
MAX_IMAGE_DIMENSION = 2048
JPEG_QUALITY = 85
PNG_COMPRESSION = 6

# Supported Languages
SUPPORTED_SOURCE_LANGUAGES = {
    'auto': 'Auto-detect',
    'zh': 'Chinese',
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'en': 'English',
    'ja': 'Japanese',
    'ko': 'Korean',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'th': 'Thai',
    'vi': 'Vietnamese'
}

SUPPORTED_TARGET_LANGUAGES = {
    'de': 'German',
    'en': 'English',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian'
}

# Platform Detection
IS_WINDOWS = platform.system() == 'Windows'
IS_LINUX = platform.system() == 'Linux'
IS_MAC = platform.system() == 'Darwin'

# File Paths
CONFIG_DIR = "config"
ASSETS_DIR = "assets"
ICONS_DIR = "assets/icons"
STYLES_DIR = "assets/styles"
CACHE_DIR = "cache"

# Error Messages
ERROR_MESSAGES = {
    'NO_API_KEY': "API key not configured. Please set your API key in settings.",
    'API_ERROR': "API request failed. Please check your internet connection and API key.",
    'SCREENSHOT_ERROR': "Failed to capture screenshot. Please try again.",
    'TRANSLATION_ERROR': "Translation failed. Please try again or check your settings.",
    'CONFIG_ERROR': "Configuration error. Please check your settings.",
    'NETWORK_ERROR': "Network error. Please check your internet connection.",
    'TIMEOUT_ERROR': "Request timed out. Please try again.",
    'INVALID_IMAGE': "Invalid image format. Please capture a new screenshot.",
    'RATE_LIMIT': "API rate limit exceeded. Please wait before trying again."
}

# Success Messages
SUCCESS_MESSAGES = {
    'TRANSLATION_COMPLETE': "Translation completed successfully",
    'COPIED_TO_CLIPBOARD': "Translation copied to clipboard",
    'SETTINGS_SAVED': "Settings saved successfully",
    'CACHE_CLEARED': "Cache cleared successfully"
}

# Hotkey Mappings
DEFAULT_HOTKEYS = {
    'toggle_mode': '<Control-Tab>',
    'capture_screenshot': '<Button-1>',
    'copy_result': '<Control-c>',
    'clear_result': '<Control-l>',
    'open_settings': '<Control-comma>',
    'quit_app': '<Control-q>'
}

# Color Schemes
COLOR_SCHEMES = {
    'default': {
        'primary': '#FF0000',
        'secondary': '#00FF00',
        'background': '#FFFFFF',
        'text': '#000000',
        'error': '#FF4444',
        'success': '#44FF44'
    },
    'dark': {
        'primary': '#FF6B6B',
        'secondary': '#4ECDC4',
        'background': '#2C3E50',
        'text': '#ECF0F1',
        'error': '#E74C3C',
        'success': '#2ECC71'
    }
}

# Development/Debug
DEBUG = False
VERBOSE_LOGGING = False
LOG_API_CALLS = False

# Performance Settings
SCREENSHOT_CACHE_SIZE = 50
TRANSLATION_CACHE_SIZE = 100
IMAGE_OPTIMIZATION_THREADS = 2
API_REQUEST_TIMEOUT = 30

# Validation Constants
MIN_VALID_IMAGE_SIZE = (10, 10)  # pixels
MAX_VALID_IMAGE_SIZE = (4096, 4096)  # pixels
MIN_BBOX_SIZE = (50, 50)  # pixels

# UI Styling
BUTTON_PADDING = (10, 5)
FRAME_PADDING = 10
WIDGET_SPACING = 5

# Animation Settings
FADE_DURATION = 200  # milliseconds
FLASH_DURATION = 300  # milliseconds
LOADING_ANIMATION_SPEED = 100  # milliseconds

def get_app_info():
    """Get formatted application information"""
    return f"{APP_NAME} v{APP_VERSION}"

def get_system_info():
    """Get system information for debugging"""
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'architecture': platform.architecture()[0]
    }

def get_font_family():
    """Get appropriate font family for current platform"""
    if IS_WINDOWS:
        return ["Microsoft YaHei", "SimHei", "Arial"]
    elif IS_MAC:
        return ["PingFang SC", "Hiragino Sans GB", "Arial"]
    elif IS_LINUX:
        return ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "DejaVu Sans"]
    else:
        return ["Arial", "sans-serif"]