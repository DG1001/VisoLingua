// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod config;
mod screenshot;
mod translator;

use config::Config;
use screenshot::capture_area;
use tauri::{Manager, State, Window};
use std::sync::Mutex;

pub struct AppState {
    config: Mutex<Config>,
}

#[tauri::command]
async fn capture_screenshot(
    _window: Window,
    x: i32,
    y: i32,
    width: u32,
    height: u32,
) -> Result<String, String> {
    capture_area(x, y, width, height)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn translate_image(
    state: State<'_, AppState>,
    image_base64: String,
) -> Result<String, String> {
    let config_data = {
        let config = state.config.lock().unwrap();
        config.get_data()
    };
    translator::translate_image_with_data(&config_data, &image_base64)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
async fn ask_ai(
    state: State<'_, AppState>,
    question: String,
    context: String,
) -> Result<String, String> {
    let config_data = {
        let config = state.config.lock().unwrap();
        config.get_data()
    };
    translator::ask_ai_with_data(&config_data, &question, &context)
        .await
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn get_config(state: State<'_, AppState>) -> Result<config::ConfigData, String> {
    let config = state.config.lock().unwrap();
    Ok(config.get_data())
}

#[tauri::command]
fn save_config(
    state: State<'_, AppState>,
    config_data: config::ConfigData,
) -> Result<(), String> {
    let mut config = state.config.lock().unwrap();
    config
        .update(config_data)
        .map_err(|e| e.to_string())
}

#[tauri::command]
fn show_result_window(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(window) = app.get_webview_window("result") {
        window.show().map_err(|e| e.to_string())?;
        window.set_focus().map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
fn hide_result_window(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(window) = app.get_webview_window("result") {
        window.hide().map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
fn show_overlay_window(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(window) = app.get_webview_window("overlay") {
        window.show().map_err(|e| e.to_string())?;
        window.set_focus().map_err(|e| e.to_string())?;
    }
    Ok(())
}

fn main() {
    // Load configuration
    let config = Config::load().expect("Failed to load configuration");

    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(AppState {
            config: Mutex::new(config),
        })
        .invoke_handler(tauri::generate_handler![
            capture_screenshot,
            translate_image,
            ask_ai,
            get_config,
            save_config,
            show_result_window,
            hide_result_window,
            show_overlay_window,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}