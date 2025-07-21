# VisoLingua Desktop Shortcut Creator (PowerShell)
# More reliable than batch/VBScript on modern Windows

param(
    [string]$ExePath = ".\VisoLingua.exe",
    [string]$ShortcutName = "VisoLingua"
)

Write-Host "Creating VisoLingua desktop shortcut..." -ForegroundColor Green

# Check if executable exists
if (-not (Test-Path $ExePath)) {
    Write-Host "ERROR: VisoLingua.exe not found!" -ForegroundColor Red
    Write-Host "Please make sure VisoLingua.exe is in the current directory." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Get full paths
$ExeFullPath = (Resolve-Path $ExePath).Path
$WorkingDir = Split-Path $ExeFullPath -Parent
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "$ShortcutName.lnk"

try {
    # Create WScript.Shell object
    $WshShell = New-Object -ComObject WScript.Shell
    
    # Create shortcut
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $ExeFullPath
    $Shortcut.WorkingDirectory = $WorkingDir
    $Shortcut.Description = "VisoLingua - Live Translation Overlay Tool"
    
    # Set icon (if available)
    if (Test-Path $ExeFullPath) {
        $Shortcut.IconLocation = $ExeFullPath
    }
    
    # Save shortcut
    $Shortcut.Save()
    
    Write-Host "✅ Desktop shortcut created successfully!" -ForegroundColor Green
    Write-Host "   📂 Location: $ShortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now double-click the VisoLingua icon on your desktop to start the app." -ForegroundColor White
    
} catch {
    Write-Host "❌ Failed to create desktop shortcut: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Manually create a shortcut to:" -ForegroundColor Yellow
    Write-Host "   $ExeFullPath" -ForegroundColor Cyan
}

Write-Host ""
Read-Host "Press Enter to exit"