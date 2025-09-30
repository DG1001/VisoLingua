# VisoLingua Windows Build Script
# Run this script on a Windows machine with PowerShell

Write-Host "🚀 VisoLingua Windows Build Script" -ForegroundColor Cyan
Write-Host ""

# Check if Rust is installed
Write-Host "Checking prerequisites..." -ForegroundColor Yellow
if (!(Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Rust not found. Installing Rust..." -ForegroundColor Red
    Write-Host "Please visit https://rustup.rs/ and install Rust, then run this script again."
    exit 1
} else {
    $rustVersion = cargo --version
    Write-Host "✅ Rust found: $rustVersion" -ForegroundColor Green
}

# Check if Node.js is installed
if (!(Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js not found. Installing..." -ForegroundColor Red
    Write-Host "Please visit https://nodejs.org/ and install Node.js, then run this script again."
    exit 1
} else {
    $nodeVersion = node --version
    Write-Host "✅ Node.js found: $nodeVersion" -ForegroundColor Green
}

# Check WebView2
$webview2Path = "C:\Program Files (x86)\Microsoft\EdgeWebView\Application"
if (Test-Path $webview2Path) {
    Write-Host "✅ WebView2 Runtime found" -ForegroundColor Green
} else {
    Write-Host "⚠️  WebView2 Runtime not detected" -ForegroundColor Yellow
    Write-Host "   The app will still build, but may not run on systems without WebView2" -ForegroundColor Yellow
    Write-Host "   Download: https://go.microsoft.com/fwlink/p/?LinkId=2124703" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📦 Installing npm dependencies..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ npm install failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔨 Building Tauri application for Windows..." -ForegroundColor Yellow
Write-Host "   This may take 5-10 minutes on first build..." -ForegroundColor Gray
npm run tauri build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Build successful!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Build artifacts:" -ForegroundColor Cyan
Write-Host "   Executable: src-tauri\target\release\visolingua.exe" -ForegroundColor White

# Check for MSI installer
$msiPath = "src-tauri\target\release\bundle\msi\*.msi"
if (Test-Path $msiPath) {
    $msiFile = Get-ChildItem $msiPath | Select-Object -First 1
    Write-Host "   Installer:  $($msiFile.FullName)" -ForegroundColor White
}

# Display file sizes
$exePath = "src-tauri\target\release\visolingua.exe"
if (Test-Path $exePath) {
    $exeSize = (Get-Item $exePath).Length / 1MB
    Write-Host ""
    Write-Host "📊 Binary size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Done! You can now run: src-tauri\target\release\visolingua.exe" -ForegroundColor Green