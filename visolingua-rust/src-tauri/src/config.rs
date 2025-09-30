use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConfigData {
    pub llm_provider: String,
    pub gemini_api_key: String,
    pub gemini_model: String,
    pub openai_api_key: String,
    pub openai_model: String,
    pub ollama_url: String,
    pub ollama_model: String,
    pub target_language: String,
    pub overlay_transparency: f64,
}

pub struct Config {
    path: PathBuf,
    data: HashMap<String, HashMap<String, String>>,
}

impl Config {
    /// Load configuration from file or create default
    pub fn load() -> Result<Self> {
        let path = Self::config_path()?;

        // Create config directory if it doesn't exist
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).context("Failed to create config directory")?;
        }

        // Load or create default config
        let data = if path.exists() {
            Self::load_toml(&path)?
        } else {
            let default = Self::default_config();
            Self::save_toml(&path, &default)?;
            default
        };

        Ok(Config { path, data })
    }

    /// Get configuration value
    pub fn get(&self, section: &str, key: &str) -> Option<String> {
        self.data
            .get(section)
            .and_then(|s| s.get(key))
            .cloned()
    }

    /// Get all configuration data
    pub fn get_data(&self) -> ConfigData {
        ConfigData {
            llm_provider: self.get("llm", "provider").unwrap_or_default(),
            gemini_api_key: self.get("api_keys", "gemini").unwrap_or_default(),
            gemini_model: self.get("llm", "gemini_model").unwrap_or_default(),
            openai_api_key: self.get("api_keys", "openai").unwrap_or_default(),
            openai_model: self.get("llm", "openai_model").unwrap_or_default(),
            ollama_url: self.get("llm", "ollama_url").unwrap_or_default(),
            ollama_model: self.get("llm", "ollama_model").unwrap_or_default(),
            target_language: self.get("translation", "target_language").unwrap_or_default(),
            overlay_transparency: self
                .get("ui", "overlay_transparency")
                .and_then(|s| s.parse().ok())
                .unwrap_or(0.3),
        }
    }

    /// Update configuration
    pub fn update(&mut self, config_data: ConfigData) -> Result<()> {
        self.set("llm", "provider", &config_data.llm_provider);
        self.set("api_keys", "gemini", &config_data.gemini_api_key);
        self.set("llm", "gemini_model", &config_data.gemini_model);
        self.set("api_keys", "openai", &config_data.openai_api_key);
        self.set("llm", "openai_model", &config_data.openai_model);
        self.set("llm", "ollama_url", &config_data.ollama_url);
        self.set("llm", "ollama_model", &config_data.ollama_model);
        self.set("translation", "target_language", &config_data.target_language);
        self.set("ui", "overlay_transparency", &config_data.overlay_transparency.to_string());

        Self::save_toml(&self.path, &self.data)
    }

    fn set(&mut self, section: &str, key: &str, value: &str) {
        self.data
            .entry(section.to_string())
            .or_insert_with(HashMap::new)
            .insert(key.to_string(), value.to_string());
    }

    fn config_path() -> Result<PathBuf> {
        let config_dir = dirs::config_dir()
            .context("Failed to get config directory")?
            .join("visolingua");
        Ok(config_dir.join("config.toml"))
    }

    fn default_config() -> HashMap<String, HashMap<String, String>> {
        let mut config = HashMap::new();

        let mut llm = HashMap::new();
        llm.insert("provider".to_string(), "gemini".to_string());
        llm.insert("gemini_model".to_string(), "gemini-2.0-flash-exp".to_string());
        llm.insert("openai_model".to_string(), "gpt-4o-mini".to_string());
        llm.insert("ollama_url".to_string(), "http://localhost:11434".to_string());
        llm.insert("ollama_model".to_string(), "llava".to_string());
        config.insert("llm".to_string(), llm);

        let mut api_keys = HashMap::new();
        api_keys.insert("gemini".to_string(), "".to_string());
        api_keys.insert("openai".to_string(), "".to_string());
        config.insert("api_keys".to_string(), api_keys);

        let mut translation = HashMap::new();
        translation.insert("target_language".to_string(), "German".to_string());
        config.insert("translation".to_string(), translation);

        let mut ui = HashMap::new();
        ui.insert("overlay_transparency".to_string(), "0.3".to_string());
        config.insert("ui".to_string(), ui);

        config
    }

    fn load_toml(path: &PathBuf) -> Result<HashMap<String, HashMap<String, String>>> {
        let contents = fs::read_to_string(path).context("Failed to read config file")?;
        toml::from_str(&contents).context("Failed to parse config file")
    }

    fn save_toml(path: &PathBuf, data: &HashMap<String, HashMap<String, String>>) -> Result<()> {
        let contents = toml::to_string_pretty(data).context("Failed to serialize config")?;
        fs::write(path, contents).context("Failed to write config file")
    }
}