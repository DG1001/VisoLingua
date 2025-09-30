package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"image"
	"image/png"
	"bytes"

	"github.com/kbinani/screenshot"
	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx        context.Context
	config     *Config
	translator *Translator
}

// NewApp creates a new App application struct
func NewApp() *App {
	config, _ := LoadConfig()
	return &App{
		config:     config,
		translator: NewTranslator(config),
	}
}

// startup is called when the app starts
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

// CaptureScreenshot captures a screenshot of the specified area
func (a *App) CaptureScreenshot(x, y, width, height int) (string, error) {
	fmt.Printf("CaptureScreenshot called: x=%d, y=%d, w=%d, h=%d\n", x, y, width, height)

	bounds := image.Rect(x, y, x+width, y+height)
	fmt.Printf("Capture bounds: %v\n", bounds)

	img, err := screenshot.CaptureRect(bounds)
	if err != nil {
		fmt.Printf("Screenshot capture error: %v\n", err)
		return "", fmt.Errorf("failed to capture screenshot: %w", err)
	}

	fmt.Printf("Screenshot captured, size: %dx%d\n", img.Bounds().Dx(), img.Bounds().Dy())

	// Convert to base64
	var buf bytes.Buffer
	if err := png.Encode(&buf, img); err != nil {
		fmt.Printf("PNG encode error: %v\n", err)
		return "", fmt.Errorf("failed to encode image: %w", err)
	}

	fmt.Printf("Base64 encoded, length: %d bytes\n", buf.Len())
	return base64.StdEncoding.EncodeToString(buf.Bytes()), nil
}

// TranslateImage sends the image to LLM for translation
func (a *App) TranslateImage(imageBase64 string) (string, error) {
	fmt.Printf("TranslateImage called, base64 length: %d\n", len(imageBase64))
	result, err := a.translator.TranslateImage(imageBase64)
	if err != nil {
		fmt.Printf("Translation error: %v\n", err)
		return "", err
	}
	fmt.Printf("Translation result: %s\n", result)
	return result, nil
}

// AskAI asks a question about the translation
func (a *App) AskAI(question, context string) (string, error) {
	return a.translator.AskAI(question, context)
}

// GetConfig returns the current configuration
func (a *App) GetConfig() (*ConfigData, error) {
	return &ConfigData{
		LLMProvider:     a.config.LLM.Provider,
		GeminiAPIKey:    a.config.APIKeys.Gemini,
		GeminiModel:     a.config.LLM.GeminiModel,
		OpenAIAPIKey:    a.config.APIKeys.OpenAI,
		OpenAIModel:     a.config.LLM.OpenAIModel,
		OllamaURL:       a.config.LLM.OllamaURL,
		OllamaModel:     a.config.LLM.OllamaModel,
		TargetLanguage:  a.config.Translation.TargetLanguage,
		Transparency:    a.config.UI.Transparency,
	}, nil
}

// SaveConfig saves the configuration
func (a *App) SaveConfig(config ConfigData) error {
	a.config.LLM.Provider = config.LLMProvider
	a.config.APIKeys.Gemini = config.GeminiAPIKey
	a.config.LLM.GeminiModel = config.GeminiModel
	a.config.APIKeys.OpenAI = config.OpenAIAPIKey
	a.config.LLM.OpenAIModel = config.OpenAIModel
	a.config.LLM.OllamaURL = config.OllamaURL
	a.config.LLM.OllamaModel = config.OllamaModel
	a.config.Translation.TargetLanguage = config.TargetLanguage
	a.config.UI.Transparency = config.Transparency

	return a.config.Save()
}

// ShowResultWindow opens the result window
func (a *App) ShowResultWindow() {
	runtime.WindowShow(a.ctx)
}

// GetWindowBounds returns the current window position and size
func (a *App) GetWindowBounds() (map[string]int, error) {
	// Get window position
	x, y := runtime.WindowGetPosition(a.ctx)
	fmt.Printf("WindowGetPosition returned: x=%d, y=%d\n", x, y)

	// Get window size
	width, height := runtime.WindowGetSize(a.ctx)
	fmt.Printf("WindowGetSize returned: width=%d, height=%d\n", width, height)

	result := map[string]int{
		"x":      x,
		"y":      y,
		"width":  width,
		"height": height,
	}
	fmt.Printf("Returning bounds: %v\n", result)

	return result, nil
}