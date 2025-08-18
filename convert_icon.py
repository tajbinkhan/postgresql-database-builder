"""
Convert PNG icon to ICO format for use with PyInstaller
"""

from PIL import Image
import os


def convert_png_to_ico():
    """Convert the PNG icon to ICO format"""
    png_path = os.path.join("icon", "app-icon.png")
    ico_path = os.path.join("icon", "app-icon.ico")

    if not os.path.exists(png_path):
        print(f"❌ PNG icon not found: {png_path}")
        return False

    try:
        # Open the PNG image
        img = Image.open(png_path)

        # Convert to ICO format with multiple sizes for best compatibility
        # ICO files can contain multiple sizes
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # Create the ICO file
        img.save(ico_path, format="ICO", sizes=sizes)

        print(f"✅ Successfully converted {png_path} to {ico_path}")
        print(f"📁 ICO file created: {os.path.abspath(ico_path)}")
        return True

    except Exception as e:
        print(f"❌ Error converting icon: {e}")
        return False


if __name__ == "__main__":
    print("🖼️ Converting PNG icon to ICO format...")
    if convert_png_to_ico():
        print("🎉 Icon conversion completed successfully!")
    else:
        print("❌ Icon conversion failed!")
