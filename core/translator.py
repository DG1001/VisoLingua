"""
LLM translation integration
"""

import asyncio
import aiohttp
import base64
import json
import time
from typing import Dict, Any, Optional
from PIL import Image
import io

from core.screenshot import ScreenCapture


class Translator:
    """Handles LLM-based translation"""
    
    def __init__(self, settings):
        self.settings = settings
        self.screen_capture = ScreenCapture()
        self.translation_cache = {}
        
    async def translate_image(self, image: Image.Image) -> str:
        """
        Translate text in image using configured LLM
        
        Args:
            image: PIL Image containing text to translate
            
        Returns:
            Translation result as string
        """
        start_time = time.time()
        
        try:
            # Get current LLM configuration
            llm_name = self.settings.get('api', 'default_llm', 'gemini-2.5-flash')
            llm_config = self.settings.llm_config.get(llm_name)
            
            if not llm_config:
                raise ValueError(f"Unknown LLM: {llm_name}")
                
            # Check cache
            image_hash = self.screen_capture._get_image_hash(image)
            if image_hash in self.translation_cache:
                return self.translation_cache[image_hash]
                
            # Optimize image for API
            max_size = llm_config['max_image_size']
            optimized_image_data = self.screen_capture.optimize_image_for_llm(image, max_size)
            
            # Translate using appropriate API
            if llm_name.startswith('gemini'):
                result = await self._translate_with_gemini(optimized_image_data)
            elif llm_name.startswith('gpt'):
                result = await self._translate_with_openai(optimized_image_data, llm_name)
            elif llm_name == 'ollama':
                result = await self._translate_with_ollama(optimized_image_data, llm_name)
            else:
                raise ValueError(f"Unsupported LLM: {llm_name}")
                
            # Cache result
            if self.settings.getboolean('translation', 'cache_translations', True):
                self.translation_cache[image_hash] = result
                self._cleanup_cache()
                
            processing_time = time.time() - start_time
            print(f"Translation completed in {processing_time:.2f}s")
            
            return result
            
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
            
    async def _translate_with_gemini(self, image_data: bytes) -> str:
        """Translate using Google Gemini API"""
        api_key = self.settings.get('api', 'gemini_api_key')
        if not api_key:
            raise ValueError("Gemini API key not configured")
            
        # Prepare request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
        
        # Encode image
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build prompt
        prompt = self.settings.translation_prompt
        if self._contains_chinese_chars(image_data):
            prompt += "\n" + self.settings.chinese_optimized_prompt
            
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_b64
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Gemini API error ({response.status}): {error_text}")
                    
                result = await response.json()
                
                if 'candidates' not in result or not result['candidates']:
                    raise Exception("No translation result from Gemini")
                    
                return result['candidates'][0]['content']['parts'][0]['text']
                
    async def _translate_with_openai(self, image_data: bytes, model_name: str) -> str:
        """Translate using OpenAI API"""
        api_key = self.settings.get('api', 'openai_api_key')
        if not api_key:
            raise ValueError("OpenAI API key not configured")
            
        # Map model name
        model_mapping = {
            'gpt-4.1-mini': 'gpt-4o-mini',
            'gpt-4.1-nano': 'gpt-4o-mini'  # Using mini as nano doesn't exist yet
        }
        
        api_model = model_mapping.get(model_name, 'gpt-4o-mini')
        
        # Prepare request
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Encode image
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build prompt
        prompt = self.settings.translation_prompt
        if self._contains_chinese_chars(image_data):
            prompt += "\n" + self.settings.chinese_optimized_prompt
            
        payload = {
            "model": api_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2048,
            "temperature": 0.1
        }
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error ({response.status}): {error_text}")
                    
                result = await response.json()
                
                if 'choices' not in result or not result['choices']:
                    raise Exception("No translation result from OpenAI")
                    
                return result['choices'][0]['message']['content']
                
    def _contains_chinese_chars(self, image_data: bytes) -> bool:
        """
        Heuristic to detect if image might contain Chinese characters
        This is a simple implementation - in practice, you might want to use OCR
        """
        # For now, always assume it might contain Chinese for better prompt handling
        return True
        
    def _cleanup_cache(self):
        """Clean up translation cache if it gets too large"""
        max_entries = self.settings.getint('translation', 'max_cache_entries', 100)
        
        if len(self.translation_cache) > max_entries:
            # Remove oldest entries (simple FIFO)
            entries_to_remove = len(self.translation_cache) - max_entries + 10
            keys_to_remove = list(self.translation_cache.keys())[:entries_to_remove]
            
            for key in keys_to_remove:
                del self.translation_cache[key]
                
    def clear_cache(self):
        """Clear translation cache"""
        self.translation_cache.clear()
        
    async def test_api_connection(self, llm_name: str = None) -> Dict[str, Any]:
        """Test API connection for specified LLM"""
        if not llm_name:
            llm_name = self.settings.get('api', 'default_llm', 'gemini-2.5-flash')
            
        try:
            # Create a small test image
            test_img = Image.new('RGB', (100, 50), color='white')
            
            # Try translation
            start_time = time.time()
            result = await self.translate_image(test_img)
            end_time = time.time()
            
            return {
                'success': True,
                'llm': llm_name,
                'response_time': end_time - start_time,
                'result': result[:100] + "..." if len(result) > 100 else result
            }
            
        except Exception as e:
            return {
                'success': False,
                'llm': llm_name,
                'error': str(e)
            }
            
    def get_api_status(self) -> Dict[str, Any]:
        """Get API configuration status"""
        status = {}
        
        for llm_name in self.settings.llm_config.keys():
            if llm_name.startswith('gemini'):
                key_configured = bool(self.settings.get('api', 'gemini_api_key'))
            elif llm_name.startswith('gpt'):
                key_configured = bool(self.settings.get('api', 'openai_api_key'))
            elif llm_name == 'ollama':
                key_configured = self.settings.getboolean('ollama', 'enabled', False)
            else:
                key_configured = False
                
            status[llm_name] = {
                'key_configured': key_configured,
                'config': self.settings.llm_config[llm_name]
            }
            
        return status
        
    async def _translate_with_ollama(self, image_data: bytes, llm_name: str) -> str:
        """Translate using Ollama local API"""
        if not self.settings.getboolean('ollama', 'enabled', False):
            raise ValueError("Ollama not enabled in configuration")
            
        # Get Ollama configuration
        llm_config = self.settings.llm_config.get(llm_name)
        if not llm_config:
            raise ValueError(f"Unknown Ollama model: {llm_name}")
            
        base_url = self.settings.get('ollama', 'base_url', 'http://localhost:11434')
        model_name = llm_config['model_name']
        timeout_seconds = self.settings.getint('ollama', 'timeout', 30)
        
        # Encode image to base64
        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        # Build prompt - Ollama vision models work differently
        prompt = self.settings.translation_prompt
        if self._contains_chinese_chars(image_data):
            prompt += "\n" + self.settings.chinese_optimized_prompt
            
        # Ollama API payload
        payload = {
            "model": model_name,
            "prompt": prompt,
            "images": [image_b64],
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 1000
            }
        }
        
        # Make request to Ollama
        timeout = aiohttp.ClientTimeout(total=timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                async with session.post(f"{base_url}/api/generate", json=payload) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error {response.status}: {error_text}")
                        
                    result = await response.json()
                    
                    if 'response' not in result:
                        raise Exception(f"Invalid Ollama response format: {result}")
                        
                    translation = result['response'].strip()
                    if not translation:
                        raise Exception("Empty translation received from Ollama")
                        
                    return translation
                    
            except asyncio.TimeoutError:
                raise Exception(f"Ollama request timed out after {timeout_seconds}s")
            except aiohttp.ClientError as e:
                raise Exception(f"Ollama connection error: {str(e)}")
                
    async def test_ollama_connection(self) -> Dict[str, Any]:
        """Test Ollama server connection"""
        if not self.settings.getboolean('ollama', 'enabled', False):
            return {
                'success': False,
                'error': 'Ollama not enabled in configuration'
            }
            
        base_url = self.settings.get('ollama', 'base_url', 'http://localhost:11434')
        timeout_seconds = self.settings.getint('ollama', 'timeout', 30)
        
        try:
            timeout = aiohttp.ClientTimeout(total=5)  # Quick test
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Test server availability
                async with session.get(f"{base_url}/api/tags") as response:
                    if response.status == 200:
                        models = await response.json()
                        available_models = [m['name'] for m in models.get('models', [])]
                        
                        return {
                            'success': True,
                            'server_url': base_url,
                            'available_models': available_models,
                            'configured_models': list(self.settings.get_ollama_models().keys())
                        }
                    else:
                        return {
                            'success': False,
                            'error': f'Server returned status {response.status}'
                        }
                        
        except asyncio.TimeoutError:
            return {
                'success': False,
                'error': 'Connection timeout - is Ollama running?'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Connection failed: {str(e)}'
            }