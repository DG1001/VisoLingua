"""
Configuration management for VisoLingua
"""

import configparser
import os
import sys
from typing import Dict, Any


class Settings:
    """Manages application settings and configuration"""
    
    def __init__(self):
        # For PyInstaller compatibility - config.ini next to EXE
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller executable
            exe_dir = os.path.dirname(sys.executable)
            self.config_file = os.path.join(exe_dir, 'config.ini')
        else:
            # Running as Python script
            self.config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
            
        self.config = configparser.ConfigParser()
        self._load_config()
        
    def _load_config(self):
        """Load configuration from file or create defaults"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self._create_default_config()
            
    def _create_default_config(self):
        """Create default configuration file"""
        self.config['api'] = {
            'default_llm': 'gemini-2.5-flash',
            'gemini_api_key': '',
            'openai_api_key': ''
        }
        
        self.config['ollama'] = {
            'enabled': 'false',
            'base_url': 'http://localhost:11434',
            'model': 'llava:7b',
            'timeout': '30'
        }
        
        self.config['ui'] = {
            'overlay_transparency': '0.7',
            'overlay_border_color': '#FF0000',
            'overlay_border_width': '2',
            'always_on_top': 'true',
            'auto_save_position': 'true',
            'font_size': '10',
            'font_family': 'TkDefaultFont'
        }
        
        self.config['translation'] = {
            'source_language': 'auto',
            'target_language': 'de',
            'cache_translations': 'true',
            'max_cache_entries': '100'
        }
        
        self.config['hotkeys'] = {
            'toggle_tabs': 'ctrl+tab',
            'take_screenshot': 'click',
            'copy_result': 'ctrl+c'
        }
        
        self.save()
        
    def save(self):
        """Save current configuration to file"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
            
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
        
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value"""
        return self.config.getboolean(section, key, fallback=fallback)
        
    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value"""
        return self.config.getint(section, key, fallback=fallback)
        
    def getfloat(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value"""
        return self.config.getfloat(section, key, fallback=fallback)
        
    def set(self, section: str, key: str, value: str):
        """Set configuration value"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        
    @property
    def llm_config(self) -> Dict[str, Dict]:
        """Get LLM configuration"""
        config = {
            'gemini-2.5-flash': {
                'endpoint': 'https://generativelanguage.googleapis.com/v1beta/',
                'max_image_size': '4MB',
                'cost_per_1m_tokens': {'input': 0.10, 'output': 0.40}
            },
            'gpt-4.1-mini': {
                'endpoint': 'https://api.openai.com/v1/',
                'max_image_size': '20MB', 
                'cost_per_1m_tokens': {'input': 0.40, 'output': 1.60}
            },
            'gpt-4.1-nano': {
                'endpoint': 'https://api.openai.com/v1/',
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.15, 'output': 0.60}
            }
        }
        
        # Add Ollama as single option if enabled
        if self.getboolean('ollama', 'enabled', False):
            base_url = self.get('ollama', 'base_url', 'http://localhost:11434')
            timeout = self.getint('ollama', 'timeout', 30)
            selected_model = self.get('ollama', 'model', 'llava:7b')
            
            config['ollama'] = {
                'endpoint': f"{base_url}/api/generate",
                'model_name': selected_model,
                'type': 'ollama',
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.0, 'output': 0.0},  # Local = free
                'timeout': timeout
            }
            
        return config
    
    def get_font_config(self) -> Dict[str, Any]:
        """Get font configuration for UI"""
        return {
            'family': self.get('ui', 'font_family', 'TkDefaultFont'),
            'size': self.getint('ui', 'font_size', 10)
        }
    
    def scale_font(self, delta: int):
        """Scale font size by delta"""
        current_size = self.getint('ui', 'font_size', 10)
        new_size = max(8, min(24, current_size + delta))  # Limit between 8-24
        self.set('ui', 'font_size', str(new_size))
        self.save()
        return new_size
        
    def get_ollama_models(self) -> Dict[str, Dict]:
        """Get available Ollama models configuration"""
        base_url = self.get('ollama', 'base_url', 'http://localhost:11434')
        timeout = self.getint('ollama', 'timeout', 30)
        
        return {
            'ollama-llava-7b': {
                'endpoint': f"{base_url}/api/generate",
                'model_name': 'llava:7b',
                'type': 'ollama',
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.0, 'output': 0.0},  # Local = free
                'timeout': timeout
            },
            'ollama-internvl-2b': {
                'endpoint': f"{base_url}/api/generate", 
                'model_name': 'internvl2:2b',
                'type': 'ollama',
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.0, 'output': 0.0},
                'timeout': timeout
            },
            'ollama-qwen2vl-7b': {
                'endpoint': f"{base_url}/api/generate",
                'model_name': 'qwen2-vl:7b', 
                'type': 'ollama',
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.0, 'output': 0.0},
                'timeout': timeout
            },
            'ollama-cogvlm2-19b': {
                'endpoint': f"{base_url}/api/generate",
                'model_name': 'cogvlm2:19b',
                'type': 'ollama', 
                'max_image_size': '20MB',
                'cost_per_1m_tokens': {'input': 0.0, 'output': 0.0},
                'timeout': timeout
            }
        }
        
    @property
    def translation_prompt(self) -> str:
        """Get translation prompt template"""
        return """
Du bist ein Experte für Chinesisch-Deutsch-Übersetzung. 
Analysiere das Bild und:
1. Erkenne automatisch die Quellsprache
2. Übersetze ALLEN erkannten Text ins Deutsche
3. Behalte die ursprüngliche Formatierung bei
4. Bei mehreren Textblöcken: nummeriere sie

Ausgabeformat:
**Erkannte Sprache:** [Sprache]
**Übersetzung:**
[übersetzter Text]
"""

    @property
    def chinese_optimized_prompt(self) -> str:
        """Get Chinese-optimized prompt"""
        return """
Speziell für chinesischen Text:
- Erkenne sowohl vereinfachte als auch traditionelle Zeichen
- Beachte Kontext für mehrdeutige Zeichen
- Übersetze idiomatische Ausdrücke sinngemäß
- Bei technischen Begriffen: gib auch englische Entsprechung an
"""