use crate::config::ConfigData;
use anyhow::{Context, Result};
use reqwest::Client;
use serde_json::{json, Value};

/// Translate an image using the configured LLM
pub async fn translate_image_with_data(config: &ConfigData, image_base64: &str) -> Result<String> {
    let llm_provider = &config.llm_provider;
    let target_language = &config.target_language;

    match llm_provider.as_str() {
        "gemini" => translate_with_gemini(config, image_base64, target_language).await,
        "openai" => translate_with_openai(config, image_base64, target_language).await,
        "ollama" => translate_with_ollama(config, image_base64, target_language).await,
        _ => anyhow::bail!("Unknown LLM provider: {}", llm_provider),
    }
}

/// Ask AI a question about the translation
pub async fn ask_ai_with_data(config: &ConfigData, question: &str, context: &str) -> Result<String> {
    let llm_provider = &config.llm_provider;

    let prompt = format!(
        "Based on this translation:\n\n{}\n\nUser question: {}\n\nProvide a helpful answer.",
        context, question
    );

    match llm_provider.as_str() {
        "gemini" => ask_gemini(config, &prompt).await,
        "openai" => ask_openai(config, &prompt).await,
        "ollama" => ask_ollama(config, &prompt).await,
        _ => anyhow::bail!("Unknown LLM provider: {}", llm_provider),
    }
}

async fn translate_with_gemini(config: &ConfigData, image_base64: &str, target_lang: &str) -> Result<String> {
    let api_key = &config.gemini_api_key;
    if api_key.is_empty() {
        anyhow::bail!("Gemini API key not configured");
    }
    let model = &config.gemini_model;

    let client = Client::new();
    let url = format!(
        "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}",
        model, api_key
    );

    let body = json!({
        "contents": [{
            "parts": [
                {
                    "text": format!(
                        "Translate the text in this image to {}. Only provide the translation, no explanations.",
                        target_lang
                    )
                },
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": image_base64
                    }
                }
            ]
        }]
    });

    let response = client
        .post(&url)
        .json(&body)
        .send()
        .await
        .context("Failed to send request to Gemini")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse Gemini response")?;

    extract_gemini_text(&json)
}

async fn translate_with_openai(config: &ConfigData, image_base64: &str, target_lang: &str) -> Result<String> {
    let api_key = &config.openai_api_key;
    if api_key.is_empty() {
        anyhow::bail!("OpenAI API key not configured");
    }
    let model = &config.openai_model;

    let client = Client::new();
    let url = "https://api.openai.com/v1/chat/completions";

    let body = json!({
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": format!(
                        "Translate the text in this image to {}. Only provide the translation, no explanations.",
                        target_lang
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": format!("data:image/png;base64,{}", image_base64)
                    }
                }
            ]
        }],
        "max_tokens": 1000
    });

    let response = client
        .post(url)
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&body)
        .send()
        .await
        .context("Failed to send request to OpenAI")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse OpenAI response")?;

    extract_openai_text(&json)
}

async fn translate_with_ollama(config: &ConfigData, image_base64: &str, target_lang: &str) -> Result<String> {
    let base_url = &config.ollama_url;
    let model = &config.ollama_model;

    let client = Client::new();
    let url = format!("{}/api/generate", base_url);

    let body = json!({
        "model": model,
        "prompt": format!(
            "Translate the text in this image to {}. Only provide the translation, no explanations.",
            target_lang
        ),
        "images": [image_base64],
        "stream": false
    });

    let response = client
        .post(&url)
        .json(&body)
        .send()
        .await
        .context("Failed to send request to Ollama")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse Ollama response")?;

    json["response"]
        .as_str()
        .map(|s| s.to_string())
        .context("Invalid Ollama response")
}

async fn ask_gemini(config: &ConfigData, prompt: &str) -> Result<String> {
    let api_key = &config.gemini_api_key;
    if api_key.is_empty() {
        anyhow::bail!("Gemini API key not configured");
    }
    let model = &config.gemini_model;

    let client = Client::new();
    let url = format!(
        "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}",
        model, api_key
    );

    let body = json!({
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    });

    let response = client
        .post(&url)
        .json(&body)
        .send()
        .await
        .context("Failed to send request to Gemini")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse Gemini response")?;

    extract_gemini_text(&json)
}

async fn ask_openai(config: &ConfigData, prompt: &str) -> Result<String> {
    let api_key = &config.openai_api_key;
    if api_key.is_empty() {
        anyhow::bail!("OpenAI API key not configured");
    }
    let model = &config.openai_model;

    let client = Client::new();
    let url = "https://api.openai.com/v1/chat/completions";

    let body = json!({
        "model": model,
        "messages": [{
            "role": "user",
            "content": prompt
        }],
        "max_tokens": 1000
    });

    let response = client
        .post(url)
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&body)
        .send()
        .await
        .context("Failed to send request to OpenAI")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse OpenAI response")?;

    extract_openai_text(&json)
}

async fn ask_ollama(config: &ConfigData, prompt: &str) -> Result<String> {
    let base_url = &config.ollama_url;
    let model = &config.ollama_model;

    let client = Client::new();
    let url = format!("{}/api/generate", base_url);

    let body = json!({
        "model": model,
        "prompt": prompt,
        "stream": false
    });

    let response = client
        .post(&url)
        .json(&body)
        .send()
        .await
        .context("Failed to send request to Ollama")?;

    let json: Value = response
        .json()
        .await
        .context("Failed to parse Ollama response")?;

    json["response"]
        .as_str()
        .map(|s| s.to_string())
        .context("Invalid Ollama response")
}

fn extract_gemini_text(json: &Value) -> Result<String> {
    json["candidates"][0]["content"]["parts"][0]["text"]
        .as_str()
        .map(|s| s.to_string())
        .context("Invalid Gemini response format")
}

fn extract_openai_text(json: &Value) -> Result<String> {
    json["choices"][0]["message"]["content"]
        .as_str()
        .map(|s| s.to_string())
        .context("Invalid OpenAI response format")
}