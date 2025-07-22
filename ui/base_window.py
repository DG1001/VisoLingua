"""
Base window class with font scaling support
"""

import tkinter as tk
import tkinter.font as tkFont
from typing import Dict, List


class BaseWindow:
    """Base class for windows with font scaling support"""
    
    def __init__(self, settings):
        self.settings = settings
        self.fonts: Dict[str, tkFont.Font] = {}
        self.widgets_with_fonts: List[tk.Widget] = []
        
    def setup_fonts(self):
        """Setup scalable fonts for the window"""
        font_config = self.settings.get_font_config()
        
        # Create different font styles
        self.fonts = {
            'default': tkFont.Font(family=font_config['family'], size=font_config['size']),
            'bold': tkFont.Font(family=font_config['family'], size=font_config['size'], weight='bold'),
            'small': tkFont.Font(family=font_config['family'], size=max(8, font_config['size'] - 2)),
            'large': tkFont.Font(family=font_config['family'], size=font_config['size'] + 2)
        }
        
    def register_widget_font(self, widget: tk.Widget, font_name: str = 'default'):
        """Register a widget to use a specific font"""
        if font_name in self.fonts:
            try:
                # Get widget class name to determine if it's ttk
                widget_class = widget.__class__.__name__
                widget_module = widget.__class__.__module__
                
                # Skip ttk widgets as they don't support font configuration directly
                if 'ttk' in widget_module or widget_class.startswith('Ttk'):
                    return
                    
                # Only configure font for standard tk widgets that support it
                if hasattr(widget, 'keys') and 'font' in widget.keys():
                    widget.configure(font=self.fonts[font_name])
                    self.widgets_with_fonts.append((widget, font_name))
                    
            except (AttributeError, tk.TclError):
                # Widget doesn't support font configuration
                pass
            
    def scale_fonts(self, delta: int):
        """Scale all fonts by delta size"""
        new_size = self.settings.scale_font(delta)
        
        # Update all font objects
        for font_name, font_obj in self.fonts.items():
            base_size = new_size
            if font_name == 'small':
                base_size = max(8, new_size - 2)
            elif font_name == 'large':
                base_size = new_size + 2
                
            font_obj.configure(size=base_size)
            
        return new_size
        
    def bind_font_scaling(self, widget: tk.Widget):
        """Bind mouse wheel font scaling to a widget"""
        def on_mouse_wheel(event):
            if event.state & 0x4:  # Ctrl key pressed
                delta = 1 if event.delta > 0 else -1
                self.scale_fonts(delta)
                return "break"
                
        # Bind to both wheel events for cross-platform compatibility
        widget.bind("<Control-MouseWheel>", on_mouse_wheel)  # Windows
        widget.bind("<Control-Button-4>", lambda e: on_mouse_wheel(type('Event', (), {'delta': 120, 'state': 0x4})()))  # Linux up
        widget.bind("<Control-Button-5>", lambda e: on_mouse_wheel(type('Event', (), {'delta': -120, 'state': 0x4})()))  # Linux down
        
    def setup_window_font_scaling(self, window: tk.Toplevel):
        """Setup font scaling for an entire window"""
        self.setup_fonts()
        self.bind_font_scaling(window)
        
        # Apply fonts to existing widgets recursively
        def apply_fonts_recursive(widget):
            try:
                # Check if widget has font option
                if 'font' in widget.keys():
                    self.register_widget_font(widget, 'default')
            except:
                pass
                
            # Process children
            for child in widget.winfo_children():
                apply_fonts_recursive(child)
                
        # Apply fonts after a short delay to ensure all widgets are created
        window.after(100, lambda: apply_fonts_recursive(window))