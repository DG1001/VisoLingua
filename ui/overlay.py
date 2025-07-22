"""
Transparent overlay window for screenshot capture
"""

import tkinter as tk
from tkinter import ttk
from utils.helpers import get_safe_cursor
from .base_window import BaseWindow


class OverlayWindow(BaseWindow):
    """Transparent overlay window for capturing screenshots"""
    
    def __init__(self, parent, settings, on_screenshot_callback, toggle_callback=None, quit_callback=None):
        super().__init__(settings)
        self.parent = parent
        self.on_screenshot = on_screenshot_callback
        self.toggle_callback = toggle_callback
        self.quit_callback = quit_callback
        
        # Create overlay window
        self.window = tk.Toplevel(parent)
        self.window.withdraw()  # Start hidden
        
        # Window configuration
        self.window.title("VisoLingua - Capture")
        
        # Windows DPI awareness
        self._setup_dpi_awareness()
        
        # Make window more visible (0.05 is too transparent)
        transparency = self.settings.getfloat('ui', 'overlay_transparency', 0.05)
        # Ensure minimum visibility
        if transparency < 0.3:
            transparency = 0.7  # 30% transparent, 70% visible
        self.window.attributes('-alpha', transparency)
        self.window.attributes('-topmost', self.settings.getboolean('ui', 'always_on_top', True))
        # Don't remove decorations initially to make window visible
        # self.window.overrideredirect(True)
        
        # Minimum size
        self.min_width = 200
        self.min_height = 200
        
        # Initial size and position - use actual screen coordinates
        self._calculate_initial_geometry()
        
        # Configure window
        self._setup_window()
        self._setup_bindings()
        
        # Handle window close event - should quit the entire app
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Setup font scaling
        self.setup_fonts()
        self.bind_font_scaling(self.window)
        
        # Drag and resize state
        self.dragging = False
        self.resizing = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def _setup_dpi_awareness(self):
        """Setup DPI awareness for Windows"""
        try:
            import platform
            if platform.system() == 'Windows':
                # Try to set DPI awareness
                try:
                    import ctypes
                    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # PROCESS_SYSTEM_DPI_AWARE
                except:
                    try:
                        ctypes.windll.user32.SetProcessDPIAware()
                    except:
                        pass  # DPI awareness not available
        except:
            pass  # Not on Windows or DPI functions not available
            
    def _calculate_initial_geometry(self):
        """Calculate proper initial geometry accounting for DPI"""
        # Let tkinter initialize first
        self.window.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate initial size (accounting for DPI scaling)
        self.width = min(400, screen_width // 4)
        self.height = min(300, screen_height // 4)
        
        # Calculate centered position
        self.x = (screen_width - self.width) // 4  # Not fully centered, but visible
        self.y = (screen_height - self.height) // 4
        
        print(f"Calculated initial geometry: {self.width}x{self.height}+{self.x}+{self.y}")
        print(f"Screen size: {screen_width}x{screen_height}")
        
    def _setup_window(self):
        """Setup window appearance and layout"""
        # Create main frame with border
        border_color = self.settings.get('ui', 'overlay_border_color', '#FF0000')
        border_width = self.settings.getint('ui', 'overlay_border_width', 2)
        
        self.main_frame = tk.Frame(
            self.window,
            bg=border_color,
            highlightthickness=border_width,
            highlightcolor=border_color,
            highlightbackground=border_color
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inner transparent area
        self.capture_area = tk.Frame(
            self.main_frame,
            bg='black',
            cursor='crosshair'
        )
        self.capture_area.pack(fill=tk.BOTH, expand=True, padx=border_width, pady=border_width)
        
        # Title bar for dragging
        self.title_bar = tk.Label(
            self.main_frame,
            text="VisoLingua - Click to Capture",
            bg=border_color,
            fg='white',
            font=('Arial', 8),
            cursor='fleur'
        )
        self.title_bar.pack(side=tk.TOP, fill=tk.X)
        
        # Resize handle
        resize_cursor = get_safe_cursor('sizing', 'hand2')
        
        self.resize_handle = tk.Label(
            self.main_frame,
            text="◢",
            bg=border_color,
            fg='white',
            font=('Arial', 12),
            cursor=resize_cursor
        )
        self.resize_handle.place(relx=1.0, rely=1.0, anchor='se')
        
    def _setup_bindings(self):
        """Setup mouse event bindings"""
        # Click to capture
        self.capture_area.bind('<Button-1>', self._on_capture_click)
        
        # Double-click title bar to toggle modes
        self.title_bar.bind('<Double-Button-1>', self._on_title_double_click)
        
        # Drag title bar
        self.title_bar.bind('<Button-1>', self._on_drag_start)
        self.title_bar.bind('<B1-Motion>', self._on_drag_motion)
        self.title_bar.bind('<ButtonRelease-1>', self._on_drag_end)
        
        # Resize handle
        self.resize_handle.bind('<Button-1>', self._on_resize_start)
        self.resize_handle.bind('<B1-Motion>', self._on_resize_motion)
        self.resize_handle.bind('<ButtonRelease-1>', self._on_resize_end)
        
    def _on_capture_click(self, event):
        """Handle click in capture area"""
        # Get window geometry for screenshot
        bbox = self._get_capture_bbox()
        
        # Visual feedback
        self._flash_border()
        
        # Trigger screenshot
        if self.on_screenshot:
            self.on_screenshot(bbox)
            
    def _get_capture_bbox(self):
        """Get bounding box for screenshot capture"""
        # Get window position and size
        self.window.update_idletasks()
        x = self.window.winfo_rootx()
        y = self.window.winfo_rooty()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        
        # Account for border and title bar
        border_width = self.settings.getint('ui', 'overlay_border_width', 2)
        title_height = self.title_bar.winfo_reqheight()
        
        return (
            x + border_width,
            y + title_height + border_width,
            x + width - border_width,
            y + height - border_width
        )
        
    def _flash_border(self):
        """Flash border for visual feedback"""
        original_color = self.settings.get('ui', 'overlay_border_color', '#FF0000')
        flash_color = '#00FF00'
        
        # Flash to green
        self.main_frame.configure(bg=flash_color, highlightcolor=flash_color, highlightbackground=flash_color)
        self.title_bar.configure(bg=flash_color)
        self.resize_handle.configure(bg=flash_color)
        
        # Return to original after 200ms
        self.window.after(200, lambda: self._restore_border_color(original_color))
        
    def _restore_border_color(self, color):
        """Restore original border color"""
        self.main_frame.configure(bg=color, highlightcolor=color, highlightbackground=color)
        self.title_bar.configure(bg=color)
        self.resize_handle.configure(bg=color)
        
    def _on_title_double_click(self, event):
        """Handle double-click on title bar"""
        # Switch to result mode if available
        if self.toggle_callback:
            self.toggle_callback()
            
    def _on_drag_start(self, event):
        """Start dragging window"""
        self.dragging = True
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
    def _on_drag_motion(self, event):
        """Handle window dragging"""
        if self.dragging:
            dx = event.x_root - self.drag_start_x
            dy = event.y_root - self.drag_start_y
            
            new_x = self.window.winfo_x() + dx
            new_y = self.window.winfo_y() + dy
            
            self.window.geometry(f"+{new_x}+{new_y}")
            
            self.drag_start_x = event.x_root
            self.drag_start_y = event.y_root
            
    def _on_drag_end(self, event):
        """End window dragging"""
        self.dragging = False
        
    def _on_resize_start(self, event):
        """Start resizing window"""
        self.resizing = True
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_start_width = self.window.winfo_width()
        self.resize_start_height = self.window.winfo_height()
        
    def _on_resize_motion(self, event):
        """Handle window resizing"""
        if self.resizing:
            dx = event.x_root - self.resize_start_x
            dy = event.y_root - self.resize_start_y
            
            new_width = max(self.min_width, self.resize_start_width + dx)
            new_height = max(self.min_height, self.resize_start_height + dy)
            
            self.window.geometry(f"{new_width}x{new_height}")
            
    def _on_resize_end(self, event):
        """End window resizing"""
        self.resizing = False
        
    def show(self):
        """Show overlay window"""
        print("Showing overlay window...")
        
        self.window.deiconify()
        self.window.lift()
        self.window.attributes('-topmost', True)
        
        # Set geometry - always use calculated values
        geometry = f"{self.width}x{self.height}+{self.x}+{self.y}"
        print(f"Setting overlay geometry: {geometry}")
        self.window.geometry(geometry)
        
        # Force update to ensure proper sizing
        self.window.update_idletasks()
        
        # Verify actual size after showing
        actual_width = self.window.winfo_width()
        actual_height = self.window.winfo_height()
        actual_x = self.window.winfo_x()
        actual_y = self.window.winfo_y()
        print(f"Actual geometry after show: {actual_width}x{actual_height}+{actual_x}+{actual_y}")
        
        # Update stored values with actual values
        self.width = actual_width
        self.height = actual_height
        self.x = actual_x
        self.y = actual_y
        
    def hide(self):
        """Hide overlay window"""
        # Save current position and size before hiding
        try:
            if self.window.winfo_viewable():
                self.x = self.window.winfo_x()
                self.y = self.window.winfo_y()
                self.width = self.window.winfo_width()
                self.height = self.window.winfo_height()
                print(f"Saving overlay geometry: {self.width}x{self.height}+{self.x}+{self.y}")
        except tk.TclError:
            pass  # Window might not be available
        
        self.window.withdraw()
        
    def _on_window_close(self):
        """Handle overlay window close - quit entire application"""
        print("Overlay window closed - quitting application")
        if self.quit_callback:
            self.quit_callback()
        else:
            # Fallback: quit the main application
            self.parent.quit()
            
    def destroy(self):
        """Destroy overlay window"""
        if self.window:
            self.window.destroy()