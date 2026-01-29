# Building for macOS

Complete guide for building PostgreSQL Database Manager on macOS.

## 🚀 Quick Start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Convert icon (optional but recommended)
chmod +x convert_icon_mac.sh
./convert_icon_mac.sh

# Build executable
python3 build_exe.py
```

## 📋 Prerequisites

### 1. Install Python 3.7+

```bash
# Check Python version
python3 --version

# Install via Homebrew (if not installed)
brew install python@3.11
```

### 2. Install PostgreSQL

```bash
# Install via Homebrew
brew install postgresql@15

# Or download from postgresql.org
# https://www.postgresql.org/download/macosx/

# Verify installation
which psql
which pg_dump
which pg_restore
```

### 3. Install Dependencies

```bash
# Navigate to project directory
cd /path/to/pg-ui

# Install Python packages
pip3 install -r requirements.txt
pip3 install pyinstaller
```

### 4. Install UPX (Optional - for compression)

```bash
# Install via Homebrew
brew install upx

# Verify installation
upx --version
```

## 🎨 Icon Conversion

macOS uses `.icns` format instead of Windows `.ico` format.

### Method 1: Automated Script (Recommended)

```bash
# Make script executable
chmod +x convert_icon_mac.sh

# Run conversion
./convert_icon_mac.sh
```

### Method 2: Manual Conversion with sips

```bash
# Convert .ico to .icns
sips -s format icns icon/app-icon.ico --out icon/app-icon.icns
```

### Method 3: Manual Conversion with iconutil (Best Quality)

```bash
# Create iconset folder
mkdir icon/app-icon.iconset

# Add PNG images in required sizes:
# icon_16x16.png, icon_16x16@2x.png (32x32)
# icon_32x32.png, icon_32x32@2x.png (64x64)
# icon_128x128.png, icon_128x128@2x.png (256x256)
# icon_256x256.png, icon_256x256@2x.png (512x512)
# icon_512x512.png, icon_512x512@2x.png (1024x1024)

# Convert to icns
iconutil -c icns icon/app-icon.iconset

# Move to icon folder
mv icon/app-icon.icns icon/
```

## 🔨 Building the Application

### Standard Build

```bash
python3 build_exe.py
```

### Build with Maximum Optimization

```bash
# Install UPX first
brew install upx

# Build
python3 build_exe.py
```

### Build Output

```
dist/
  PostgreSQL_Database_Manager  # macOS executable (no extension)
build/
  [temporary build files]
PostgreSQL_Database_Manager.spec  # PyInstaller spec file
```

## 🚀 Running the Application

### From Build Output

```bash
# Make executable (if not already)
chmod +x dist/PostgreSQL_Database_Manager

# Run with sudo (required for PostgreSQL operations)
sudo ./dist/PostgreSQL_Database_Manager
```

### Troubleshooting "Developer Cannot Be Verified"

If macOS Gatekeeper blocks the app:

#### Option 1: Remove Quarantine Attribute

```bash
xattr -cr dist/PostgreSQL_Database_Manager
```

#### Option 2: Allow in System Preferences

1. Try to open the app (it will be blocked)
2. Go to **System Preferences** → **Security & Privacy**
3. Click **"Open Anyway"** for PostgreSQL_Database_Manager
4. Confirm when prompted

#### Option 3: Disable Gatekeeper Temporarily

```bash
# Disable Gatekeeper (requires admin password)
sudo spctl --master-disable

# Run your app
sudo ./dist/PostgreSQL_Database_Manager

# Re-enable Gatekeeper (recommended)
sudo spctl --master-enable
```

## 📦 Distribution

### Creating a DMG Installer

```bash
# Create DMG
hdiutil create -volname "PostgreSQL Manager" \
  -srcfolder dist/ \
  -ov -format UDZO \
  PostgreSQL_Manager.dmg

# Verify DMG
hdiutil verify PostgreSQL_Manager.dmg
```

### Code Signing (Requires Apple Developer Account)

```bash
# Sign the executable
codesign --force --deep \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  dist/PostgreSQL_Database_Manager

# Verify signature
codesign --verify --verbose dist/PostgreSQL_Database_Manager

# Check signature details
codesign -dv --verbose=4 dist/PostgreSQL_Database_Manager
```

### Notarization (For Distribution Outside App Store)

```bash
# Create app-specific password in Apple ID account
# Store in keychain: xcrun notarytool store-credentials

# Notarize the DMG
xcrun notarytool submit PostgreSQL_Manager.dmg \
  --keychain-profile "AC_PASSWORD" \
  --wait

# Staple the notarization ticket
xcrun stapler staple PostgreSQL_Manager.dmg

# Verify stapling
xcrun stapler validate PostgreSQL_Manager.dmg
```

## 🐛 Troubleshooting

### Python Version Issues

```bash
# If 'python3' not found
brew install python@3.11

# Add to PATH
echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### tkinter Not Found

```bash
# Reinstall Python with tkinter support
brew reinstall python-tk@3.11
```

### PostgreSQL Tools Not Found

```bash
# Add PostgreSQL to PATH
echo 'export PATH="/usr/local/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
which psql pg_dump pg_restore
```

### Permission Denied Errors

```bash
# Make script executable
chmod +x dist/PostgreSQL_Database_Manager

# Run with sudo
sudo ./dist/PostgreSQL_Database_Manager
```

### Build Fails with Import Errors

```bash
# Reinstall dependencies
pip3 uninstall customtkinter pyinstaller
pip3 install customtkinter pyinstaller

# Clear build cache
rm -rf build/ dist/ *.spec
python3 build_exe.py
```

### Large Executable Size

```bash
# Install UPX for compression
brew install upx

# Clean and rebuild
rm -rf build/ dist/ *.spec
python3 build_exe.py

# Expected size: ~10-15 MB with UPX, ~20-25 MB without
```

## 🎯 Platform-Specific Notes

### M1/M2 (Apple Silicon) vs Intel

The build script automatically detects your architecture:

```bash
# Check architecture
uname -m
# arm64 = Apple Silicon (M1/M2)
# x86_64 = Intel

# Build for native architecture (recommended)
python3 build_exe.py

# Build universal binary (both architectures) - Advanced
arch -x86_64 python3 build_exe.py  # Intel build on Apple Silicon
```

### macOS Version Compatibility

- **Built on macOS 13+**: Works on macOS 13+ only
- **Built on macOS 11**: Works on macOS 11+
- **Built on macOS 10.15**: Works on macOS 10.15+

Build on the **oldest version** you want to support.

## 📊 Optimization Results

| Build Type                | Size       | Features                        |
| ------------------------- | ---------- | ------------------------------- |
| **Standard PyInstaller**  | ~20 MB     | Basic executable                |
| **Optimized PyInstaller** | ~15 MB     | Module exclusions               |
| **UPX Compressed**        | **~12 MB** | Full optimization + compression |

## 🔍 Testing Before Distribution

```bash
# Test on clean macOS install (VM recommended)
# 1. Copy executable to test machine
# 2. Verify no Python installed
# 3. Run and test all features

# Test PostgreSQL operations
# 1. Install PostgreSQL
# 2. Create test database
# 3. Test backup
# 4. Test restore
# 5. Verify history tracking
```

## 📝 Release Checklist

- [ ] ✅ Build with UPX compression
- [ ] ✅ Convert icon to .icns
- [ ] ✅ Test on clean macOS system
- [ ] ✅ Test on both Intel and Apple Silicon (if possible)
- [ ] ✅ Verify PostgreSQL integration
- [ ] ✅ Test with sudo permissions
- [ ] ✅ Generate SHA256 checksum
- [ ] ✅ Create DMG installer
- [ ] ✅ Code sign (if distributing publicly)
- [ ] ✅ Notarize (if distributing publicly)
- [ ] ✅ Update release notes

## 🔗 Additional Resources

- [PyInstaller macOS Guide](https://pyinstaller.org/en/stable/usage.html#macos-specific-options)
- [macOS Code Signing Guide](https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution)
- [Apple Developer Program](https://developer.apple.com/programs/)
- [Homebrew Package Manager](https://brew.sh/)

---

**Need Help?** Check the main [BUILD_GUIDE.md](BUILD_GUIDE.md) or open an issue on GitHub.
