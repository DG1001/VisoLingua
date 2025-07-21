"""
Screenshot capture functionality using mss
"""

import mss
from PIL import Image, ImageTk
import io
import hashlib
from typing import Tuple, Optional


class ScreenCapture:
    """Handles screen capture operations"""
    
    def __init__(self):
        self.sct = mss.mss()
        self.cache = {}  # Simple cache for identical screenshots
        
    def capture_area(self, bbox: Tuple[int, int, int, int]) -> Image.Image:
        """
        Capture screenshot of specified area
        
        Args:
            bbox: Bounding box (left, top, right, bottom)
            
        Returns:
            PIL Image of captured area
        """
        left, top, right, bottom = bbox
        
        # MSS uses different bbox format
        monitor = {
            "top": top,
            "left": left,
            "width": right - left,
            "height": bottom - top
        }
        
        # Capture screenshot
        screenshot = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        
        return img
        
    def capture_area_cached(self, bbox: Tuple[int, int, int, int]) -> Tuple[Image.Image, bool]:
        """
        Capture screenshot with caching
        
        Args:
            bbox: Bounding box (left, top, right, bottom)
            
        Returns:
            Tuple of (PIL Image, was_cached)
        """
        # Generate cache key from bbox
        cache_key = f"{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}"
        
        # Capture image
        img = self.capture_area(bbox)
        
        # Generate hash of image data
        img_hash = self._get_image_hash(img)
        full_cache_key = f"{cache_key}_{img_hash}"
        
        # Check cache
        if full_cache_key in self.cache:
            return self.cache[full_cache_key], True
            
        # Store in cache
        self.cache[full_cache_key] = img
        
        # Limit cache size
        if len(self.cache) > 50:
            # Remove oldest entries
            oldest_keys = list(self.cache.keys())[:10]
            for key in oldest_keys:
                del self.cache[key]
                
        return img, False
        
    def _get_image_hash(self, img: Image.Image) -> str:
        """Generate hash of image for caching"""
        # Convert image to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()
        
        # Generate MD5 hash
        return hashlib.md5(img_bytes).hexdigest()[:16]
        
    def optimize_image_for_llm(self, img: Image.Image, max_size: str = "4MB", quality: int = 85) -> bytes:
        """
        Optimize image for LLM API submission
        
        Args:
            img: PIL Image to optimize
            max_size: Maximum size (e.g., "4MB", "20MB")
            quality: JPEG quality (1-100)
            
        Returns:
            Optimized image as bytes
        """
        # Parse max size
        max_bytes = self._parse_size(max_size)
        
        # Start with original size
        current_quality = quality
        current_img = img.copy()
        
        while True:
            # Convert to bytes
            img_bytes = io.BytesIO()
            
            # Save as JPEG for better compression
            if current_img.mode in ('RGBA', 'LA', 'P'):
                # Convert to RGB for JPEG
                rgb_img = Image.new('RGB', current_img.size, (255, 255, 255))
                rgb_img.paste(current_img, mask=current_img.split()[-1] if current_img.mode in ('RGBA', 'LA') else None)
                current_img = rgb_img
                
            current_img.save(img_bytes, format='JPEG', quality=current_quality, optimize=True)
            img_data = img_bytes.getvalue()
            
            # Check size
            if len(img_data) <= max_bytes or current_quality <= 20:
                return img_data
                
            # Reduce quality or resize
            if current_quality > 50:
                current_quality -= 10
            else:
                # Reduce image size
                width, height = current_img.size
                new_width = int(width * 0.9)
                new_height = int(height * 0.9)
                current_img = current_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                current_quality = 60  # Reset quality after resize
                
    def _parse_size(self, size_str: str) -> int:
        """Parse size string to bytes"""
        size_str = size_str.upper()
        
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            # Assume bytes
            return int(size_str)
            
    def get_screen_info(self) -> dict:
        """Get information about available screens"""
        monitors = []
        for monitor in self.sct.monitors[1:]:  # Skip monitor 0 (all monitors)
            monitors.append({
                'left': monitor['left'],
                'top': monitor['top'],
                'width': monitor['width'],
                'height': monitor['height']
            })
            
        return {
            'monitors': monitors,
            'primary': monitors[0] if monitors else None
        }
        
    def capture_full_screen(self, monitor_index: int = 1) -> Image.Image:
        """Capture full screen of specified monitor"""
        monitor = self.sct.monitors[monitor_index]
        screenshot = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img
        
    def clear_cache(self):
        """Clear screenshot cache"""
        self.cache.clear()
        
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'sct') and self.sct:
            self.sct.close()