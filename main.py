#!/usr/bin/env python3
"""
VisoLingua - Live Translation Overlay Tool
Main application entry point
"""

import tkinter as tk
import asyncio
import threading
import sys
import os

from config.settings import Settings
from ui.overlay import OverlayWindow
from ui.result_window import ResultWindow
from core.screenshot import ScreenCapture
from core.translator import Translator


class VisoLinguaApp:
    def __init__(self):
        self.settings = Settings()
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window initially
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.translator = Translator(self.settings)
        
        # Initialize windows
        self.overlay = OverlayWindow(self.root, self.settings, self.on_screenshot, self.switch_to_result, self.quit)
        self.result_window = ResultWindow(self.root, self.settings, self.switch_to_capture, self.quit)
        
        # Current mode: 'capture' or 'result'
        self.current_mode = 'capture'
        
        # Setup event loop for async operations
        self.loop = asyncio.new_event_loop()
        self.async_thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.async_thread.start()
        
    def _run_async_loop(self):
        """Run async event loop in separate thread"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        
    def on_screenshot(self, bbox):
        """Handle screenshot capture from overlay"""
        asyncio.run_coroutine_threadsafe(
            self._process_screenshot(bbox), 
            self.loop
        )
        
    async def _process_screenshot(self, bbox):
        """Process screenshot asynchronously"""
        try:
            # Capture screenshot
            image = self.screen_capture.capture_area(bbox)
            
            # Show loading in result window
            self.root.after(0, self.result_window.show_loading)
            
            # Translate
            translation = await self.translator.translate_image(image)
            
            # Display result
            self.root.after(0, lambda: self.result_window.show_translation(translation))
            
            # Switch to result mode
            self.root.after(0, self.switch_to_result)
            
        except Exception as e:
            self.root.after(0, lambda: self.result_window.show_error(str(e)))
            self.root.after(0, self.switch_to_result)
            
    def switch_to_capture(self):
        """Switch to capture mode"""
        print("Switching to capture mode...")
        self.current_mode = 'capture'
        self.result_window.hide()
        self.overlay.show()
        
    def switch_to_result(self):
        """Switch to result mode"""
        print("Switching to result mode...")
        self.current_mode = 'result'
        self.overlay.hide()
        self.result_window.show()
        
    def toggle_mode(self):
        """Toggle between capture and result modes"""
        if self.current_mode == 'capture':
            self.switch_to_result()
        else:
            self.switch_to_capture()
            
    def run(self):
        """Start the application"""
        print(f"Starting {self.settings.get('ui', 'overlay_transparency')}% transparent overlay...")
        print("Look for a red-bordered window that you can drag and resize.")
        print("Click inside the red area to capture screenshots for translation.")
        print("Double-click the title bar to switch between capture and result modes.")
        
        # Setup global hotkeys
        self.root.bind('<Control-Tab>', lambda e: self.toggle_mode())
        
        # Show initial overlay
        self.overlay.show()
        
        # Start main loop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.quit()
            
    def quit(self):
        """Clean shutdown"""
        print("Shutting down VisoLingua...")
        try:
            # Stop async loop
            if hasattr(self, 'loop') and self.loop.is_running():
                self.loop.call_soon_threadsafe(self.loop.stop)
                
            # Close windows
            if hasattr(self, 'result_window'):
                self.result_window.destroy()
            if hasattr(self, 'overlay'):
                self.overlay.destroy()
                
            # Quit main application
            self.root.quit()
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
            # Force quit
            import sys
            sys.exit(0)


def main():
    """Application entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        print("VisoLingua - Live Translation Overlay Tool")
        print("Usage: python main.py")
        return
        
    try:
        app = VisoLinguaApp()
        app.run()
    except Exception as e:
        print(f"Error starting VisoLingua: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()