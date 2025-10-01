# VisoLingua Release Guide

## 🚀 Automated Release Process

The project now has **automated GitHub releases** that trigger when you push a version tag.

## How to Create a Release

### Step 1: Prepare Your Changes

```bash
# Make sure all changes are committed
git add .
git commit -m "Your changes here"
git push
```

### Step 2: Create and Push a Version Tag

```bash
# Create a version tag (e.g., v1.0.0, v1.2.3, v2.0.0-beta)
git tag v1.0.0

# Push the tag to GitHub
git push origin v1.0.0
```

**That's it!** The automated workflow will:
1. ✅ Build the Rust/Tauri Windows binary
2. ✅ Create a portable ZIP package
3. ✅ Create a GitHub Release
4. ✅ Upload the ZIP and EXE files
5. ✅ Generate release notes

## Version Tag Format

Use [Semantic Versioning](https://semver.org/):

```bash
# Stable releases
git tag v1.0.0      # Major release
git tag v1.1.0      # Minor release (new features)
git tag v1.0.1      # Patch release (bug fixes)

# Pre-releases (marked as "pre-release" on GitHub)
git tag v1.0.0-alpha
git tag v1.0.0-beta
git tag v1.0.0-rc1
```

## What Gets Released

### Files Included:
1. **VisoLingua-Windows-vX.X.X.zip** (Complete package)
   - `visolingua.exe` - Main executable
   - `Start-VisoLingua.bat` - Launch script
   - `config/config_sample.toml` - Config template
   - `README.txt` - Quick start guide

2. **visolingua.exe** (Standalone binary)

### Automatic Release Notes Include:
- ✨ Feature highlights
- 🎯 Advantages over Python version
- 📦 Download links
- 🔧 Setup instructions
- 📋 System requirements
- 🔑 API key links

## Monitor Build Progress

1. Go to GitHub → **Actions** tab
2. Find the "Automated Release Build" workflow
3. Watch the build progress live
4. Build typically takes **5-10 minutes**

## After Release

Once the workflow completes:
1. Go to GitHub → **Releases**
2. You'll see your new release with:
   - Version tag
   - Release notes
   - Downloadable files
3. Share the release URL with users!

## Release URL Format

Your releases will be available at:
```
https://github.com/YOUR-USERNAME/VisoLingua/releases/tag/v1.0.0
```

Direct download links:
```
https://github.com/YOUR-USERNAME/VisoLingua/releases/download/v1.0.0/VisoLingua-Windows-v1.0.0.zip
```

## Updating a Release

### To update release notes:
1. Go to Releases → Click your release → "Edit release"
2. Update the description
3. Save

### To replace files (not recommended):
1. Delete the tag and release
2. Create a new tag with same version
3. Push again

**Better approach**: Create a patch version (e.g., v1.0.1)

## Troubleshooting

### Build Failed?
1. Check Actions tab for error details
2. Common issues:
   - Dependencies missing (npm/cargo)
   - Rust compilation errors
   - File path issues

### Tag Already Exists?
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0

# Create new tag
git tag v1.0.0
git push origin v1.0.0
```

### Release Not Appearing?
- Check if workflow completed (Actions tab)
- Verify tag format starts with 'v'
- Check repository permissions

## Manual Release (Fallback)

If automated release fails, use the manual workflow:

```bash
# Go to GitHub → Actions → "Build Rust Windows Binary"
# Click "Run workflow"
# Enter version tag (e.g., v1.0.0)
```

## Version History Example

```bash
git tag v1.0.0     # Initial release
git push origin v1.0.0

git tag v1.0.1     # Bug fix
git push origin v1.0.1

git tag v1.1.0     # New features
git push origin v1.1.0

git tag v2.0.0     # Breaking changes
git push origin v2.0.0
```

## Best Practices

1. **Test before tagging**
   - Build locally first
   - Test the executable
   - Verify features work

2. **Write good commit messages**
   - Release notes reference recent commits
   - Be descriptive

3. **Use semantic versioning**
   - MAJOR: Breaking changes
   - MINOR: New features (backwards compatible)
   - PATCH: Bug fixes

4. **Keep changelog**
   - Document changes between versions
   - Makes it easier to write release notes

## Quick Reference

```bash
# Create release
git tag v1.0.0 && git push origin v1.0.0

# Delete release
git tag -d v1.0.0 && git push origin :refs/tags/v1.0.0

# List all tags
git tag -l

# View release workflow status
# Go to: https://github.com/YOUR-USERNAME/VisoLingua/actions
```

## Summary

**To create a new release:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

**Wait 5-10 minutes, then share:**
```
https://github.com/YOUR-USERNAME/VisoLingua/releases/latest
```

Done! 🎉
