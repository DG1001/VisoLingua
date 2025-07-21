"""
Utility helper functions
"""

import os
import sys
import json
import time
import hashlib
import platform
from typing import Any, Dict, List, Tuple, Optional, Union
from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

from utils.constants import *


def ensure_dir(directory: str) -> str:
    """Ensure directory exists, create if not"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return directory


def get_resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_json_file(file_path: str) -> Optional[Dict]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None


def save_json_file(file_path: str, data: Dict) -> bool:
    """Save data to JSON file safely"""
    try:
        ensure_dir(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def format_time_duration(seconds: float) -> str:
    """Format time duration in human readable format"""
    if seconds < 1:
        return f"{int(seconds * 1000)}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def validate_bbox(bbox: Tuple[int, int, int, int]) -> bool:
    """Validate bounding box coordinates"""
    if len(bbox) != 4:
        return False
    
    left, top, right, bottom = bbox
    
    # Check if coordinates are valid
    if left >= right or top >= bottom:
        return False
        
    # Check minimum size
    width = right - left
    height = bottom - top
    
    return width >= MIN_BBOX_SIZE[0] and height >= MIN_BBOX_SIZE[1]


def clamp_bbox_to_screen(bbox: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    """Clamp bounding box to screen boundaries"""
    try:
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
    except:
        # Fallback to common screen size
        screen_width, screen_height = 1920, 1080
    
    left, top, right, bottom = bbox
    
    # Clamp to screen boundaries
    left = max(0, min(left, screen_width))
    top = max(0, min(top, screen_height))
    right = max(left + MIN_BBOX_SIZE[0], min(right, screen_width))
    bottom = max(top + MIN_BBOX_SIZE[1], min(bottom, screen_height))
    
    return (left, top, right, bottom)


def resize_image_proportional(image: Image.Image, max_size: Tuple[int, int]) -> Image.Image:
    """Resize image while maintaining aspect ratio"""
    max_width, max_height = max_size
    width, height = image.size
    
    # Calculate scaling factor
    scale_x = max_width / width
    scale_y = max_height / height
    scale = min(scale_x, scale_y)
    
    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return image


def center_window(window: tk.Tk, width: int = None, height: int = None):
    """Center window on screen"""
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
        
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")


def create_rounded_rectangle(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, 
                           radius: int = 10, **kwargs) -> int:
    """Create a rounded rectangle on canvas"""
    points = []
    for x, y in [(x1, y1 + radius), (x1, y1), (x1 + radius, y1),
                 (x2 - radius, y1), (x2, y1), (x2, y1 + radius),
                 (x2, y2 - radius), (x2, y2), (x2 - radius, y2),
                 (x1 + radius, y2), (x1, y2), (x1, y2 - radius)]:
        points.extend([x, y])
    
    return canvas.create_polygon(points, smooth=True, **kwargs)


def debounce(wait_time: float):
    """Decorator to debounce function calls"""
    def decorator(func):
        last_called = [0]
        
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] > wait_time:
                last_called[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator


def throttle(wait_time: float):
    """Decorator to throttle function calls"""
    def decorator(func):
        last_called = [0]
        
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= wait_time:
                last_called[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to integer"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_bool(value: Any, default: bool = False) -> bool:
    """Safely convert value to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    try:
        return bool(int(value))
    except (ValueError, TypeError):
        return default


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def hash_string(text: str) -> str:
    """Generate hash of string"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_hotkey(hotkey: str) -> str:
    """Parse hotkey string to tkinter format"""
    # Convert common hotkey formats
    replacements = {
        'ctrl': 'Control',
        'cmd': 'Command',
        'alt': 'Alt',
        'shift': 'Shift',
        'meta': 'Meta'
    }
    
    parts = hotkey.lower().split('+')
    formatted_parts = []
    
    for part in parts:
        part = part.strip()
        if part in replacements:
            formatted_parts.append(replacements[part])
        else:
            formatted_parts.append(part)
    
    return '<' + '-'.join(formatted_parts) + '>'


def is_valid_image(image_path: str) -> bool:
    """Check if file is a valid image"""
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False


def get_image_info(image: Image.Image) -> Dict[str, Any]:
    """Get information about an image"""
    return {
        'size': image.size,
        'mode': image.mode,
        'format': image.format,
        'width': image.width,
        'height': image.height,
        'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info
    }


def create_error_image(width: int = 200, height: int = 100, text: str = "Error") -> Image.Image:
    """Create a simple error image"""
    img = Image.new('RGB', (width, height), color='red')
    # In a full implementation, you'd add text rendering here
    return img


def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    timestamp = get_timestamp()
    error_msg = f"[{timestamp}] ERROR in {context}: {type(error).__name__}: {error}"
    print(error_msg)
    
    # In a full implementation, you might write to a log file
    if DEBUG:
        import traceback
        traceback.print_exc()


def show_notification(title: str, message: str, duration: int = 3000):
    """Show notification (platform-specific implementation would go here)"""
    print(f"NOTIFICATION: {title} - {message}")


def get_system_fonts() -> List[str]:
    """Get list of available system fonts"""
    try:
        import tkinter.font as tkfont
        root = tk.Tk()
        fonts = list(tkfont.families())
        root.destroy()
        return sorted(fonts)
    except Exception:
        return get_font_family()


def validate_config_value(value: Any, expected_type: type, default: Any = None) -> Any:
    """Validate and convert config value"""
    if value is None:
        return default
        
    try:
        if expected_type == bool:
            return safe_bool(value, default)
        elif expected_type == int:
            return safe_int(value, default)
        elif expected_type == float:
            return safe_float(value, default)
        elif expected_type == str:
            return str(value)
        else:
            return value
    except Exception:
        return default


def cleanup_temp_files(temp_dir: str, max_age: int = 3600):
    """Clean up temporary files older than max_age seconds"""
    if not os.path.exists(temp_dir):
        return
        
    current_time = time.time()
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > max_age:
                    os.remove(file_path)
        except Exception as e:
            log_error(e, f"cleanup_temp_files: {file_path}")


def memory_usage() -> Dict[str, Any]:
    """Get current memory usage information"""
    try:
        import psutil
        process = psutil.Process()
        return {
            'rss': process.memory_info().rss,
            'vms': process.memory_info().vms,
            'percent': process.memory_percent(),
            'formatted_rss': format_file_size(process.memory_info().rss)
        }
    except ImportError:
        return {'error': 'psutil not available'}
    except Exception as e:
        return {'error': str(e)}