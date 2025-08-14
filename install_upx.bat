@echo off
echo Installing UPX Compressor for Better Executable Compression
echo ===========================================================
echo.

echo UPX can reduce executable size by 30-50%% additional compression.
echo.

echo Please download UPX from: https://upx.github.io/
echo.
echo Instructions:
echo 1. Download UPX for Windows
echo 2. Extract upx.exe to this folder or add to your PATH
echo 3. Run build_exe.py again for smaller executables
echo.

echo Alternative: Download UPX automatically (requires curl)
set /p download="Download UPX automatically? (y/n): "

if /i "%download%"=="y" (
    echo.
    echo Downloading UPX...
    curl -L -o upx.zip "https://github.com/upx/upx/releases/download/v4.2.1/upx-4.2.1-win64.zip"

    if exist upx.zip (
        echo Extracting UPX...
        powershell -command "Expand-Archive -Path upx.zip -DestinationPath . -Force"
        copy "upx-4.2.1-win64\upx.exe" .
        del upx.zip
        rmdir /s /q "upx-4.2.1-win64"
        echo.
        echo ✅ UPX installed successfully!
        echo You can now run build_exe.py for compressed executables.
    ) else (
        echo ❌ Download failed. Please download manually from https://upx.github.io/
    )
)

echo.
pause
