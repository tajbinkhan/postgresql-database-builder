"""
Font Download Utility for PostgreSQL Database Manager

This utility helps download Poppins font files from Google Fonts.
Run this script to automatically download the required font files.
"""

import urllib.request
import urllib.error
import os
from pathlib import Path
import shutil


def download_poppins_fonts():
    """Download Poppins font family from Google Fonts"""

    # Get the fonts directory path
    fonts_dir = Path(__file__).parent / "fonts"
    fonts_dir.mkdir(exist_ok=True)

    # Google Fonts GitHub repository URLs for direct download
    font_urls = {
        "Poppins-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
        "Poppins-Medium.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Medium.ttf",
        "Poppins-SemiBold.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf",
        "Poppins-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    }

    try:
        print(
            "📥 Downloading Poppins font files from Google Fonts GitHub repository..."
        )

        downloaded_count = 0
        total_files = len(font_urls)

        for filename, url in font_urls.items():
            try:
                print(f"⬇️  Downloading {filename}...")

                # Create request with headers
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                    },
                )

                # Download the font file
                with urllib.request.urlopen(req) as response:
                    font_data = response.read()

                # Save the font file
                font_path = fonts_dir / filename
                with open(font_path, "wb") as f:
                    f.write(font_data)

                # Verify the file was downloaded correctly
                if (
                    font_path.exists() and font_path.stat().st_size > 1000
                ):  # Font files should be > 1KB
                    print(
                        f"✅ Downloaded: {filename} ({font_path.stat().st_size / 1024:.1f} KB)"
                    )
                    downloaded_count += 1
                else:
                    print(
                        f"❌ Failed to download: {filename} (file too small or missing)"
                    )

            except urllib.error.URLError as e:
                print(f"❌ Download error for {filename}: {e}")
            except Exception as e:
                print(f"❌ Unexpected error downloading {filename}: {e}")

        print(
            f"\n🎉 Successfully downloaded {downloaded_count}/{total_files} font files!"
        )

        if downloaded_count == total_files:
            print("✅ All Poppins font files are ready!")
            print("🔄 Please restart the application to use the new fonts.")
        elif downloaded_count > 0:
            print("⚠️  Some font files may be missing. Check the fonts directory.")
        else:
            print("❌ No font files were downloaded successfully.")

        return downloaded_count == total_files

    except urllib.error.URLError as e:
        print(f"❌ Download error: {e}")
        print(
            "💡 Please download manually from: https://fonts.google.com/specimen/Poppins"
        )
        return False

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(
            "💡 Please download manually from: https://fonts.google.com/specimen/Poppins"
        )
        return False


def check_fonts_status():
    """Check which font files are currently available"""
    fonts_dir = Path(__file__).parent / "fonts"

    required_files = [
        "Poppins-Regular.ttf",
        "Poppins-Medium.ttf",
        "Poppins-SemiBold.ttf",
        "Poppins-Bold.ttf",
    ]

    print(f"📁 Checking fonts in: {fonts_dir}")
    print("=" * 50)

    available_count = 0
    for font_file in required_files:
        font_path = fonts_dir / font_file
        if font_path.exists():
            size_mb = font_path.stat().st_size / (1024 * 1024)
            print(f"✅ {font_file} ({size_mb:.1f} MB)")
            available_count += 1
        else:
            print(f"❌ {font_file} (missing)")

    print("=" * 50)
    print(f"Status: {available_count}/{len(required_files)} font files available")

    return available_count == len(required_files)


if __name__ == "__main__":
    import sys

    print("🔤 Poppins Font Download Utility")
    print("=" * 40)

    # Check current status
    if check_fonts_status():
        print("\n✅ All font files are already available!")
        print("🔄 Restart the application if you just added them.")
    else:
        print(f"\n📥 Some font files are missing.")
        response = input("Would you like to download them now? (y/n): ").lower().strip()

        if response in ["y", "yes"]:
            print("\n🚀 Starting download...")
            if download_poppins_fonts():
                print("\n🎉 Download completed successfully!")
            else:
                print("\n❌ Download failed. Please try manual installation.")
        else:
            print("\n💡 Manual installation instructions:")
            print("1. Visit: https://fonts.google.com/specimen/Poppins")
            print("2. Download the font family")
            print("3. Extract and copy .ttf files to the fonts/ directory")
            print("4. Restart the application")
