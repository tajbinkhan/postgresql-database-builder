#!/bin/bash
# Convert Windows .ico file to macOS .icns format
# Usage: ./convert_icon_mac.sh

echo "🍎 macOS Icon Converter for PostgreSQL Database Manager"
echo "=========================================================="

# Check if icon file exists
if [ ! -f "icon/app-icon.ico" ]; then
    echo "❌ Error: icon/app-icon.ico not found"
    exit 1
fi

# Check if sips command is available (macOS only)
if ! command -v sips &> /dev/null; then
    echo "❌ Error: sips command not found. This script only works on macOS."
    exit 1
fi

echo "📝 Converting icon/app-icon.ico to icon/app-icon.icns..."

# Method 1: Using sips (simple, works for most cases)
sips -s format icns icon/app-icon.ico --out icon/app-icon.icns

if [ $? -eq 0 ]; then
    echo "✅ Icon converted successfully!"
    echo "📁 Output: icon/app-icon.icns"
    ls -lh icon/app-icon.icns
else
    echo "❌ Conversion failed using sips"
    echo ""
    echo "🔧 Alternative method: Using iconutil (manual steps required)"
    echo "   1. Create iconset folder: mkdir icon/app-icon.iconset"
    echo "   2. Add PNG images in these sizes:"
    echo "      - icon_16x16.png, icon_16x16@2x.png (32x32)"
    echo "      - icon_32x32.png, icon_32x32@2x.png (64x64)"
    echo "      - icon_128x128.png, icon_128x128@2x.png (256x256)"
    echo "      - icon_256x256.png, icon_256x256@2x.png (512x512)"
    echo "      - icon_512x512.png, icon_512x512@2x.png (1024x1024)"
    echo "   3. Run: iconutil -c icns icon/app-icon.iconset"
fi

echo ""
echo "💡 Now you can rebuild with: python3 build_exe.py"
