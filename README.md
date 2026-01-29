# PostgreSQL Database Manager

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)

A modern, user-friendly PostgreSQL database management tool built with Python and CustomTkinter. Features a tabbed interface for database backup, restore operations, and complete history tracking. **Now supports Windows, macOS, and Linux!**

## ✨ Features

### 🎯 Core Functionality

- **Database Backup & Restore** - Full PostgreSQL database dump and restore capabilities
- **Tabbed Interface** - Separate tabs for Backup, Restore, and History operations
- **Connection Testing** - Test database connections before operations
- **File Management** - Smart file existence warnings with user confirmation
- **Operation History** - Complete tracking of all database operations with timestamps

### 🎨 Modern UI

- **Dark Theme** - Modern CustomTkinter dark interface
- **Custom Fonts** - Google Fonts integration (Poppins) with intelligent fallbacks
- **Responsive Design** - Scrollable content areas and proper button alignment
- **Progress Indicators** - Real-time operation status and progress feedback

### 🔧 Advanced Features

- **PostgreSQL Auto-Detection** - Automatic PostgreSQL installation checking
- **Environment Management** - Smart PATH variable management and fixing
- **Administrator Privileges** - Built-in UAC support for elevated operations
- **Cross-Platform Ready** - Windows, macOS, and Linux support
- **One-Click Executable** - Standalone executable file generation

## 📸 Screenshots

### Main Interface - Backup Tab

![Backup Tab](screenshots/backup_tab.png)

### Restore Operations

![Restore Tab](screenshots/restore_tab.png)

### History Tracking

![History Tab](screenshots/history_tab.png)

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)

#### Windows

1. Download the latest `PostgreSQL_Database_Manager.exe` from [Releases](../../releases)
2. Right-click and select "Run as administrator"
3. Start managing your PostgreSQL databases!

#### macOS

1. Download the latest `PostgreSQL_Database_Manager` (macOS) from [Releases](../../releases)
2. Open Terminal and run: `chmod +x PostgreSQL_Database_Manager`
3. Run with: `sudo ./PostgreSQL_Database_Manager`

#### Linux

1. Download the latest `PostgreSQL_Database_Manager` (Linux) from [Releases](../../releases)
2. Open Terminal and run: `chmod +x PostgreSQL_Database_Manager`
3. Run with: `sudo ./PostgreSQL_Database_Manager`

### Option 2: Run from Source

```bash
# Clone the repository
git clone https://github.com/tajbinkhan/postgresql-database-builder.git
cd postgresql-database-manager

# Install dependencies
pip install customtkinter

# Run the application
python db_manager.py  # Windows
python3 db_manager.py  # macOS/Linux
```

## 📋 Requirements

### System Requirements

- **Operating System**: Windows 7/8/10/11, macOS 10.13+, or Linux (Ubuntu 18.04+, Fedora 30+, etc.)
- **PostgreSQL**: Must be installed with command-line tools (pg_dump, pg_restore, psql)
- **Python**: 3.7+ (if running from source)

### Python Dependencies

```
customtkinter>=5.0.0
```

### PostgreSQL Tools

The application requires PostgreSQL command-line tools to be installed and accessible:

- `pg_dump` - For database backups
- `pg_restore` - For database restores
- `psql` - For connection testing

**Auto-Detection**: The app automatically detects PostgreSQL installation and can fix PATH issues.

## 🛠️ Installation

### For End Users (Executable)

1. **Download**: Get the latest executable for your platform from the [Releases](../../releases) page
2. **Install PostgreSQL**: Ensure PostgreSQL is installed on your system
3. **Run**:
   - **Windows**: Double-click the .exe (will request administrator privileges)
   - **macOS/Linux**: Run `chmod +x PostgreSQL_Database_Manager` then `sudo ./PostgreSQL_Database_Manager`

### For Developers (Source)

```bash
# Clone repository
git clone https://github.com/tajbinkhan/postgresql-database-builder.git
cd postgresql-database-manager

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python db_manager.py
```

## 📖 Usage Guide

### Database Backup

1. Switch to the **Backup** tab
2. Enter your **source database connection string**:
   ```
   postgresql://username:password@host:port/database_name
   ```
3. **Test Connection** to verify database accessibility
4. Choose **backup filename** (with .sql or .dump extension)
5. Select **backup format** (SQL or Custom)
6. Click **Start Backup**

### Database Restore

1. Switch to the **Restore** tab
2. Enter your **target database connection string**
3. **Test Connection** to verify target database
4. **Browse and select** backup file to restore
5. Choose **restore options** (clean, create, etc.)
6. Click **Start Restore**

### View History

1. Switch to the **History** tab
2. View all **past operations** with timestamps
3. **Filter by operation type** (Backup/Restore)
4. **Click any entry** to view detailed information

## 🔧 Building Executable

### Quick Build

To create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build optimized executable
python build_exe.py

# Or use the batch file
build.bat
```

The executable will be created in the `dist/` folder with administrator privileges enabled.

### 🚀 Advanced Build System Features

Our optimized build system includes multiple compression and optimization techniques:

#### **Automatic Optimization**

- **Python Bytecode Optimization** (`--optimize=2`) - Removes debug information and docstrings
- **Unused Module Exclusion** - Automatically excludes test frameworks, email libraries, and unused modules
- **Binary Stripping** - Removes debug symbols from compiled libraries
- **Smart Compression** - Automatically detects and uses UPX compression when available

#### **File Size Optimization Results**

- **Before Optimization**: ~13+ MB
- **After PyInstaller Optimization**: ~11.0 MB (15% reduction)
- **After UPX Compression**: **~9.6 MB (26% total reduction)**

#### **UPX Compression Setup**

For maximum compression, install UPX compressor:

```bash
# Option 1: Automatic installation
.\install_upx.bat

# Option 2: Manual installation
# 1. Download UPX from https://upx.github.io/
# 2. Extract upx.exe to project folder
# 3. Run build again: python build_exe.py
```

#### **Build Process Features**

- **Real-time Progress** - Live PyInstaller output during build
- **Automatic Cleanup** - Removes temporary build files after completion
- **Size Reporting** - Shows final executable size and compression ratio
- **Error Handling** - Graceful handling of missing dependencies
- **Cross-Platform Ready** - Optimized for Windows with Unix compatibility

#### **Excluded Modules (for Size Optimization)**

The build system automatically excludes these unused modules:

```
tkinter.test, test, unittest, doctest, pdb, pydoc
email, xml, urllib, http, ssl, socket, select
multiprocessing, concurrent
```

#### **Technical Build Specifications**

```python
# PyInstaller command generated:
pyinstaller --onefile --windowed \
    --name=PostgreSQL_Database_Manager \
    --uac-admin --optimize=2 --strip \
    --exclude-module=test --exclude-module=email \
    --exclude-module=xml --exclude-module=urllib \
    --upx-dir=. --manifest=app.manifest \
    db_manager.py
```

## 📦 Deployment & Distribution

### 🎯 Executable Distribution

The optimized executable is perfect for distribution:

#### **System Requirements for End Users**

- **Operating System**: Windows 7/8/10/11 (32-bit or 64-bit)
- **PostgreSQL**: Must be installed with command-line tools
- **No Python Required**: Standalone executable includes all dependencies
- **Administrator Access**: Required for PostgreSQL operations and PATH management

#### **Distribution Checklist**

- ✅ **File Size**: Optimized to ~9.6 MB (26% smaller than unoptimized)
- ✅ **Dependencies**: All Python libraries bundled
- ✅ **Security**: Code-signed executable (recommended for production)
- ✅ **Compatibility**: Works on all supported Windows versions
- ✅ **Administrator Support**: Built-in UAC manifest

#### **Deployment Options**

**Option 1: Direct Download**

```
📁 dist/PostgreSQL_Database_Manager.exe (9.6 MB)
└── Ready for immediate distribution
```

**Option 2: Installer Package** (Future enhancement)

```
📦 PostgreSQL_Database_Manager_Setup.exe
├── Application executable
├── PostgreSQL detection
└── Desktop shortcut creation
```

**Option 3: Portable Package**

```
📁 PostgreSQL_Database_Manager_Portable/
├── PostgreSQL_Database_Manager.exe
├── README.txt
└── LICENSE.txt
```

### 🔐 Security Considerations

#### **Administrator Privileges**

- **Required**: For PostgreSQL operations and PATH management
- **Implementation**: Windows UAC manifest (`app.manifest`)
- **User Experience**: Single UAC prompt on startup
- **Fallback**: Graceful degradation if admin rights denied

#### **Data Security**

- **Local Storage**: All data saved in user's Documents folder
- **No Cloud**: No external data transmission
- **Sanitized Logs**: Database credentials never stored in history
- **Permission Management**: Respects Windows file permissions

## ⚙️ Configuration

### Application Data Location

All application data is stored in your Documents folder:

```
📁 Documents/PostgreSQL Database Manager/
├── db_manager_settings.json    # User preferences and settings
└── db_operations_history.json  # Operation history and logs
```

### Settings File

The application creates `db_manager_settings.json` in the Documents folder to store:

- Default connection strings
- Preferred save locations
- UI preferences
- Font settings

### History File

Operation history is stored in `db_operations_history.json` in the Documents folder:

- Operation timestamps
- Connection details (sanitized)
- File paths and sizes
- Success/failure status

## 🐛 Troubleshooting

### Common Issues

**PostgreSQL Not Found**

```
✅ Solution: The app will auto-detect and offer to fix PATH variables
✅ Manual Fix: Add PostgreSQL bin directory to system PATH
✅ Verification: Run 'pg_dump --version' in command prompt
```

**Connection Failed**

```
✅ Check: Database server is running
✅ Check: Connection string format
✅ Check: User permissions
✅ Check: Firewall settings
```

**Permission Denied**

```
✅ Solution: Run as administrator (right-click → "Run as administrator")
✅ Alternative: Grant user PostgreSQL permissions
✅ Note: Administrator mode required for PATH management
```

**Font Issues**

```
✅ Install Poppins font from Google Fonts for best experience
✅ App includes fallback fonts (Inter, Segoe UI)
✅ System fonts used if Google Fonts unavailable
```

### Build System Troubleshooting

**PyInstaller Issues**

```
❌ Problem: "PyInstaller not found"
✅ Solution: pip install pyinstaller

❌ Problem: "Import errors during build"
✅ Solution: Check virtual environment activation
✅ Alternative: pip install -r requirements.txt

❌ Problem: "Large executable size"
✅ Solution: Install UPX compression (./install_upx.bat)
✅ Expected: 9.6 MB with UPX, 11.0 MB without
```

**UPX Compression Issues**

```
❌ Problem: "UPX not found"
✅ Solution: Run install_upx.bat or download from https://upx.github.io/
✅ Manual: Extract upx.exe to project folder

❌ Problem: "UPX compression failed"
✅ Solution: Some DLLs can't be compressed (normal behavior)
✅ Note: Python runtime DLLs may show warnings (safe to ignore)

❌ Problem: "Executable won't run after UPX"
✅ Solution: Try without UPX first (remove upx.exe)
✅ Alternative: Check antivirus software (UPX sometimes flagged)
```

**Windows-Specific Issues**

```
❌ Problem: "Application won't start"
✅ Solution: Install Microsoft Visual C++ Redistributable
✅ Check: Windows Defender/antivirus exclusions
✅ Alternative: Run from command prompt to see errors

❌ Problem: "UAC keeps prompting"
✅ Solution: Normal behavior - required for PostgreSQL operations
✅ Alternative: Run once as admin, then normal mode may work

❌ Problem: "Files not saving"
✅ Solution: Check Documents folder permissions
✅ Alternative: Run as administrator
```

### Performance Optimization

**Build Performance**

```
🚀 Fast Build: Use build.bat for automated process
🚀 Parallel Build: PyInstaller uses multiple cores automatically
🚀 Incremental: Subsequent builds are faster (cached modules)
```

**Runtime Performance**

```
🚀 Startup: ~2-3 seconds on modern systems
🚀 Operations: Real-time PostgreSQL operations
🚀 Memory: ~50-100 MB RAM usage
```

### Error Logs

- Application errors are displayed in real-time dialogs
- Check PostgreSQL logs for database-specific issues
- Use "Test Connection" to diagnose connection problems

## 📚 Documentation

### 📖 User Documentation

- **[README.md](README.md)** - Main project documentation and user guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and feature updates
- **[LICENSE](LICENSE)** - MIT License terms

### 🛠️ Developer Documentation

- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Comprehensive build system and optimization guide
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment and distribution guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and development setup
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project organization and file structure

### 🎯 Quick Links

- **Build System**: See [BUILD_GUIDE.md](BUILD_GUIDE.md) for detailed optimization instructions
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment workflows
- **Issues**: Report bugs on [GitHub Issues](../../issues)
- **Discussions**: Join [GitHub Discussions](../../discussions)

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
git clone https://github.com/tajbinkhan/postgresql-database-builder.git
cd postgresql-database-manager
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** - For the modern GUI framework
- **PostgreSQL** - For the robust database system
- **Google Fonts** - For the Poppins font family
- **PyInstaller** - For executable generation

## 📞 Support

- **Issues**: Report bugs on [GitHub Issues](../../issues)
- **Discussions**: Join [GitHub Discussions](../../discussions)
- **Email**: tajbink@gmail.com

## 🗺️ Roadmap

### Version 2.0 (Planned)

- [ ] Multi-database support (MySQL, SQLite)
- [ ] Scheduled backup automation
- [ ] Cloud storage integration
- [ ] Database schema comparison
- [ ] SQL query editor
- [ ] User access management

### Version 1.1 (In Progress)

- [x] Administrator privilege support
- [x] Real-time build status
- [x] Enhanced error handling
- [ ] Configuration wizard
- [ ] Backup compression options

---

<div align="center">
  <p>Made with ❤️ for the PostgreSQL community</p>
  <p>⭐ Star this repo if you find it helpful!</p>
</div>
