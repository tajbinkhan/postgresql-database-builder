# PostgreSQL Database Manager

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)

A modern, user-friendly PostgreSQL database management tool built with Python and CustomTkinter. Features a tabbed interface for database backup, restore operations, and complete history tracking.

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
- **Cross-Platform Ready** - Windows optimized with Unix compatibility
- **One-Click Executable** - Standalone .exe file generation

## 📸 Screenshots

### Main Interface - Backup Tab
![Backup Tab](screenshots/backup_tab.png)

### Restore Operations
![Restore Tab](screenshots/restore_tab.png)

### History Tracking
![History Tab](screenshots/history_tab.png)

## 🚀 Quick Start

### Option 1: Download Executable (Recommended)
1. Download the latest `PostgreSQL_Database_Manager.exe` from [Releases](../../releases)
2. Right-click and select "Run as administrator"
3. Start managing your PostgreSQL databases!

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/tajbinkhan/postgresql-database-builder.git
cd postgresql-database-manager

# Install dependencies
pip install customtkinter

# Run the application
python db_manager.py
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 7/8/10/11
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
1. **Download**: Get the latest `.exe` file from the [Releases](../../releases) page
2. **Install PostgreSQL**: Ensure PostgreSQL is installed on your system
3. **Run**: Double-click the executable (will request administrator privileges)

### For Developers (Source)
```bash
# Clone repository
git clone https://github.com/tajbinkhan/postgresql-database-builder.git
cd postgresql-database-manager

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

To create your own executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Or use the batch file
build.bat
```

The executable will be created in the `dist/` folder with administrator privileges enabled.

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
```

**Connection Failed**
```
✅ Check: Database server is running
✅ Check: Connection string format
✅ Check: User permissions
```

**Permission Denied**
```
✅ Solution: Run as administrator (right-click → "Run as administrator")
```

**Font Issues**
```
✅ Install Poppins font from Google Fonts for best experience
✅ App includes fallback fonts (Inter, Segoe UI)
```

### Error Logs
- Application errors are displayed in real-time dialogs
- Check PostgreSQL logs for database-specific issues
- Use "Test Connection" to diagnose connection problems

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
