# Fonts Directory

This directory contains local font files for the PostgreSQL Database Manager application.

## Poppins Font Installation

To use the Poppins font in the application, download the following font files from [Google Fonts](https://fonts.google.com/specimen/Poppins) and place them in this directory:

### Required Font Files:
- `Poppins-Regular.ttf` (400 weight)
- `Poppins-Medium.ttf` (500 weight)
- `Poppins-SemiBold.ttf` (600 weight)
- `Poppins-Bold.ttf` (700 weight)

### Download Instructions:

1. Visit: https://fonts.google.com/specimen/Poppins
2. Click "Download family" button
3. Extract the ZIP file
4. Copy the required `.ttf` files to this `fonts/` directory
5. Restart the application

### Supported Platforms:

- **Windows**: Fonts are loaded using Windows API (AddFontResourceEx)
- **macOS**: Fonts are loaded using Core Text framework
- **Linux**: Fonts are copied to `~/.local/share/fonts/` and font cache is refreshed

### Folder Structure:
```
fonts/
├── README.md (this file)
├── Poppins-Regular.ttf
├── Poppins-Medium.ttf
├── Poppins-SemiBold.ttf
└── Poppins-Bold.ttf
```

### Troubleshooting:

If fonts don't load properly:
1. Ensure font files are named exactly as shown above
2. Check file permissions (fonts should be readable)
3. Restart the application after adding fonts
4. Check console output for font loading messages

The application will automatically fall back to system fonts if Poppins is not available.
