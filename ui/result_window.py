"""
Result window for displaying translations
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip
from typing import List, Dict
from .base_window import BaseWindow


class ResultWindow(BaseWindow):
    """Window for displaying translation results"""
    
    def __init__(self, parent, settings, toggle_callback=None, quit_callback=None):
        super().__init__(settings)
        self.parent = parent
        self.toggle_callback = toggle_callback
        self.quit_callback = quit_callback
        
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
        
        # Setup font scaling for main window
        self.setup_window_font_scaling(self.window)
        
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
        
        # Quit button
        self.quit_button = ttk.Button(
            button_frame,
            text="Quit",
            command=self._quit_app
        )
        self.quit_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Settings button
        self.settings_button = ttk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings
        )
        self.settings_button.pack(side=tk.RIGHT, padx=(0, 5))
        
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
        settings_window.geometry("500x500")
        settings_window.transient(self.window)
        settings_window.grab_set()
        
        # Setup font scaling for settings window
        self.setup_window_font_scaling(settings_window)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Cloud LLM Tab
        cloud_frame = ttk.Frame(notebook)
        notebook.add(cloud_frame, text="Cloud LLMs")
        
        # === Cloud LLM Tab Content ===
        # LLM selection
        ttk.Label(cloud_frame, text="Default LLM:").pack(pady=10)
        
        # Get available LLMs (cloud + ollama if enabled)
        available_llms = ['gemini-2.5-flash', 'gpt-4.1-mini', 'gpt-4.1-nano']
        if self.settings.getboolean('ollama', 'enabled', False):
            available_llms.extend(['ollama-llava-7b', 'ollama-internvl-2b', 'ollama-qwen2vl-7b', 'ollama-cogvlm2-19b'])
        
        llm_var = tk.StringVar(value=self.settings.get('api', 'default_llm', 'gemini-2.5-flash'))
        llm_combo = ttk.Combobox(
            cloud_frame,
            textvariable=llm_var,
            values=available_llms,
            state="readonly"
        )
        llm_combo.pack(pady=5)
        
        # API Keys
        ttk.Label(cloud_frame, text="Gemini API Key:").pack(pady=(20, 5))
        gemini_key_var = tk.StringVar(value=self.settings.get('api', 'gemini_api_key', ''))
        gemini_entry = ttk.Entry(cloud_frame, textvariable=gemini_key_var, width=40, show='*')
        gemini_entry.pack(pady=5)
        
        ttk.Label(cloud_frame, text="OpenAI API Key:").pack(pady=(10, 5))
        openai_key_var = tk.StringVar(value=self.settings.get('api', 'openai_api_key', ''))
        openai_entry = ttk.Entry(cloud_frame, textvariable=openai_key_var, width=40, show='*')
        openai_entry.pack(pady=5)
        
        # === Local Ollama Tab ===
        ollama_frame = ttk.Frame(notebook)
        notebook.add(ollama_frame, text="Local Ollama")
        
        # Ollama enable/disable
        ollama_enabled_var = tk.BooleanVar(value=self.settings.getboolean('ollama', 'enabled', False))
        ollama_check = ttk.Checkbutton(ollama_frame, text="Enable Ollama (Local LLMs)", variable=ollama_enabled_var)
        ollama_check.pack(pady=10)
        
        # Ollama URL
        ttk.Label(ollama_frame, text="Ollama Server URL:").pack(pady=(10, 5))
        ollama_url_var = tk.StringVar(value=self.settings.get('ollama', 'base_url', 'http://localhost:11434'))
        ollama_url_entry = ttk.Entry(ollama_frame, textvariable=ollama_url_var, width=40)
        ollama_url_entry.pack(pady=5)
        
        # Ollama timeout
        ttk.Label(ollama_frame, text="Request Timeout (seconds):").pack(pady=(10, 5))
        ollama_timeout_var = tk.StringVar(value=str(self.settings.getint('ollama', 'timeout', 30)))
        ollama_timeout_entry = ttk.Entry(ollama_frame, textvariable=ollama_timeout_var, width=10)
        ollama_timeout_entry.pack(pady=5)
        
        # Ollama model selection
        ttk.Label(ollama_frame, text="Model Selection:").pack(pady=(20, 5))
        
        model_frame = ttk.Frame(ollama_frame)
        model_frame.pack(pady=5, fill='x', padx=20)
        
        # Auto-detect models from Ollama
        available_models_var = tk.StringVar(value="")
        model_combo = ttk.Combobox(model_frame, textvariable=available_models_var, width=30)
        model_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh models button
        def refresh_models():
            # Show loading message
            refresh_btn.config(text="Loading...", state="disabled")
            
            def fetch_models_thread():
                try:
                    import asyncio
                    import aiohttp
                    
                    # Simple direct HTTP request instead of using translator
                    base_url = self.settings.get('ollama', 'base_url', 'http://localhost:11434')
                    
                    async def get_models():
                        timeout = aiohttp.ClientTimeout(total=5)
                        async with aiohttp.ClientSession(timeout=timeout) as session:
                            async with session.get(f"{base_url}/api/tags") as response:
                                if response.status == 200:
                                    result = await response.json()
                                    return result.get('models', [])
                                else:
                                    raise Exception(f"HTTP {response.status}")
                    
                    # Run async function
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        models_data = loop.run_until_complete(get_models())
                        loop.close()
                        
                        # Extract model names
                        model_names = [m['name'] for m in models_data if 'name' in m]
                        
                        # Update UI in main thread
                        def update_ui():
                            refresh_btn.config(text="Refresh Models", state="normal")
                            if model_names:
                                model_combo['values'] = model_names
                                # Set current model if available
                                current_model = self.settings.get('ollama', 'model', 'llava:7b')
                                if current_model in model_names:
                                    available_models_var.set(current_model)
                                else:
                                    available_models_var.set(model_names[0])
                                tk.messagebox.showinfo("Models Found", 
                                    f"Found {len(model_names)} models:\n" + 
                                    "\n".join(model_names[:10]) + 
                                    ("\n..." if len(model_names) > 10 else ""))
                            else:
                                tk.messagebox.showwarning("No Models", "No models found. Make sure Ollama is running and has models installed.")
                                available_models_var.set(self.settings.get('ollama', 'model', 'llava:7b'))
                        
                        settings_window.after(0, update_ui)
                        
                    except Exception as e:
                        def show_error():
                            refresh_btn.config(text="Refresh Models", state="normal")
                            error_msg = str(e)
                            if "Connection" in error_msg or "timeout" in error_msg.lower():
                                error_msg = "Connection failed. Is Ollama running?\n\nStart Ollama with: ollama serve"
                            tk.messagebox.showerror("Connection Error", f"Failed to connect to Ollama:\n{error_msg}")
                            available_models_var.set(self.settings.get('ollama', 'model', 'llava:7b'))
                        
                        settings_window.after(0, show_error)
                        
                except Exception as e:
                    def show_error():
                        refresh_btn.config(text="Refresh Models", state="normal")
                        tk.messagebox.showerror("Error", f"Error refreshing models:\n{str(e)}")
                        available_models_var.set(self.settings.get('ollama', 'model', 'llava:7b'))
                    
                    settings_window.after(0, show_error)
            
            # Run in background thread
            import threading
            threading.Thread(target=fetch_models_thread, daemon=True).start()
        
        refresh_btn = ttk.Button(model_frame, text="Refresh Models", command=refresh_models)
        refresh_btn.pack(side=tk.LEFT)
        
        # Set initial model value
        available_models_var.set(self.settings.get('ollama', 'model', 'llava:7b'))
        
        # Model recommendations
        ttk.Label(ollama_frame, text="Recommended Ollama Models:", font=('TkDefaultFont', 10, 'bold')).pack(pady=(20, 10))
        
        models_text = tk.Text(ollama_frame, height=8, width=60, wrap=tk.WORD)
        models_text.pack(pady=5)
        
        model_info = """• InternVL2 2B - Fastest, good for prototyping
  ollama pull internvl2:2b

• LLaVA 7B - Optimal balance of speed and quality  
  ollama pull llava:7b

• Qwen2-VL 7B - Best Chinese text recognition
  ollama pull qwen2-vl:7b

• CogVLM2 19B - Highest quality (requires more VRAM)
  ollama pull cogvlm2:19b"""
        
        models_text.insert('1.0', model_info)
        models_text.config(state='disabled')
        
        # Test Ollama connection button
        def test_ollama():
            test_btn.config(text="Testing...", state="disabled")
            
            def test_thread():
                try:
                    import asyncio
                    import aiohttp
                    
                    base_url = self.settings.get('ollama', 'base_url', 'http://localhost:11434')
                    
                    async def test_connection():
                        timeout = aiohttp.ClientTimeout(total=5)
                        async with aiohttp.ClientSession(timeout=timeout) as session:
                            async with session.get(f"{base_url}/api/tags") as response:
                                if response.status == 200:
                                    result = await response.json()
                                    return True, result.get('models', [])
                                else:
                                    return False, f"HTTP {response.status}"
                    
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        success, data = loop.run_until_complete(test_connection())
                        loop.close()
                        
                        def show_result():
                            test_btn.config(text="Test Ollama Connection", state="normal")
                            if success:
                                model_count = len(data) if isinstance(data, list) else 0
                                tk.messagebox.showinfo("Connection Test", 
                                    f"Connection successful!\n"
                                    f"Server: {base_url}\n"
                                    f"Available models: {model_count}")
                            else:
                                tk.messagebox.showerror("Connection Test", f"Connection failed:\n{data}")
                        
                        settings_window.after(0, show_result)
                        
                    except Exception as e:
                        def show_error():
                            test_btn.config(text="Test Ollama Connection", state="normal")
                            error_msg = str(e)
                            if "Connection" in error_msg or "timeout" in error_msg.lower():
                                error_msg = "Connection failed. Is Ollama running?\n\nStart Ollama with: ollama serve"
                            tk.messagebox.showerror("Connection Test", f"Test failed:\n{error_msg}")
                        
                        settings_window.after(0, show_error)
                        
                except Exception as e:
                    def show_error():
                        test_btn.config(text="Test Ollama Connection", state="normal")
                        tk.messagebox.showerror("Connection Test", f"Unexpected error:\n{str(e)}")
                    
                    settings_window.after(0, show_error)
            
            import threading
            threading.Thread(target=test_thread, daemon=True).start()
        
        test_btn = ttk.Button(ollama_frame, text="Test Ollama Connection", command=test_ollama)
        test_btn.pack(pady=10)
        
        # === UI Settings Tab ===
        ui_frame = ttk.Frame(notebook)
        notebook.add(ui_frame, text="UI Settings")
        
        # Font settings
        ttk.Label(ui_frame, text="Font Settings:", font=('TkDefaultFont', 10, 'bold')).pack(pady=(10, 5))
        
        font_frame = ttk.Frame(ui_frame)
        font_frame.pack(pady=10)
        
        # Current font size display
        current_font_size = tk.IntVar(value=self.settings.getint('ui', 'font_size', 10))
        ttk.Label(font_frame, text=f"Font Size: {current_font_size.get()}").pack(pady=5)
        
        # Font size scale
        def on_font_size_change(value):
            size = int(float(value))
            current_font_size.set(size)
            # Update label text
            for widget in font_frame.winfo_children():
                if isinstance(widget, ttk.Label) and "Font Size:" in str(widget.cget('text')):
                    widget.configure(text=f"Font Size: {size}")
                    break
        
        font_scale = ttk.Scale(font_frame, from_=8, to=24, value=current_font_size.get(), 
                              command=on_font_size_change, orient='horizontal')
        font_scale.pack(pady=5)
        
        # Font scaling buttons
        button_frame = ttk.Frame(font_frame)
        button_frame.pack(pady=10)
        
        def increase_font():
            new_size = self.scale_fonts(1)
            font_scale.set(new_size)
            current_font_size.set(new_size)
            
        def decrease_font():
            new_size = self.scale_fonts(-1)
            font_scale.set(new_size)
            current_font_size.set(new_size)
        
        ttk.Button(button_frame, text="A-", command=decrease_font).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="A+", command=increase_font).pack(side=tk.LEFT, padx=5)
        
        # Instructions
        instructions = tk.Text(ui_frame, height=4, wrap=tk.WORD)
        instructions.pack(pady=20, padx=20, fill='x')
        instructions.insert('1.0', 
            "Font Scaling Tips:\n"
            "• Use Ctrl+Mouse Wheel to scale fonts in any window\n"
            "• Use the slider or A-/A+ buttons to adjust font size\n"
            "• Changes are saved automatically and apply to all windows")
        instructions.config(state='disabled')
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(pady=20)
        
        def save_settings():
            # Save cloud LLM settings
            self.settings.set('api', 'default_llm', llm_var.get())
            self.settings.set('api', 'gemini_api_key', gemini_key_var.get())
            self.settings.set('api', 'openai_api_key', openai_key_var.get())
            
            # Save Ollama settings
            self.settings.set('ollama', 'enabled', str(ollama_enabled_var.get()).lower())
            self.settings.set('ollama', 'base_url', ollama_url_var.get())
            self.settings.set('ollama', 'model', available_models_var.get())
            try:
                timeout_val = int(ollama_timeout_var.get())
                self.settings.set('ollama', 'timeout', str(timeout_val))
            except ValueError:
                self.settings.set('ollama', 'timeout', '30')  # Default fallback
            
            # Save UI settings (font size)
            try:
                font_size = int(font_scale.get())
                self.settings.set('ui', 'font_size', str(font_size))
            except (ValueError, NameError):
                # font_scale might not be defined if UI tab wasn't created yet
                pass
                
            self.settings.save()
            settings_window.destroy()
            tk.messagebox.showinfo("Settings", "Settings saved successfully!")
            
        ttk.Button(button_frame, text="Save", command=save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side=tk.LEFT, padx=5)
        
    def _back_to_capture(self):
        """Switch back to capture mode"""
        if self.toggle_callback:
            self.toggle_callback()
            
    def _quit_app(self):
        """Quit the entire application"""
        if self.quit_callback:
            self.quit_callback()
        else:
            # Fallback
            self.parent.quit()
            
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