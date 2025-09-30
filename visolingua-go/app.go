package main

import (
	"context"
	"encoding/base64"
	"fmt"
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
	bounds := screenshot.Rect{
		Min: screenshot.Point{X: x, Y: y},
		Max: screenshot.Point{X: x + width, Y: y + height},
	}

	img, err := screenshot.CaptureRect(bounds)
	if err != nil {
		return "", fmt.Errorf("failed to capture screenshot: %w", err)
	}

	// Convert to base64
	var buf bytes.Buffer
	if err := png.Encode(&buf, img); err != nil {
		return "", fmt.Errorf("failed to encode image: %w", err)
	}

	return base64.StdEncoding.EncodeToString(buf.Bytes()), nil
}

// TranslateImage sends the image to LLM for translation
func (a *App) TranslateImage(imageBase64 string) (string, error) {
	return a.translator.TranslateImage(imageBase64)
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