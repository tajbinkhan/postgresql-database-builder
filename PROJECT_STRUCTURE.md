# Project Structure

```
postgresql-database-manager/
│
├── 📁 .github/                     # GitHub specific files
│   ├── 📁 ISSUE_TEMPLATE/          # Issue templates
│   │   ├── bug_report.md           # Bug report template
│   │   └── feature_request.md      # Feature request template
│   ├── 📁 workflows/               # GitHub Actions workflows
│   │   └── ci.yml                  # CI/CD pipeline
│   └── pull_request_template.md    # Pull request template
│
├── 📁 dist/                        # Built executables (generated)
│   └── PostgreSQL_Database_Manager.exe
│
├── 📁 screenshots/                 # Application screenshots (to be added)
│   ├── backup_tab.png
│   ├── restore_tab.png
│   └── history_tab.png
│
├── 📄 .gitignore                   # Git ignore rules
├── 📄 app.manifest                 # Windows UAC manifest
├── 📄 build.bat                    # Windows batch build script
├── 📄 build_exe.py                 # Executable builder script
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 db_manager.py                # Main application file
├── 📄 LICENSE                      # MIT License
├── 📄 README.md                    # Main project documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 requirements-dev.txt         # Development dependencies
└── 📄 PROJECT_STRUCTURE.md         # This file

```

## File Descriptions

### Core Application Files
- **`db_manager.py`** - Main application with GUI and database operations
- **`app.manifest`** - Windows manifest for administrator privileges
- **`build_exe.py`** - Script to build standalone executable
- **`build.bat`** - Windows batch file for easy building

### Documentation Files
- **`README.md`** - Comprehensive project documentation
- **`CHANGELOG.md`** - Version history and feature tracking
- **`CONTRIBUTING.md`** - Guidelines for contributors
- **`LICENSE`** - MIT License text

### Configuration Files
- **`.gitignore`** - Git ignore patterns
- **`requirements.txt`** - Runtime Python dependencies
- **`requirements-dev.txt`** - Development dependencies

### GitHub Integration
- **`.github/ISSUE_TEMPLATE/`** - Standardized issue templates
- **`.github/workflows/ci.yml`** - Automated testing and builds
- **`.github/pull_request_template.md`** - PR template

### Generated Files (Not in Git)
- **`dist/`** - Built executable files
- **`build/`** - Temporary build files
- **`__pycache__/`** - Python bytecode cache

### User Data Files (Saved in Documents)
The following files are created in `Documents/PostgreSQL Database Manager/`:
- **`db_operations_history.json`** - User operation history and logs
- **`db_manager_settings.json`** - User preferences and application settings

## Development Workflow

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/postgresql-database-manager.git
   ```

2. **Setup Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Run Application**
   ```bash
   python db_manager.py
   ```

4. **Build Executable**
   ```bash
   python build_exe.py
   # or
   build.bat
   ```

## Key Features by File

### `db_manager.py`
- FontManager class for Google Fonts integration
- PostgreSQLChecker for environment validation
- ModernDatabaseManager main application class
- Tabbed interface with Backup, Restore, History
- Threading for background operations
- Settings and history persistence

### `build_exe.py`
- PyInstaller integration
- Real-time build output
- Administrator privilege configuration
- Automatic dependency detection
- Cross-platform compatibility

### GitHub Templates
- Standardized bug reporting
- Feature request workflow
- Pull request checklist
- Automated CI/CD pipeline
