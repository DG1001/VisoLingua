package main

import (
	"os"
	"path/filepath"

	"github.com/BurntSushi/toml"
)

type Config struct {
	LLM         LLMConfig         `toml:"llm"`
	APIKeys     APIKeysConfig     `toml:"api_keys"`
	Translation TranslationConfig `toml:"translation"`
	UI          UIConfig          `toml:"ui"`
}

type LLMConfig struct {
	Provider    string `toml:"provider"`
	GeminiModel string `toml:"gemini_model"`
	OpenAIModel string `toml:"openai_model"`
	OllamaURL   string `toml:"ollama_url"`
	OllamaModel string `toml:"ollama_model"`
}

type APIKeysConfig struct {
	Gemini string `toml:"gemini"`
	OpenAI string `toml:"openai"`
}

type TranslationConfig struct {
	TargetLanguage string `toml:"target_language"`
}

type UIConfig struct {
	Transparency float64 `toml:"transparency"`
}

type ConfigData struct {
	LLMProvider    string  `json:"llm_provider"`
	GeminiAPIKey   string  `json:"gemini_api_key"`
	GeminiModel    string  `json:"gemini_model"`
	OpenAIAPIKey   string  `json:"openai_api_key"`
	OpenAIModel    string  `json:"openai_model"`
	OllamaURL      string  `json:"ollama_url"`
	OllamaModel    string  `json:"ollama_model"`
	TargetLanguage string  `json:"target_language"`
	Transparency   float64 `json:"transparency"`
}

// LoadConfig loads configuration from file or creates default
func LoadConfig() (*Config, error) {
	configPath := getConfigPath()

	// Create default config if doesn't exist
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		config := defaultConfig()
		if err := config.Save(); err != nil {
			return nil, err
		}
		return config, nil
	}

	var config Config
	if _, err := toml.DecodeFile(configPath, &config); err != nil {
		return nil, err
	}

	return &config, nil
}

// Save saves the configuration to file
func (c *Config) Save() error {
	configPath := getConfigPath()

	// Ensure directory exists
	dir := filepath.Dir(configPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return err
	}

	file, err := os.Create(configPath)
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := toml.NewEncoder(file)
	return encoder.Encode(c)
}

func getConfigPath() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".config", "visolingua", "config.toml")
}

func defaultConfig() *Config {
	return &Config{
		LLM: LLMConfig{
			Provider:    "gemini",
			GeminiModel: "gemini-2.0-flash-exp",
			OpenAIModel: "gpt-4o-mini",
			OllamaURL:   "http://localhost:11434",
			OllamaModel: "llava",
		},
		APIKeys: APIKeysConfig{
			Gemini: "",
			OpenAI: "",
		},
		Translation: TranslationConfig{
			TargetLanguage: "German",
		},
		UI: UIConfig{
			Transparency: 0.3,
		},
	}
}