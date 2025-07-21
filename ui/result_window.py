"""
Result window for displaying translations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
from typing import List, Dict


class ResultWindow:
    """Window for displaying translation results"""
    
    def __init__(self, parent, settings, toggle_callback=None):
        self.parent = parent
        self.settings = settings
        self.toggle_callback = toggle_callback
        
        # Create result window
        self.window = tk.Toplevel(parent)
        self.window.withdraw()  # Start hidden
        
        # Window configuration
        self.window.title("VisoLingua - Translation Result")
        self.window.geometry("500x400")
        self.window.minsize(400, 300)
        
        # Translation history
        self.translation_history: List[Dict] = []
        self.max_history = self.settings.getint('translation', 'max_cache_entries', 100)
        
        # Setup UI
        self._setup_ui()
        self._setup_bindings()
        
        # Handle window close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
    def _setup_ui(self):
        """Setup the result window UI"""
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="VisoLingua - Translation Result",
            font=('Arial', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Translation display area
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=15,
            font=('Microsoft YaHei', 10),  # Chinese font support
            state=tk.DISABLED
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Copy button
        self.copy_button = ttk.Button(
            button_frame,
            text="Copy Translation",
            command=self._copy_translation,
            state=tk.DISABLED
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Clear button
        self.clear_button = ttk.Button(
            button_frame,
            text="Clear",
            command=self._clear_result
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Back to capture button
        self.back_button = ttk.Button(
            button_frame,
            text="Back to Capture",
            command=self._back_to_capture
        )
        self.back_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Settings button
        self.settings_button = ttk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings
        )
        self.settings_button.pack(side=tk.RIGHT)
        
        # History dropdown
        history_frame = ttk.Frame(main_frame)
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(history_frame, text="History:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.history_var = tk.StringVar()
        self.history_dropdown = ttk.Combobox(
            history_frame,
            textvariable=self.history_var,
            state="readonly",
            width=50
        )
        self.history_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.history_dropdown.bind('<<ComboboxSelected>>', self._on_history_selected)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready for translation",
            font=('Arial', 8)
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Loading indicator
        self.loading_label = ttk.Label(
            main_frame,
            text="Processing translation...",
            font=('Arial', 10),
            foreground='blue'
        )
        
        # Current translation text
        self.current_translation = ""
        
    def _setup_bindings(self):
        """Setup event bindings"""
        # Copy shortcut
        self.window.bind('<Control-c>', lambda e: self._copy_translation())
        
        # Close with Escape
        self.window.bind('<Escape>', lambda e: self.hide())
        
        # Toggle with double-click on title area
        title_area = self.window
        # This would be handled by parent app
        
    def show_translation(self, translation: str, source_language: str = None, processing_time: float = None):
        """Display translation result"""
        self.current_translation = translation
        
        # Update text area
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, translation)
        self.text_area.config(state=tk.DISABLED)
        
        # Enable copy button
        self.copy_button.config(state=tk.NORMAL)
        
        # Update status
        status_text = "Translation complete"
        if processing_time:
            status_text += f" ({processing_time:.2f}s)"
        if source_language:
            status_text += f" - Source: {source_language}"
        self.status_label.config(text=status_text)
        
        # Add to history
        self._add_to_history(translation, source_language)
        
        # Hide loading indicator
        self.loading_label.pack_forget()
        
    def show_loading(self):
        """Show loading indicator"""
        self.loading_label.pack(pady=10)
        self.status_label.config(text="Processing translation...")
        
    def show_error(self, error_message: str):
        """Display error message"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, f"Error: {error_message}")
        self.text_area.config(state=tk.DISABLED)
        
        self.status_label.config(text="Translation failed")
        self.copy_button.config(state=tk.DISABLED)
        
        # Hide loading indicator
        self.loading_label.pack_forget()
        
    def _copy_translation(self):
        """Copy current translation to clipboard"""
        if self.current_translation:
            try:
                pyperclip.copy(self.current_translation)
                self.status_label.config(text="Translation copied to clipboard")
                
                # Reset status after 2 seconds
                self.window.after(2000, lambda: self.status_label.config(text="Ready"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy to clipboard: {e}")
                
    def _clear_result(self):
        """Clear the result display"""
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
        
        self.current_translation = ""
        self.copy_button.config(state=tk.DISABLED)
        self.status_label.config(text="Cleared")
        
    def _add_to_history(self, translation: str, source_language: str = None):
        """Add translation to history"""
        # Create history entry
        preview = translation[:50] + "..." if len(translation) > 50 else translation
        preview = preview.replace('\n', ' ')  # Single line for dropdown
        
        history_entry = {
            'preview': preview,
            'full_text': translation,
            'source_language': source_language,
            'timestamp': tk.datetime.now() if hasattr(tk, 'datetime') else None
        }
        
        # Add to beginning of history
        self.translation_history.insert(0, history_entry)
        
        # Limit history size
        if len(self.translation_history) > self.max_history:
            self.translation_history = self.translation_history[:self.max_history]
            
        # Update dropdown
        self._update_history_dropdown()
        
    def _update_history_dropdown(self):
        """Update history dropdown with recent translations"""
        previews = [entry['preview'] for entry in self.translation_history]
        self.history_dropdown['values'] = previews
        
    def _on_history_selected(self, event):
        """Handle history selection"""
        selection_index = self.history_dropdown.current()
        if 0 <= selection_index < len(self.translation_history):
            entry = self.translation_history[selection_index]
            self.show_translation(
                entry['full_text'],
                entry.get('source_language')
            )
            
    def _open_settings(self):
        """Open settings dialog"""
        # Simple settings dialog
        settings_window = tk.Toplevel(self.window)
        settings_window.title("VisoLingua Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # LLM selection
        ttk.Label(settings_window, text="Default LLM:").pack(pady=10)
        
        llm_var = tk.StringVar(value=self.settings.get('api', 'default_llm', 'gemini-2.5-flash'))
        llm_combo = ttk.Combobox(
            settings_window,
            textvariable=llm_var,
            values=['gemini-2.5-flash', 'gpt-4.1-mini', 'gpt-4.1-nano'],
            state="readonly"
        )
        llm_combo.pack(pady=5)
        
        # API Keys
        ttk.Label(settings_window, text="Gemini API Key:").pack(pady=(20, 5))
        gemini_key_var = tk.StringVar(value=self.settings.get('api', 'gemini_api_key', ''))
        gemini_entry = ttk.Entry(settings_window, textvariable=gemini_key_var, width=40, show='*')
        gemini_entry.pack(pady=5)
        
        ttk.Label(settings_window, text="OpenAI API Key:").pack(pady=(10, 5))
        openai_key_var = tk.StringVar(value=self.settings.get('api', 'openai_api_key', ''))
        openai_entry = ttk.Entry(settings_window, textvariable=openai_key_var, width=40, show='*')
        openai_entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(pady=20)
        
        def save_settings():
            self.settings.set('api', 'default_llm', llm_var.get())
            self.settings.set('api', 'gemini_api_key', gemini_key_var.get())
            self.settings.set('api', 'openai_api_key', openai_key_var.get())
            self.settings.save()
            settings_window.destroy()
            
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def _back_to_capture(self):
        """Switch back to capture mode"""
        if self.toggle_callback:
            self.toggle_callback()
            
    def _on_window_close(self):
        """Handle window close event - switch back to capture"""
        self._back_to_capture()
        
    def show(self):
        """Show result window"""
        self.window.deiconify()
        self.window.lift()
        
    def hide(self):
        """Hide result window"""
        self.window.withdraw()
        
    def destroy(self):
        """Destroy result window"""
        if self.window:
            self.window.destroy()