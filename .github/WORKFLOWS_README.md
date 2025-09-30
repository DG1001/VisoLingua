# GitHub Actions Workflows

This repository has 2 manual build workflows for Windows binaries.

## Available Workflows

### 1. Build Python Windows Binary
**File:** `build-release.yml`
**Builds:** Python + PyInstaller version (~50 MB)

### 2. Build Rust Windows Binary
**File:** `build-rust-windows.yml`
**Builds:** Rust + Tauri version (~8 MB, 80% smaller)

## How to Trigger Builds

Both workflows are **manual only** - they will NOT run automatically on commits.

### Via GitHub Web UI:

1. Go to **Actions** tab in your repository
2. Select the workflow you want to run:
   - "Build Python Windows Binary" (original version)
   - "Build Rust Windows Binary" (new native version)
3. Click **Run workflow** button
4. (Optional) Enter a version tag like `v1.0.0`
5. Click **Run workflow**

### Build Time:
- **Python version**: ~5-8 minutes
- **Rust version**: ~10-15 minutes (first build), ~5 minutes (cached)

### Artifacts:
After completion, download from the workflow run page:
- ZIP file with portable package
- Standalone `.exe` file

## GitHub Actions Limits (Free Tier):

- **Public repos**: Unlimited minutes
- **Private repos**: 2,000 minutes/month

Both workflows are optimized with caching to minimize build times.

## Testing the Builds

Windows builds run natively on GitHub's Windows Server VMs, ensuring:
- ✅ No cross-compilation issues
- ✅ Native Windows libraries (WebView2, Win32 API)
- ✅ Proper installers (MSI for Rust version)

## Comparison

| Feature | Python Version | Rust Version |
|---------|---------------|--------------|
| **Size** | ~50 MB | ~8 MB |
| **Startup** | ~2-3s | ~0.5s |
| **AV Issues** | Common | Rare |
| **Build Time** | 5-8 min | 10-15 min |
| **Features** | Full | Full |