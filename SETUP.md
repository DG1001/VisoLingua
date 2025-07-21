# VisoLingua Setup Guide

## Installation

### 1. Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys Configuration

VisoLingua requires API keys for translation services:

#### Google Gemini API
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Copy the key for configuration

#### OpenAI API (optional)
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new secret key
4. Copy the key for configuration

### 3. First Run Setup

1. Start the application:
```bash
python main.py
```

2. The app will create default configuration files
3. Open Settings (gear icon in result window)
4. Enter your API keys:
   - Gemini API Key: Your Google AI Studio key
   - OpenAI API Key: Your OpenAI key (optional)
5. Select default LLM (recommend: gemini-2.5-flash)
6. Save settings

## Usage

### Basic Workflow
1. **Start**: Run `python main.py`
2. **Position**: Move the transparent overlay over text to translate
3. **Capture**: Click inside the overlay area
4. **View**: Translation appears in result window
5. **Switch**: Double-click title bar or Ctrl+Tab to toggle modes

### Hotkeys
- `Ctrl+Tab`: Switch between capture and result modes
- `Ctrl+C`: Copy translation (in result mode)
- `Esc`: Hide result window

### Tips
- Position overlay carefully over text
- Ensure good contrast for better OCR
- Use caching - identical screenshots won't be re-translated
- Check translation history dropdown for previous results

## Troubleshooting

### Common Issues

**"No display found" error:**
- Ensure you're running on a system with GUI support
- On Linux: Install X11 server or use desktop environment
- On WSL: Install VcXsrv or similar X11 server

**"API key not configured" error:**
- Open Settings and enter valid API keys
- Ensure keys have proper permissions
- Check internet connection

**"Screenshot capture failed":**
- Try repositioning the overlay window
- Ensure the capture area contains visible content
- Check if other applications are blocking screen access

**"Translation failed":**
- Verify API keys are correct
- Check internet connection
- Try switching to different LLM in settings
- Ensure captured area contains readable text

### System Requirements
- Python 3.8+
- GUI environment (X11/Wayland on Linux, native on Windows/macOS)
- Internet connection for API calls
- 4GB+ RAM recommended

### Performance Tips
- Close unused applications to improve screenshot speed
- Use smaller capture areas for faster processing
- Enable caching in settings (default: enabled)
- Consider using Gemini 2.5 Flash for faster/cheaper translations

## Development

### Running Tests
```bash
python test_app.py
```

### File Structure
```
VisoLingua/
├── main.py              # Entry point
├── config/              # Configuration management
├── ui/                  # User interface components
├── core/                # Core functionality (screenshot, translation)
├── utils/               # Utilities and constants
└── requirements.txt     # Dependencies
```

### Contributing
This project is designed for defensive security and language learning purposes only.

## Support

For issues and feature requests, please refer to the project documentation or create an issue in the project repository.