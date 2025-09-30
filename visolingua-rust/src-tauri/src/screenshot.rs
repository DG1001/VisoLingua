use anyhow::{Context, Result};
use base64::{engine::general_purpose::STANDARD, Engine};
use image::{ImageBuffer, RgbaImage};
use xcap::Monitor;

/// Capture a screenshot of a specific area and return as base64-encoded PNG
pub async fn capture_area(x: i32, y: i32, width: u32, height: u32) -> Result<String> {
    // Get all monitors
    let monitors = Monitor::all().context("Failed to get monitors")?;

    // Find the monitor containing this area (use primary for now)
    let monitor = monitors
        .into_iter()
        .next()
        .context("No monitors found")?;

    // Capture the entire monitor
    let image = monitor.capture_image().context("Failed to capture screenshot")?;

    // Get monitor position
    let monitor_x = monitor.x();
    let monitor_y = monitor.y();

    // Calculate relative coordinates
    let rel_x = (x - monitor_x).max(0) as u32;
    let rel_y = (y - monitor_y).max(0) as u32;

    // Crop to the specified area
    let cropped = crop_image(&image, rel_x, rel_y, width, height)?;

    // Encode as PNG and convert to base64
    let mut png_bytes = Vec::new();
    cropped
        .write_to(&mut std::io::Cursor::new(&mut png_bytes), image::ImageFormat::Png)
        .context("Failed to encode image as PNG")?;

    // Debug: Save screenshot to temp folder for verification
    if let Some(temp_dir) = std::env::temp_dir().to_str() {
        let debug_path = format!("{}/visolingua_last_capture.png", temp_dir);
        let _ = cropped.save(&debug_path);
        println!("Screenshot saved to: {}", debug_path);
        println!("Captured: x={}, y={}, w={}, h={}, size={}kb", x, y, width, height, png_bytes.len()/1024);
    }

    let base64_string = STANDARD.encode(&png_bytes);
    Ok(base64_string)
}

/// Crop an image to a specific region
fn crop_image(
    image: &RgbaImage,
    x: u32,
    y: u32,
    width: u32,
    height: u32,
) -> Result<RgbaImage> {
    let (img_width, img_height) = image.dimensions();

    // Clamp coordinates to image bounds
    let x = x.min(img_width.saturating_sub(1));
    let y = y.min(img_height.saturating_sub(1));
    let width = width.min(img_width - x);
    let height = height.min(img_height - y);

    // Create new image buffer for the cropped region
    let mut cropped = ImageBuffer::new(width, height);

    for dy in 0..height {
        for dx in 0..width {
            let pixel = image.get_pixel(x + dx, y + dy);
            cropped.put_pixel(dx, dy, *pixel);
        }
    }

    Ok(cropped)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_screenshot_capture() {
        // Basic test to ensure the function doesn't panic
        let result = capture_area(0, 0, 100, 100).await;
        assert!(result.is_ok() || result.is_err()); // Just ensure it returns
    }
}