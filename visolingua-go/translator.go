package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Translator struct {
	config *Config
	client *http.Client
}

func NewTranslator(config *Config) *Translator {
	return &Translator{
		config: config,
		client: &http.Client{},
	}
}

// TranslateImage translates text in an image
func (t *Translator) TranslateImage(imageBase64 string) (string, error) {
	switch t.config.LLM.Provider {
	case "gemini":
		return t.translateWithGemini(imageBase64)
	case "openai":
		return t.translateWithOpenAI(imageBase64)
	case "ollama":
		return t.translateWithOllama(imageBase64)
	default:
		return "", fmt.Errorf("unknown LLM provider: %s", t.config.LLM.Provider)
	}
}

// AskAI asks a question about the translation
func (t *Translator) AskAI(question, context string) (string, error) {
	prompt := fmt.Sprintf("Based on this translation:\n\n%s\n\nUser question: %s\n\nProvide a helpful answer.", context, question)

	switch t.config.LLM.Provider {
	case "gemini":
		return t.askGemini(prompt)
	case "openai":
		return t.askOpenAI(prompt)
	case "ollama":
		return t.askOllama(prompt)
	default:
		return "", fmt.Errorf("unknown LLM provider: %s", t.config.LLM.Provider)
	}
}

func (t *Translator) translateWithGemini(imageBase64 string) (string, error) {
	if t.config.APIKeys.Gemini == "" {
		return "", fmt.Errorf("Gemini API key not configured")
	}

	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s",
		t.config.LLM.GeminiModel, t.config.APIKeys.Gemini)

	payload := map[string]interface{}{
		"contents": []map[string]interface{}{
			{
				"parts": []map[string]interface{}{
					{
						"text": fmt.Sprintf("Translate the text in this image to %s. Only provide the translation, no explanations.", t.config.Translation.TargetLanguage),
					},
					{
						"inline_data": map[string]string{
							"mime_type": "image/png",
							"data":      imageBase64,
						},
					},
				},
			},
		},
	}

	body, _ := json.Marshal(payload)
	fmt.Printf("Gemini request URL: %s\n", url)

	resp, err := t.client.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		fmt.Printf("Gemini request error: %v\n", err)
		return "", fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Read response body
	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Failed to read response: %v\n", err)
		return "", fmt.Errorf("failed to read response: %w", err)
	}

	fmt.Printf("Gemini response status: %d\n", resp.StatusCode)
	fmt.Printf("Gemini response: %s\n", string(responseBody))

	if resp.StatusCode != 200 {
		return "", fmt.Errorf("API error (%d): %s", resp.StatusCode, string(responseBody))
	}

	var result map[string]interface{}
	if err := json.Unmarshal(responseBody, &result); err != nil {
		fmt.Printf("JSON parse error: %v\n", err)
		return "", fmt.Errorf("failed to parse JSON: %w", err)
	}

	// Extract text from response with error checking
	candidates, ok := result["candidates"].([]interface{})
	if !ok || len(candidates) == 0 {
		return "", fmt.Errorf("no candidates in response")
	}

	candidate0, ok := candidates[0].(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("invalid candidate format")
	}

	content, ok := candidate0["content"].(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("invalid content format")
	}

	parts, ok := content["parts"].([]interface{})
	if !ok || len(parts) == 0 {
		return "", fmt.Errorf("no parts in content")
	}

	part0, ok := parts[0].(map[string]interface{})
	if !ok {
		return "", fmt.Errorf("invalid part format")
	}

	text, ok := part0["text"].(string)
	if !ok {
		return "", fmt.Errorf("no text in part")
	}

	return text, nil
}

func (t *Translator) translateWithOpenAI(imageBase64 string) (string, error) {
	if t.config.APIKeys.OpenAI == "" {
		return "", fmt.Errorf("OpenAI API key not configured")
	}

	url := "https://api.openai.com/v1/chat/completions"

	payload := map[string]interface{}{
		"model": t.config.LLM.OpenAIModel,
		"messages": []map[string]interface{}{
			{
				"role": "user",
				"content": []map[string]interface{}{
					{
						"type": "text",
						"text": fmt.Sprintf("Translate the text in this image to %s. Only provide the translation, no explanations.", t.config.Translation.TargetLanguage),
					},
					{
						"type": "image_url",
						"image_url": map[string]string{
							"url": fmt.Sprintf("data:image/png;base64,%s", imageBase64),
						},
					},
				},
			},
		},
		"max_tokens": 1000,
	}

	body, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", t.config.APIKeys.OpenAI))

	resp, err := t.client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}

	choices := result["choices"].([]interface{})
	message := choices[0].(map[string]interface{})["message"].(map[string]interface{})
	return message["content"].(string), nil
}

func (t *Translator) translateWithOllama(imageBase64 string) (string, error) {
	url := fmt.Sprintf("%s/api/generate", t.config.LLM.OllamaURL)

	payload := map[string]interface{}{
		"model":  t.config.LLM.OllamaModel,
		"prompt": fmt.Sprintf("Translate the text in this image to %s. Only provide the translation, no explanations.", t.config.Translation.TargetLanguage),
		"images": []string{imageBase64},
		"stream": false,
	}

	body, _ := json.Marshal(payload)
	resp, err := t.client.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return "", err
	}

	return result["response"].(string), nil
}

func (t *Translator) askGemini(prompt string) (string, error) {
	if t.config.APIKeys.Gemini == "" {
		return "", fmt.Errorf("Gemini API key not configured")
	}

	url := fmt.Sprintf("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s",
		t.config.LLM.GeminiModel, t.config.APIKeys.Gemini)

	payload := map[string]interface{}{
		"contents": []map[string]interface{}{
			{
				"parts": []map[string]interface{}{
					{"text": prompt},
				},
			},
		},
	}

	body, _ := json.Marshal(payload)
	resp, err := t.client.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	var result map[string]interface{}
	json.Unmarshal(respBody, &result)

	candidates := result["candidates"].([]interface{})
	content := candidates[0].(map[string]interface{})["content"].(map[string]interface{})
	parts := content["parts"].([]interface{})
	return parts[0].(map[string]interface{})["text"].(string), nil
}

func (t *Translator) askOpenAI(prompt string) (string, error) {
	if t.config.APIKeys.OpenAI == "" {
		return "", fmt.Errorf("OpenAI API key not configured")
	}

	url := "https://api.openai.com/v1/chat/completions"

	payload := map[string]interface{}{
		"model": t.config.LLM.OpenAIModel,
		"messages": []map[string]interface{}{
			{
				"role":    "user",
				"content": prompt,
			},
		},
		"max_tokens": 1000,
	}

	body, _ := json.Marshal(payload)
	req, _ := http.NewRequest("POST", url, bytes.NewBuffer(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", t.config.APIKeys.OpenAI))

	resp, err := t.client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	choices := result["choices"].([]interface{})
	message := choices[0].(map[string]interface{})["message"].(map[string]interface{})
	return message["content"].(string), nil
}

func (t *Translator) askOllama(prompt string) (string, error) {
	url := fmt.Sprintf("%s/api/generate", t.config.LLM.OllamaURL)

	payload := map[string]interface{}{
		"model":  t.config.LLM.OllamaModel,
		"prompt": prompt,
		"stream": false,
	}

	body, _ := json.Marshal(payload)
	resp, err := t.client.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)

	return result["response"].(string), nil
}