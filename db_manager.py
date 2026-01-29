import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading
from datetime import datetime
import json
import platform
import tkinter.font as tkfont
from pathlib import Path

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "system", "dark", or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", or "dark-blue"


class ScrollableErrorDialog:
    """Custom scrollable error dialog with maximum width"""

    def __init__(
        self,
        parent,
        title="Error",
        message="An error occurred",
        max_width=800,
        max_height=600,
        font_family="Poppins",
    ):
        self.parent = parent
        self.result = None
        self.font_family = font_family

        # Create toplevel window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Calculate dialog size based on content
        message_lines = message.count("\n") + 1
        estimated_height = min(max_height, max(300, message_lines * 25 + 200))
        estimated_width = min(max_width, max(500, min(len(message) * 7, 800)))

        dialog_width = estimated_width
        dialog_height = estimated_height

        # Center the dialog on parent window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        self.dialog.resizable(True, True)
        self.dialog.minsize(300, 150)

        # Configure grid
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(1, weight=1)

        # Error icon and title frame
        title_frame = ctk.CTkFrame(self.dialog)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)

        # Error icon
        error_label = ctk.CTkLabel(
            title_frame, text="❌", font=ctk.CTkFont(family=self.font_family, size=24)
        )
        error_label.grid(row=0, column=0, padx=(10, 0), pady=10)

        # Title label
        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
        )
        title_label.grid(row=0, column=1, padx=(10, 10), pady=10, sticky="w")

        # Scrollable text frame
        text_frame = ctk.CTkScrollableFrame(self.dialog)
        text_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        text_frame.grid_columnconfigure(0, weight=1)

        # Message text with better formatting
        # Split very long lines for better readability
        formatted_message = message
        if len(message) > 1000:
            # For very long messages, add line breaks at reasonable points
            lines = message.split("\n")
            formatted_lines = []
            for line in lines:
                if len(line) > 80:
                    # Break long lines at word boundaries
                    words = line.split(" ")
                    current_line = ""
                    for word in words:
                        if len(current_line + word) > 80:
                            if current_line:
                                formatted_lines.append(current_line.strip())
                                current_line = word + " "
                        else:
                            current_line += word + " "
                    if current_line:
                        formatted_lines.append(current_line.strip())
                else:
                    formatted_lines.append(line)
            formatted_message = "\n".join(formatted_lines)

        message_label = ctk.CTkLabel(
            text_frame,
            text=formatted_message,
            font=ctk.CTkFont(family=self.font_family, size=12),
            justify="left",
            wraplength=dialog_width - 80,
        )
        message_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        # Button frame
        button_frame = ctk.CTkFrame(self.dialog)
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        button_frame.grid_columnconfigure(0, weight=1)

        # OK button
        ok_button = ctk.CTkButton(
            button_frame,
            text="OK",
            command=self.ok_clicked,
            width=100,
            font=ctk.CTkFont(family=self.font_family, size=12),
        )
        ok_button.grid(row=0, column=0, pady=10)

        # Bind escape key and window close
        self.dialog.bind("<Escape>", lambda e: self.ok_clicked())
        self.dialog.protocol("WM_DELETE_WINDOW", self.ok_clicked)

        # Focus on OK button
        ok_button.focus()

    def ok_clicked(self):
        self.result = "ok"
        self.dialog.destroy()

    def show(self):
        """Show the dialog and wait for user response"""
        self.dialog.wait_window()
        return self.result


def show_error_dialog(
    parent, title="Error", message="An error occurred", font_family="Poppins"
):
    """Helper function to show scrollable error dialog"""
    dialog = ScrollableErrorDialog(parent, title, message, font_family=font_family)
    return dialog.show()


class PostgreSQLChecker:
    """Handles PostgreSQL installation verification and environment setup"""

    def __init__(self):
        self.pg_commands = ["pg_dump", "pg_restore", "psql"]
        self.common_postgres_paths = self._get_common_paths()
        self.postgres_status = self.check_postgresql_installation()

    def _get_common_paths(self):
        """Get common PostgreSQL installation paths based on OS"""
        system = platform.system()

        if system == "Windows":
            return [
                r"C:\Program Files\PostgreSQL\*\bin",
                r"C:\Program Files (x86)\PostgreSQL\*\bin",
                r"C:\PostgreSQL\*\bin",
                r"C:\postgresql\bin",
                r"C:\postgres\bin",
                r"C:\ProgramData\PostgreSQL\*\bin",
                os.path.expanduser(r"~\AppData\Local\Programs\PostgreSQL\*\bin"),
            ]
        elif system == "Darwin":  # macOS
            return [
                "/usr/local/bin",
                "/opt/homebrew/bin",
                "/opt/homebrew/opt/postgresql@*/bin",
                "/usr/local/opt/postgresql@*/bin",
                "/Library/PostgreSQL/*/bin",
                "/Applications/Postgres.app/Contents/Versions/*/bin",
                os.path.expanduser("~/Library/PostgreSQL/*/bin"),
            ]
        else:  # Linux
            return [
                "/usr/bin",
                "/usr/local/bin",
                "/usr/lib/postgresql/*/bin",
                "/opt/postgresql/bin",
                "/opt/PostgreSQL/*/bin",
                os.path.expanduser("~/.local/bin"),
            ]

    def check_command_availability(self, command):
        """Check if a specific PostgreSQL command is available"""
        try:
            result = subprocess.run(
                [command, "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return True, result.stdout.strip()
            return False, result.stderr
        except FileNotFoundError:
            return False, f"{command} not found"
        except subprocess.TimeoutExpired:
            return False, f"{command} command timed out"
        except Exception as e:
            return False, str(e)

    def check_postgresql_installation(self):
        """Check PostgreSQL installation status"""
        status = {
            "installed": False,
            "commands_available": {},
            "missing_commands": [],
            "path_issues": False,
            "suggested_paths": [],
        }

        # Check each required command
        for cmd in self.pg_commands:
            available, info = self.check_command_availability(cmd)
            status["commands_available"][cmd] = {"available": available, "info": info}
            if not available:
                status["missing_commands"].append(cmd)

        # If all commands are available, PostgreSQL is properly installed
        if not status["missing_commands"]:
            status["installed"] = True
        else:
            # Check if PostgreSQL might be installed but not in PATH
            status["suggested_paths"] = self.find_postgresql_installations()
            if status["suggested_paths"]:
                status["path_issues"] = True

        return status

    def find_postgresql_installations(self):
        """Find potential PostgreSQL installations"""
        found_paths = []

        # Search common installation directories
        import glob

        for path_pattern in self.common_postgres_paths:
            try:
                paths = glob.glob(path_pattern)
                for path in paths:
                    if os.path.exists(path):
                        # Check if pg_dump exists in this path
                        pg_dump_path = os.path.join(
                            path,
                            (
                                "pg_dump.exe"
                                if platform.system() == "Windows"
                                else "pg_dump"
                            ),
                        )
                        if os.path.exists(pg_dump_path):
                            found_paths.append(path)
            except Exception:
                continue

        return found_paths

    def get_current_path(self):
        """Get current PATH environment variable"""
        return os.environ.get("PATH", "")

    def add_to_path(self, new_path):
        """Add a directory to PATH environment variable"""
        try:
            current_path = self.get_current_path()
            if new_path not in current_path:
                if platform.system() == "Windows":
                    # Update PATH for current session
                    os.environ["PATH"] = f"{new_path};{current_path}"

                    # Try to update system PATH (requires admin privileges)
                    try:
                        self.update_windows_path(new_path)
                        return True, "PATH updated successfully"
                    except Exception as e:
                        return (
                            False,
                            f"Could not update system PATH (admin required): {e}",
                        )
                else:
                    # Unix-like systems (macOS/Linux)
                    # Update current session
                    os.environ["PATH"] = f"{new_path}:{current_path}"

                    # Try to update shell configuration file for persistence
                    try:
                        success, msg = self.update_unix_shell_config(new_path)
                        if success:
                            return True, msg
                        else:
                            return False, msg
                    except Exception as e:
                        return False, f"Could not update shell configuration: {e}"
            else:
                return True, "Path already in PATH"
        except Exception as e:
            return False, f"Error updating PATH: {e}"

    def update_windows_path(self, new_path):
        """Update Windows system PATH (requires admin privileges)"""
        if not winreg:
            raise Exception(
                "winreg not available - cannot update system PATH on this platform"
            )

        try:
            # Open the registry key for system environment variables
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
                0,
                winreg.KEY_ALL_ACCESS,
            )

            # Get current PATH value
            current_path, _ = winreg.QueryValueEx(key, "PATH")

            # Add new path if not already present
            if new_path not in current_path:
                new_path_value = f"{current_path};{new_path}"
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)

            winreg.CloseKey(key)

            # Note: Changes will take effect after restart or logoff/logon

        except ImportError:
            raise Exception("winreg not available - cannot update system PATH")
        except PermissionError:
            raise Exception("Administrator privileges required to update system PATH")

    def update_unix_shell_config(self, new_path):
        """Update shell configuration file for macOS/Linux"""
        try:
            # Determine which shell config file to use
            home = os.path.expanduser("~")
            shell = os.environ.get("SHELL", "/bin/bash")

            # Determine config file based on shell
            if "zsh" in shell:
                config_file = os.path.join(home, ".zshrc")
            elif "bash" in shell:
                # macOS uses .bash_profile, Linux typically uses .bashrc
                if platform.system() == "Darwin":
                    config_file = os.path.join(home, ".bash_profile")
                    # Also check .bashrc as fallback
                    if not os.path.exists(config_file) and os.path.exists(os.path.join(home, ".bashrc")):
                        config_file = os.path.join(home, ".bashrc")
                else:
                    config_file = os.path.join(home, ".bashrc")
            else:
                config_file = os.path.join(home, ".profile")

            # Check if path is already in the config file
            export_line = f'export PATH="{new_path}:$PATH"'

            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    content = f.read()
                    if new_path in content:
                        return True, f"PATH already configured in {os.path.basename(config_file)}"

            # Append to config file
            with open(config_file, 'a') as f:
                f.write(f"\n# PostgreSQL - Added by PostgreSQL Database Manager\n")
                f.write(f"{export_line}\n")

            return True, f"PATH added to {os.path.basename(config_file)}. Changes will take effect in new terminal sessions."

        except PermissionError:
            return False, f"Permission denied writing to {config_file}"
        except Exception as e:
            return False, f"Error updating shell config: {str(e)}"

    def show_installation_dialog(self, parent_window, show_success=True):
        """Show PostgreSQL installation status and fix options"""
        status = self.postgres_status

        if status["installed"]:
            if show_success:
                version_info = "\n".join(
                    [
                        f"✅ {cmd}: {status['commands_available'][cmd]['info']}"
                        for cmd in self.pg_commands
                    ]
                )
                messagebox.showinfo(
                    "✅ PostgreSQL Status",
                    f"PostgreSQL is properly installed and configured!\n\n{version_info}",
                )
            return True

        # Create detailed error message
        system = platform.system()
        message = "❌ PostgreSQL Tools Not Found\n\n"
        message += "Missing commands:\n"

        for cmd in status["missing_commands"]:
            message += f"  ❌ {cmd}\n"

        if status["path_issues"]:
            message += f"\n✅ Good news! PostgreSQL installation found:\n"
            for path in status["suggested_paths"][:3]:  # Show max 3 paths
                message += f"   📁 {path}\n"
            if len(status["suggested_paths"]) > 3:
                message += f"   ... and {len(status['suggested_paths']) - 3} more\n"
            message += "\n💡 These directories need to be added to your PATH.\n"
            message += "\nWould you like to fix this?"

            # Show dialog with fix option
            result = messagebox.askyesnocancel(
                "🔧 Fix PostgreSQL PATH",
                message
                + "\n\n📋 Choose an option:\n"
                + "• YES: Automatically add to PATH (recommended)\n"
                + "• NO: Show manual setup instructions\n"
                + "• CANCEL: Continue without fixing",
            )

            if result is True:  # YES - Auto fix
                return self.auto_fix_path(status["suggested_paths"])
            elif result is False:  # NO - Manual instructions
                self.show_manual_instructions(status["suggested_paths"])
                system = platform.system()
                if system in ["Darwin", "Linux"]:
                    # Unix systems - need to reload shell
                    messagebox.showinfo(
                        "✅ PATH Updated Successfully",
                        f"PostgreSQL has been added to your PATH:\n\n"
                        f"📁 {postgres_path}\n\n"
                        f"ℹ️ {message}\n\n"
                        f"⚠️ IMPORTANT: To activate the changes:\n"
                        f"1. Close this application\n"
                        f"2. Open a NEW Terminal window\n"
                        f"3. Run: source ~/.zshrc  (or source ~/.bashrc)\n"
                        f"4. Restart this application from the new Terminal\n\n"
                        f"OR simply restart your computer for changes to take effect.",
                    )
                else:
                    # Windows
                    messagebox.showinfo(
                        "✅ PATH Updated",
                        f"Successfully added PostgreSQL to PATH:\n\n"
                        f"📁 {postgres_path}\n\n"
                        f"ℹ️ {message}\n\n"
                        f"Please restart the application to apply changes.",
                if system == "Windows":
                message += "Download for Windows:\n"
                message += "🌐 https://www.postgresql.org/download/windows/\n"
                message += "🌐 https://www.enterprisedb.com/downloads/postgres-postgresql-downloads\n\n"
                message += "⚠️ During installation:\n"
                message += "  • Select 'Command Line Tools'\n"
                message += "  • Check 'Add PostgreSQL to PATH'\n"
            elif system == "Darwin":  # macOS
                message += "Install on macOS:\n"
                message += "📦 Using Homebrew (recommended):\n"
                message += "   brew install postgresql@15\n\n"
                message += "🌐 Or download from:\n"
                message += "   https://www.postgresql.org/download/macosx/\n\n"
            else:  # Linux
                message += "Install on Linux:\n"
                message += "📦 Debian/Ubuntu:\n"
                message += "   sudo apt-get install postgresql-client\n\n"
                message += "📦 RHEL/CentOS:\n"
                message += "   sudo yum install postgresql\n\n"
                message += "📦 Arch:\n"
                message += "   sudo pacman -S postgresql\n\n"

            messagebox.showerror("PostgreSQL Not Installed", message)
            return False

    def auto_fix_path(self, suggested_paths):
        """Automatically fix PATH by adding PostgreSQL directory"""
        if not suggested_paths:
            return False

        # Use the first found path (usually the latest version)
        postgres_path = suggested_paths[0]

        try:
            success, message = self.add_to_path(postgres_path)

            if success:
                messagebox.showinfo(
                    "✅ PATH Updated",
                    f"Successfully added PostgreSQL to PATH:\n\n"
                    f"📁 {postgres_path}\n\n"
                    f"ℹ️ {message}\n\n"
                    f"Please restart the application to apply changes.",
                )
                return True
            else:
                messagebox.showerror(
                    "❌ PATH Update Failed",
                    f"Could not update PATH automatically:\n\n{message}\n\n"
                    f"Please add manually:\n📁 {postgres_path}",
                )
                return False

        except Exception as e:
            messagebox.showerror(
                "❌ Error",
                f"Error fixing PATH:\n{str(e)}\n\n"
                f"Please add manually:\n📁 {postgres_path}",
            )
            return False

    def show_manual_instructions(self, suggested_paths=None):
        """Show manual PATH setup instructions"""
        system = platform.system()
        instructions = "🔧 Manual PostgreSQL PATH Setup\n\n"

        if suggested_paths:
            instructions += "📁 Add this path to your environment:\n"
            instructions += f"   {suggested_paths[0]}\n\n"

        if system == "Windows":
            instructions += """Windows Setup:
1. Press Win + R, type: sysdm.cpl
2. Go to 'Advanced' tab → 'Environment Variables'
3. Under 'System variables', find and select 'Path'
4. Click 'Edit' → 'New'
5. Paste the PostgreSQL bin path
6. Click 'OK' on all dialogs
7. Restart this application

Alternative (PowerShell as Admin):
$env:Path += ";C:\\Program Files\\PostgreSQL\\15\\bin"
[Environment]::SetEnvironmentVariable('Path', $env:Path, 'Machine')"""
        elif system == "Darwin":  # macOS
            instructions += """macOS Setup:
1. Open Terminal
2. Edit your shell profile:
   nano ~/.zshrc   (for zsh, default on macOS)
   # or
   nano ~/.bash_profile   (for bash)

3. Add this line:
   export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

4. Save (Ctrl+O, Enter, Ctrl+X)
5. Reload: source ~/.zshrc
6. Restart this application

If using Homebrew:
brew install postgresql@15
brew link postgresql@15"""
        else:  # Linux
            instructions += """Linux Setup:
1. Open Terminal
2. Edit your shell profile:
   nano ~/.bashrc

3. Add this line:
   export PATH="/usr/bin:/usr/local/bin:$PATH"

4. Save and reload:
   source ~/.bashrc
5. Restart this application

Verify installation:
which psql
psql --version"""

        messagebox.showinfo("Manual Setup Instructions", instructions)


class FontManager:
    """Handles local and system font integration with fallback options"""

    def __init__(self):
        self.app_root = Path(__file__).parent
        self.fonts_dir = self.app_root / "fonts"

        # Font files to look for in the fonts directory
        self.font_files = {
            "Poppins": [
                "Poppins-Regular.ttf",
                "Poppins-Medium.ttf",
                "Poppins-SemiBold.ttf",
                "Poppins-Bold.ttf",
            ]
        }

        self.preferred_fonts = [
            "Poppins",  # Primary choice (will be loaded from local folder)
            "Inter",  # Modern alternative
            "Segoe UI",  # Windows default
            "SF Pro Display",  # macOS default
            "Ubuntu",  # Linux popular choice
            "-apple-system",  # System font on macOS
            "BlinkMacSystemFont",  # System font on macOS
            "Arial",  # Universal fallback
            "sans-serif",  # Ultimate fallback
        ]

        # Load local fonts first
        self.load_local_fonts()

        # Then find the best available font
        self.selected_font = self.get_best_available_font()

    def load_local_fonts(self):
        """Load fonts from the local fonts directory"""
        if not self.fonts_dir.exists():
            print(f"Fonts directory not found: {self.fonts_dir}")
            return

        try:
            if platform.system() == "Windows":
                self._load_fonts_windows()
            elif platform.system() == "Darwin":  # macOS
                self._load_fonts_macos()
            else:  # Linux
                self._load_fonts_linux()

        except Exception as e:
            print(f"Error loading local fonts: {e}")

    def _load_fonts_windows(self):
        """Load fonts on Windows using Windows API"""
        try:
            import ctypes
            from ctypes import wintypes

            # Windows API constants
            FR_PRIVATE = 0x10

            # Load AddFontResourceEx function
            gdi32 = ctypes.windll.gdi32
            add_font_resource_ex = gdi32.AddFontResourceExW
            add_font_resource_ex.argtypes = [
                wintypes.LPCWSTR,
                wintypes.DWORD,
                ctypes.c_void_p,
            ]
            add_font_resource_ex.restype = ctypes.c_int

            loaded_fonts = []
            for font_family, font_files in self.font_files.items():
                for font_file in font_files:
                    font_path = self.fonts_dir / font_file
                    if font_path.exists():
                        result = add_font_resource_ex(str(font_path), FR_PRIVATE, None)
                        if result > 0:
                            loaded_fonts.append(font_file)
                            print(f"✅ Loaded font: {font_file}")
                        else:
                            print(f"❌ Failed to load font: {font_file}")

            if loaded_fonts:
                print(f"Successfully loaded {len(loaded_fonts)} font files")

        except Exception as e:
            print(f"Windows font loading error: {e}")

    def _load_fonts_macos(self):
        """Load fonts on macOS using Core Text"""
        try:
            import ctypes
            import ctypes.util

            # Load Core Text framework
            core_text_path = ctypes.util.find_library("CoreText")
            core_foundation_path = ctypes.util.find_library("CoreFoundation")

            if core_text_path and core_foundation_path:
                core_text = ctypes.cdll.LoadLibrary(core_text_path)
                core_foundation = ctypes.cdll.LoadLibrary(core_foundation_path)

                loaded_fonts = []
                for font_family, font_files in self.font_files.items():
                    for font_file in font_files:
                        font_path = self.fonts_dir / font_file
                        if font_path.exists():
                            # This is a simplified approach - you might need more complex CTFont registration
                            loaded_fonts.append(font_file)
                            print(f"✅ Font available: {font_file}")

                if loaded_fonts:
                    print(f"Font files found: {len(loaded_fonts)}")
            else:
                print("Core Text or Core Foundation framework not found")

        except Exception as e:
            print(f"macOS font loading error: {e}")

    def _load_fonts_linux(self):
        """Load fonts on Linux using fontconfig"""
        try:
            import subprocess

            # Create fontconfig directory if it doesn't exist
            fontconfig_dir = Path.home() / ".local/share/fonts"
            fontconfig_dir.mkdir(parents=True, exist_ok=True)

            loaded_fonts = []
            for font_family, font_files in self.font_files.items():
                for font_file in font_files:
                    font_path = self.fonts_dir / font_file
                    if font_path.exists():
                        # Copy font to user fonts directory
                        target_path = fontconfig_dir / font_file
                        if not target_path.exists():
                            import shutil

                            shutil.copy2(font_path, target_path)
                        loaded_fonts.append(font_file)
                        print(f"✅ Font available: {font_file}")

            if loaded_fonts:
                # Refresh font cache
                subprocess.run(["fc-cache", "-fv"], capture_output=True)
                print(f"Font files processed: {len(loaded_fonts)}")

        except Exception as e:
            print(f"Linux font loading error: {e}")

    def get_best_available_font(self):
        """Get the best available font family from our preferred list"""
        try:
            import tkinter as tk

            root = tk.Tk()
            root.withdraw()  # Hide the window
            available_fonts = list(tkfont.families())
            root.destroy()

            # Check each preferred font in order
            for font in self.preferred_fonts:
                if font in available_fonts:
                    print(f"Selected font: {font}")
                    return font

            # If no preferred fonts found, use the first modern-looking font
            modern_fonts = [
                f
                for f in available_fonts
                if any(
                    modern in f.lower()
                    for modern in ["ui", "modern", "display", "text", "sans"]
                )
            ]

            if modern_fonts:
                print(f"Using modern system font: {modern_fonts[0]}")
                return modern_fonts[0]

        except Exception as e:
            print(f"Font detection error: {e}")

        # Ultimate fallback
        print("Using fallback font: Segoe UI")
        return "Segoe UI"

    def get_font_family(self):
        """Get the selected font family"""
        return self.selected_font

    def get_font_path(self, font_file):
        """Get the path to a specific font file"""
        return self.fonts_dir / font_file

    def check_local_fonts_available(self):
        """Check if local Poppins fonts are available"""
        if not self.fonts_dir.exists():
            return False

        for font_family, font_files in self.font_files.items():
            for font_file in font_files:
                if (self.fonts_dir / font_file).exists():
                    return True
        return False

    def get_font(self, size=12, weight="normal"):
        """Get a CTkFont with the selected font family"""
        valid_weight = "bold" if weight == "bold" else "normal"
        return ctk.CTkFont(family=self.selected_font, size=size, weight=valid_weight)

    def get_title_font(self, size=16):
        """Get a bold title font"""
        return ctk.CTkFont(family=self.selected_font, size=size, weight="bold")

    def get_heading_font(self, size=14):
        """Get a medium weight heading font"""
        return ctk.CTkFont(family=self.selected_font, size=size, weight="bold")

    def get_body_font(self, size=12):
        """Get a regular body text font"""
        return ctk.CTkFont(family=self.selected_font, size=size, weight="normal")

    def get_small_font(self, size=10):
        """Get a small text font"""
        return ctk.CTkFont(family=self.selected_font, size=size, weight="normal")

    def get_button_font(self, size=12):
        """Get a button font"""
        return ctk.CTkFont(family=self.selected_font, size=size, weight="normal")


class ModernDatabaseManager:
    def __init__(self):
        # Initialize font manager
        self.font_manager = FontManager()
        self.font_family = self.font_manager.get_font_family()
        print(f"Using font family: {self.font_family}")

        # Check font status and provide instructions
        if self.font_manager.check_local_fonts_available():
            if self.font_family == "Poppins":
                print("✅ Poppins font loaded successfully from local fonts directory!")
            else:
                print(
                    "⚠️  Poppins font files found but not loaded. Using fallback font."
                )
        else:
            print("📁 No local Poppins font files found.")
            print("💡 To use Poppins font:")
            print(
                f"   1. Download Poppins font from: https://fonts.google.com/specimen/Poppins"
            )
            print(f"   2. Place the .ttf files in: {self.font_manager.fonts_dir}")
            print("   3. Restart the application")
            print(
                "   Required files: Poppins-Regular.ttf, Poppins-Medium.ttf, Poppins-SemiBold.ttf, Poppins-Bold.ttf"
            )

        # Initialize PostgreSQL checker
        self.postgres_checker = PostgreSQLChecker()

        self.root = ctk.CTk()
        self.root.title("PostgreSQL Database Manager")
        self.root.geometry("1100x850")
        self.root.minsize(1000, 750)

        # Default save location (Desktop)
        self.save_location = os.path.join(os.path.expanduser("~"), "Desktop")

        # Application data directory (Documents folder)
        self.app_data_dir = os.path.join(
            os.path.expanduser("~"), "Documents", "PostgreSQL Database Manager"
        )

        # Create application data directory if it doesn't exist
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)

        # History and settings file paths in Documents folder
        self.history_file = os.path.join(
            self.app_data_dir, "db_operations_history.json"
        )
        self.settings_file = os.path.join(self.app_data_dir, "db_manager_settings.json")
        self.load_history()
        self.load_settings()

        # Default connection strings
        self.default_source_db = ""
        self.default_target_db = ""

        self.setup_ui()

        # Check PostgreSQL installation after UI is ready
        self.check_postgresql_on_startup()

    def create_font(self, size=12, weight="normal"):
        """Helper method to create fonts with the custom font family"""
        if weight == "bold":
            return ctk.CTkFont(family=self.font_family, size=size, weight="bold")
        else:
            return ctk.CTkFont(family=self.font_family, size=size, weight="normal")

    def get_app_data_directory(self):
        """Get the application data directory path"""
        return self.app_data_dir

    def check_postgresql_on_startup(self):
        """Check PostgreSQL installation on application startup"""

        def check_postgres():
            # Small delay to ensure UI is fully loaded
            def show_dialog_if_needed():
                # Only show dialog if there are issues with PostgreSQL
                if not self.postgres_checker.postgres_status["installed"]:
                    self.postgres_checker.show_installation_dialog(
                        self.root, show_success=False
                    )

            self.root.after(1000, show_dialog_if_needed)

        # Run check in background
        threading.Thread(target=check_postgres, daemon=True).start()

    def check_postgresql_status(self):
        """Manual PostgreSQL status check (for menu/button)"""
        self.postgres_checker.postgres_status = (
            self.postgres_checker.check_postgresql_installation()
        )
        return self.postgres_checker.show_installation_dialog(self.root)

    def setup_ui(self):
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main container with padding
        main_container = ctk.CTkFrame(
            self.root, corner_radius=0, fg_color="transparent"
        )
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(main_container, height=80, corner_radius=15)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_propagate(False)

        # PostgreSQL status button
        self.postgres_status_btn = ctk.CTkButton(
            header_frame,
            text="🔧 Check PostgreSQL",
            command=self.check_postgresql_status,
            width=140,
            height=35,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#14375e", "#1f538d"),
        )
        self.postgres_status_btn.grid(row=0, column=0, padx=(20, 10), pady=20)

        title_label = ctk.CTkLabel(
            header_frame,
            text="🗄️ PostgreSQL Database Manager",
            font=self.create_font(size=28, weight="bold"),
        )
        title_label.grid(row=0, column=1, pady=20)

        # Content area with tabs
        self.tabview = ctk.CTkTabview(
            main_container,
            corner_radius=15,
            segmented_button_fg_color=("#e6e6e6", "gray15"),
            segmented_button_selected_color=("#1f538d", "#14375e"),
            segmented_button_selected_hover_color=("#14375e", "#1f538d"),
            segmented_button_unselected_color=("#e6e6e6", "gray15"),
            segmented_button_unselected_hover_color=("#d0d0d0", "gray25"),
            text_color=("gray10", "gray90"),
            text_color_disabled=("gray50", "gray45"),
            height=600,
            border_width=1,
            border_color=("#e6e6e6", "gray15"),
            anchor="center",
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", pady=(0, 10), padx=10)
        main_container.grid_rowconfigure(1, weight=1)

        # Create tabs
        self.setup_backup_tab()
        self.setup_restore_tab()
        self.setup_history_tab()

        # Configure tab button fonts and alignment
        self.configure_tab_buttons()

        # Status bar
        self.status_frame = ctk.CTkFrame(main_container, height=50, corner_radius=10)
        self.status_frame.grid(row=2, column=0, sticky="ew")
        self.status_frame.grid_columnconfigure(1, weight=1)
        self.status_frame.grid_propagate(False)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200, height=10)
        self.progress_bar.grid(row=0, column=0, padx=(20, 10), pady=15)
        self.progress_bar.set(0)

        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            textvariable=self.status_var,
            font=self.create_font(size=12),
        )
        self.status_label.grid(row=0, column=1, sticky="w", pady=15)

    def configure_tab_buttons(self):
        """Configure tab button fonts and alignment for better appearance"""
        try:
            # Use after() to configure tabs after they're fully created
            def configure_tabs():
                try:
                    # Access the segmented button widget that contains the tab buttons
                    if hasattr(self.tabview, "_segmented_button"):
                        segmented_button = self.tabview._segmented_button

                        # Configure the segmented button widget for better spacing
                        if hasattr(segmented_button, "configure"):
                            try:
                                segmented_button.configure(
                                    font=self.create_font(size=12, weight="bold"),
                                    height=36,
                                    corner_radius=8,
                                    border_width=1,
                                )
                            except Exception as config_e:
                                print(f"Tab button config error: {config_e}")

                        # Configure individual tab buttons with spacing
                        if hasattr(segmented_button, "_buttons_dict"):
                            for (
                                button_name,
                                button,
                            ) in segmented_button._buttons_dict.items():
                                if hasattr(button, "configure"):
                                    try:
                                        button.configure(
                                            font=self.create_font(
                                                size=12, weight="bold"
                                            ),
                                            anchor="center",
                                            corner_radius=6,
                                        )
                                    except Exception as btn_e:
                                        print(f"Button config error: {btn_e}")

                                # Try to add spacing using grid configuration
                                if hasattr(button, "grid_configure"):
                                    try:
                                        button.grid_configure(padx=3, pady=2)
                                    except Exception as grid_e:
                                        print(f"Grid spacing error: {grid_e}")

                    # Configure the tab view for better spacing between buttons
                    if hasattr(self.tabview, "configure"):
                        try:
                            self.tabview.configure(
                                segmented_button_selected_color=("#1f538d", "#14375e"),
                                segmented_button_unselected_color=("#f0f0f0", "gray20"),
                                border_width=0,
                            )
                        except Exception as tv_e:
                            print(f"TabView config error: {tv_e}")

                    # Try to add padding to the segmented button container
                    try:
                        if hasattr(self.tabview, "_segmented_button"):
                            sb = self.tabview._segmented_button
                            if hasattr(sb, "grid_configure"):
                                sb.grid_configure(padx=10, pady=5)
                    except Exception as padding_e:
                        print(f"Padding config error: {padding_e}")

                    # Note: Cannot modify pack configuration for grid-managed widgets
                    # CustomTkinter tab buttons use grid internally, so we skip pack modifications

                except Exception as inner_e:
                    print(f"Inner tab configuration error: {inner_e}")

            # Schedule the configuration to run after the UI is fully loaded
            self.root.after(100, configure_tabs)

        except Exception as e:
            print(f"Note: Could not configure tab button fonts: {e}")
            # This is not critical, so we continue without stopping

    def setup_backup_tab(self):
        # Backup tab
        self.backup_tab = self.tabview.add("💾 Backup")
        self.backup_tab.grid_columnconfigure(0, weight=1)
        self.backup_tab.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for backup content
        backup_scrollable = ctk.CTkScrollableFrame(
            self.backup_tab,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=("gray75", "gray25"),
            scrollbar_button_hover_color=("gray64", "gray35"),
        )
        backup_scrollable.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        backup_scrollable.grid_columnconfigure(0, weight=1)

        # Database connection frame
        db_frame = ctk.CTkFrame(backup_scrollable, corner_radius=15)
        db_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        db_frame.grid_columnconfigure(0, weight=1)

        db_title = ctk.CTkLabel(
            db_frame,
            text="🔗 Source Database Connection",
            font=self.create_font(size=16, weight="bold"),
        )
        db_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.backup_db_entry = ctk.CTkTextbox(
            db_frame, height=80, corner_radius=10, font=self.create_font(size=11)
        )
        self.backup_db_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))
        self.backup_db_entry.insert("0.0", self.default_source_db)

        # Add hint text
        db_hint = ctk.CTkLabel(
            db_frame,
            text="💡 Format: postgresql://username:password@host:port/database",
            font=self.create_font(size=10),
            text_color=("gray60", "gray40"),
        )
        db_hint.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        # Test connection button frame
        test_frame = ctk.CTkFrame(db_frame, fg_color="transparent")
        test_frame.grid(row=3, column=0, pady=(5, 20))
        test_frame.grid_columnconfigure(0, weight=1)

        # Button container for better alignment
        button_container = ctk.CTkFrame(test_frame, fg_color="transparent")
        button_container.grid(row=0, column=0)

        test_backup_btn = ctk.CTkButton(
            button_container,
            text="🔍 Test Connection",
            command=lambda: self.test_connection("backup"),
            height=35,
            width=140,
            corner_radius=8,
            font=self.create_font(size=12, weight="bold"),
        )
        test_backup_btn.grid(row=0, column=0, padx=(0, 10))

        clear_backup_btn = ctk.CTkButton(
            button_container,
            text="🗑 Clear",
            command=lambda: self.clear_connection("backup"),
            height=35,
            width=85,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
            fg_color=("#d32f2f", "#b71c1c"),
            hover_color=("#b71c1c", "#d32f2f"),
            anchor="center",
        )
        clear_backup_btn.grid(row=0, column=1, padx=(0, 0))

        # File settings frame
        file_frame = ctk.CTkFrame(backup_scrollable, corner_radius=15)
        file_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)

        file_title = ctk.CTkLabel(
            file_frame,
            text="📁 Backup File Settings",
            font=self.create_font(size=16, weight="bold"),
        )
        file_title.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 15)
        )

        # Save location
        location_label = ctk.CTkLabel(
            file_frame, text="Save Location:", font=self.create_font(size=12)
        )
        location_label.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(0, 10))

        self.backup_location_var = ctk.StringVar(value=self.save_location)
        self.backup_location_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.backup_location_var,
            height=35,
            corner_radius=8,
            font=self.create_font(size=11),
            state="readonly",
        )
        self.backup_location_entry.grid(
            row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 10)
        )

        backup_browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse",
            command=lambda: self.browse_location("backup"),
            width=100,
            height=35,
            corner_radius=8,
            font=self.create_font(size=12, weight="bold"),
        )
        backup_browse_btn.grid(row=1, column=2, padx=(0, 20), pady=(0, 10))

        # Filename with controls
        filename_label = ctk.CTkLabel(
            file_frame, text="Filename:", font=self.create_font(size=12)
        )
        filename_label.grid(row=2, column=0, sticky="w", padx=(20, 10), pady=(0, 5))

        filename_controls_frame = ctk.CTkFrame(file_frame)
        filename_controls_frame.grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=(20, 20), pady=(0, 10)
        )
        filename_controls_frame.grid_columnconfigure(0, weight=1)

        self.backup_filename_var = ctk.StringVar(
            value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
        )
        self.backup_filename_entry = ctk.CTkEntry(
            filename_controls_frame,
            textvariable=self.backup_filename_var,
            height=35,
            corner_radius=8,
            font=self.create_font(size=11),
            placeholder_text="Enter filename for backup (e.g., mybackup.dump)",
        )
        self.backup_filename_entry.grid(
            row=0, column=0, sticky="ew", padx=(10, 5), pady=10
        )

        # Auto-generate filename button
        auto_filename_btn = ctk.CTkButton(
            filename_controls_frame,
            text="🔄 Auto",
            command=self.generate_auto_filename,
            width=70,
            height=35,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
        )
        auto_filename_btn.grid(row=0, column=1, padx=(5, 10), pady=10)

        # Filename hint
        filename_hint = ctk.CTkLabel(
            file_frame,
            text="💡 Tip: Filename will automatically get .dump extension if not specified",
            font=self.create_font(size=10),
            text_color=("gray60", "gray40"),
        )
        filename_hint.grid(
            row=4, column=0, columnspan=3, sticky="w", padx=(20, 20), pady=(0, 20)
        )

        # Backup operation frame
        backup_op_frame = ctk.CTkFrame(backup_scrollable, corner_radius=15)
        backup_op_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        backup_op_frame.grid_columnconfigure(0, weight=1)

        backup_op_title = ctk.CTkLabel(
            backup_op_frame,
            text="🚀 Backup Operation",
            font=self.create_font(size=16, weight="bold"),
        )
        backup_op_title.grid(row=0, column=0, pady=(20, 20))

        # Backup button
        self.backup_btn = ctk.CTkButton(
            backup_op_frame,
            text="💾 Start Backup\n(pg_dump)",
            command=self.backup_database,
            height=80,
            corner_radius=12,
            font=self.create_font(size=16, weight="bold"),
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#14375e", "#1f538d"),
        )
        self.backup_btn.grid(row=1, column=0, padx=20, pady=(0, 30), sticky="ew")

    def setup_restore_tab(self):
        # Restore tab
        self.restore_tab = self.tabview.add("📤 Restore")
        self.restore_tab.grid_columnconfigure(0, weight=1)
        self.restore_tab.grid_rowconfigure(0, weight=1)

        # Create scrollable frame for restore content
        restore_scrollable = ctk.CTkScrollableFrame(
            self.restore_tab,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=("gray75", "gray25"),
            scrollbar_button_hover_color=("gray64", "gray35"),
        )
        restore_scrollable.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        restore_scrollable.grid_columnconfigure(0, weight=1)

        # Database connection frame
        db_frame = ctk.CTkFrame(restore_scrollable, corner_radius=15)
        db_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        db_frame.grid_columnconfigure(0, weight=1)

        db_title = ctk.CTkLabel(
            db_frame,
            text="🔗 Target Database Connection",
            font=self.create_font(size=16, weight="bold"),
        )
        db_title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        self.restore_db_entry = ctk.CTkTextbox(
            db_frame, height=80, corner_radius=10, font=self.create_font(size=11)
        )
        self.restore_db_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))
        self.restore_db_entry.insert("0.0", self.default_target_db)

        # Add hint text
        db_hint = ctk.CTkLabel(
            db_frame,
            text="💡 Format: postgresql://username:password@host:port/database",
            font=self.create_font(size=10),
            text_color=("gray60", "gray40"),
        )
        db_hint.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        # Test connection button frame
        test_frame = ctk.CTkFrame(db_frame, fg_color="transparent")
        test_frame.grid(row=3, column=0, pady=(5, 20))
        test_frame.grid_columnconfigure(0, weight=1)

        # Button container for better alignment
        button_container = ctk.CTkFrame(test_frame, fg_color="transparent")
        button_container.grid(row=0, column=0)

        test_restore_btn = ctk.CTkButton(
            button_container,
            text="🔍 Test Connection",
            command=lambda: self.test_connection("restore"),
            height=35,
            width=140,
            corner_radius=8,
            font=self.create_font(size=12, weight="bold"),
        )
        test_restore_btn.grid(row=0, column=0, padx=(0, 10))

        clear_restore_btn = ctk.CTkButton(
            button_container,
            text="🗑 Clear",
            command=lambda: self.clear_connection("restore"),
            height=35,
            width=85,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
            fg_color=("#d32f2f", "#b71c1c"),
            hover_color=("#b71c1c", "#d32f2f"),
            anchor="center",
        )
        clear_restore_btn.grid(row=0, column=1, padx=(0, 0))

        # File selection frame
        file_frame = ctk.CTkFrame(restore_scrollable, corner_radius=15)
        file_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)

        file_title = ctk.CTkLabel(
            file_frame,
            text="📁 Restore File Selection",
            font=self.create_font(size=16, weight="bold"),
        )
        file_title.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 15)
        )

        # File path
        file_label = ctk.CTkLabel(
            file_frame, text="Dump File:", font=self.create_font(size=12)
        )
        file_label.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(0, 20))

        self.restore_file_var = ctk.StringVar(value="")
        self.restore_file_entry = ctk.CTkEntry(
            file_frame,
            textvariable=self.restore_file_var,
            height=35,
            corner_radius=8,
            font=self.create_font(size=11),
            placeholder_text="Select a dump file to restore...",
            state="readonly",
        )
        self.restore_file_entry.grid(
            row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 20)
        )

        select_file_btn = ctk.CTkButton(
            file_frame,
            text="📂 Select File",
            command=self.select_restore_file,
            width=100,
            height=35,
            corner_radius=8,
            font=self.create_font(size=12, weight="bold"),
        )
        select_file_btn.grid(row=1, column=2, padx=(0, 20), pady=(0, 20))

        # Restore operation frame
        restore_op_frame = ctk.CTkFrame(restore_scrollable, corner_radius=15)
        restore_op_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        restore_op_frame.grid_columnconfigure(0, weight=1)

        restore_op_title = ctk.CTkLabel(
            restore_op_frame,
            text="🚀 Restore Operation",
            font=self.create_font(size=16, weight="bold"),
        )
        restore_op_title.grid(row=0, column=0, pady=(20, 20))

        # Restore button
        self.restore_btn = ctk.CTkButton(
            restore_op_frame,
            text="📤 Start Restore\n(pg_restore)",
            command=self.restore_database,
            height=80,
            corner_radius=12,
            font=self.create_font(size=16, weight="bold"),
            fg_color=("#1f8d53", "#145e35"),
            hover_color=("#145e35", "#1f8d53"),
        )
        self.restore_btn.grid(row=1, column=0, padx=20, pady=(0, 30), sticky="ew")

    def setup_history_tab(self):
        # History tab
        self.history_tab = self.tabview.add("📋 History")
        self.history_tab.grid_columnconfigure(0, weight=1)
        self.history_tab.grid_rowconfigure(1, weight=1)

        # History header
        history_header = ctk.CTkFrame(
            self.history_tab, corner_radius=15, fg_color="transparent"
        )
        history_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        history_header.grid_columnconfigure(0, weight=1)

        history_title = ctk.CTkLabel(
            history_header,
            text="📊 Operation History",
            font=self.create_font(size=16, weight="bold"),
        )
        history_title.grid(row=0, column=0, pady=15)

        # History buttons
        history_btn_frame = ctk.CTkFrame(history_header, fg_color="transparent")
        history_btn_frame.grid(row=1, column=0, pady=(0, 15))

        clear_btn = ctk.CTkButton(
            history_btn_frame,
            text="🗑 Clear History",
            command=self.clear_history,
            height=32,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
            fg_color=("#d32f2f", "#b71c1c"),
            hover_color=("#b71c1c", "#d32f2f"),
        )
        clear_btn.grid(row=0, column=0, padx=(10, 5), pady=5)

        refresh_btn = ctk.CTkButton(
            history_btn_frame,
            text="🔄 Refresh",
            command=self.update_history_display,
            height=32,
            corner_radius=8,
            font=self.create_font(size=11, weight="bold"),
        )
        refresh_btn.grid(row=0, column=1, padx=(5, 10), pady=5)

        # History display
        self.history_textbox = ctk.CTkTextbox(
            self.history_tab,
            corner_radius=15,
            font=self.create_font(size=11),
            wrap="word",
        )
        self.history_textbox.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.update_history_display()

    def test_connection(self, tab_type):
        """Test database connection"""
        # Check if psql is available
        psql_available = (
            self.postgres_checker.postgres_status["commands_available"]
            .get("psql", {})
            .get("available", False)
        )
        if not psql_available:
            messagebox.showerror(
                "PostgreSQL Not Available",
                "❌ PostgreSQL psql command is not available!\n\n"
                "Connection testing requires psql to be installed and in your PATH.\n"
                "Click '🔧 Check PostgreSQL' button to diagnose and fix the issue.",
            )
            return

        if tab_type == "backup":
            conn_string = self.backup_db_entry.get("0.0", "end-1c").strip()
            title = "Source Database"
        else:
            conn_string = self.restore_db_entry.get("0.0", "end-1c").strip()
            title = "Target Database"

        if not self.validate_connection_string(conn_string, title):
            return

        def test_conn():
            try:
                self.progress_bar.set(0.5)
                self.status_var.set(f"Testing {title.lower()} connection...")

                # Use psql to test connection
                cmd = ["psql", conn_string, "-c", "SELECT 1;"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

                if result.returncode == 0:
                    messagebox.showinfo(
                        "Connection Test",
                        f"✅ {title} connection successful!\n\nConnection is working properly.",
                    )
                    self.status_var.set(f"✅ {title} connection test passed")
                else:
                    messagebox.showerror(
                        "Connection Test",
                        f"❌ {title} connection failed!\n\nError details:\n{result.stderr}",
                    )
                    self.status_var.set(f"❌ {title} connection test failed")

            except subprocess.TimeoutExpired:
                messagebox.showerror(
                    "Connection Test",
                    f"⏱️ {title} connection test timed out!\n\nThe connection attempt took too long.",
                )
                self.status_var.set("⏱️ Connection test timed out")
            except FileNotFoundError:
                messagebox.showerror(
                    "Error",
                    "❌ psql not found!\n\nPlease ensure PostgreSQL client tools are installed and added to your system PATH.",
                )
                self.status_var.set("❌ psql not found")
            except Exception as e:
                messagebox.showerror(
                    "Connection Test",
                    f"❌ Connection test error!\n\nError details:\n{str(e)}",
                )
                self.status_var.set("❌ Connection test error")
            finally:
                self.progress_bar.set(0)

        threading.Thread(target=test_conn, daemon=True).start()

    def clear_connection(self, tab_type):
        """Clear connection string"""
        if tab_type == "backup":
            confirm = messagebox.askyesno(
                "Clear Connection", "Clear the source database connection string?"
            )
            if confirm:
                self.backup_db_entry.delete("0.0", "end")
                self.status_var.set("🗑 Source database connection cleared")
        else:
            confirm = messagebox.askyesno(
                "Clear Connection", "Clear the target database connection string?"
            )
            if confirm:
                self.restore_db_entry.delete("0.0", "end")
                self.status_var.set("🗑 Target database connection cleared")

    def generate_auto_filename(self):
        """Generate automatic filename with timestamp"""
        new_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
        self.backup_filename_var.set(new_filename)
        self.status_var.set("🔄 Auto-generated filename with current timestamp")

    def validate_connection_string(self, conn_string, db_type):
        """Enhanced validation for connection string"""
        if not conn_string:
            messagebox.showerror(
                "Validation Error",
                f"❌ {db_type} connection string is empty!\n\nPlease enter a valid PostgreSQL connection string.\n\nFormat: postgresql://username:password@host:port/database",
            )
            return False

        if not conn_string.startswith("postgresql://"):
            messagebox.showerror(
                "Validation Error",
                f"❌ Invalid {db_type} connection string format!\n\nConnection string must start with 'postgresql://'\n\nCorrect format:\npostgresql://username:password@host:port/database",
            )
            return False

        # Additional validation for basic structure
        try:
            # Check if the connection string has the basic components
            if "@" not in conn_string or "/" not in conn_string.split("@")[1]:
                messagebox.showerror(
                    "Validation Error",
                    f"❌ Incomplete {db_type} connection string!\n\nThe connection string appears to be missing required components.\n\nRequired format:\npostgresql://username:password@host:port/database",
                )
                return False
        except Exception:
            messagebox.showerror(
                "Validation Error",
                f"❌ Malformed {db_type} connection string!\n\nPlease check the connection string format.\n\nRequired format:\npostgresql://username:password@host:port/database",
            )
            return False

        return True

    def browse_location(self, tab_type):
        """Browse for save location"""
        if tab_type == "backup":
            current_location = self.backup_location_var.get()
        else:
            current_location = self.save_location

        folder = filedialog.askdirectory(initialdir=current_location)
        if folder:
            if tab_type == "backup":
                self.backup_location_var.set(folder)
                self.status_var.set(
                    f"📁 Backup save location updated: {os.path.basename(folder)}"
                )
                # Save the new location as default
                self.save_location = folder
                self.save_settings()
            else:
                self.save_location = folder
                self.save_settings()
                self.status_var.set(
                    f"📁 Save location updated: {os.path.basename(folder)}"
                )

    def select_restore_file(self):
        """Select file for restore operation"""
        file_path = filedialog.askopenfilename(
            title="Select dump file to restore",
            filetypes=[
                ("Dump files", "*.dump"),
                ("SQL files", "*.sql"),
                ("All files", "*.*"),
            ],
            initialdir=self.save_location,
        )

        if file_path:
            self.restore_file_var.set(file_path)
            self.status_var.set(
                f"📁 Selected restore file: {os.path.basename(file_path)}"
            )

    def check_file_exists(self, filepath, filename):
        """Check if file exists and show warning with detailed confirmation"""
        if os.path.exists(filepath):
            # Get file info
            file_size = self.get_file_size(filepath)
            file_modified = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            result = messagebox.askyesno(
                "⚠️ File Already Exists - Confirmation Required",
                f"The file '{filename}' already exists in the selected location.\n\n"
                f"📁 Location: {os.path.dirname(filepath)}\n"
                f"📊 Current file size: {file_size}\n"
                f"🕒 Last modified: {file_modified}\n\n"
                f"❓ Do you want to overwrite this existing file?\n\n"
                f"⚠️ Warning: This action will permanently replace the existing backup file with new data.\n"
                f"The original file will be lost and cannot be recovered.\n\n"
                f"Choose:\n"
                f"• YES - Overwrite the existing file\n"
                f"• NO - Cancel operation and choose a different filename",
                icon="warning",
            )
            return result
        return True

    def backup_database(self):
        # Check PostgreSQL availability first
        if not self.postgres_checker.postgres_status["installed"]:
            messagebox.showerror(
                "PostgreSQL Not Available",
                "❌ PostgreSQL pg_dump command is not available!\n\n"
                "Click '🔧 Check PostgreSQL' button to diagnose and fix the issue.",
            )
            return

        # Get and validate inputs
        source_db = self.backup_db_entry.get("0.0", "end-1c").strip()
        if not self.validate_connection_string(source_db, "Source database"):
            return

        filename = self.backup_filename_var.get().strip()
        if not filename:
            messagebox.showerror(
                "Validation Error", "❌ Please enter a filename for the backup!"
            )
            return

        # Enhanced filename validation
        if not filename:
            messagebox.showerror(
                "Validation Error",
                "❌ Filename cannot be empty!\n\nPlease enter a valid filename for the backup.",
            )
            return

        # Check for invalid characters in filename
        invalid_chars = '<>:"/\\|?*'
        if any(char in filename for char in invalid_chars):
            messagebox.showerror(
                "Validation Error",
                f"❌ Invalid characters in filename!\n\nFilename cannot contain: {invalid_chars}\n\nPlease use a valid filename.",
            )
            return

        # Ensure .dump extension
        if not filename.lower().endswith((".dump", ".sql")):
            filename += ".dump"
            self.backup_filename_var.set(filename)

        save_location = self.backup_location_var.get()
        if not save_location or not os.path.exists(save_location):
            messagebox.showerror(
                "Validation Error",
                "❌ Invalid save location!\n\nPlease select a valid directory to save the backup.",
            )
            return

        filepath = os.path.join(save_location, filename)

        # Enhanced file existence check
        if not self.check_file_exists(filepath, filename):
            return

        def run_backup():
            try:
                # Disable button and show progress
                self.backup_btn.configure(state="disabled")
                self.progress_bar.configure(mode="indeterminate")
                self.progress_bar.start()
                self.status_var.set("🔄 Running backup operation...")

                # pg_dump command
                cmd = [
                    "pg_dump",
                    "-Fc",
                    "-d",
                    source_db,
                    "--no-owner",
                    "--no-acl",
                    "-f",
                    filepath,
                ]

                # Run the command
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    self.status_var.set("✅ Backup completed successfully!")
                    self.add_to_history(
                        "BACKUP", f"Success: {filename}", filepath, source_db
                    )
                    messagebox.showinfo(
                        "Backup Success",
                        f"✅ Backup completed successfully!\n\n📁 Saved to:\n{filepath}\n\n📊 File size: {self.get_file_size(filepath)}",
                    )

                    # Update filename with new timestamp for next backup
                    new_filename = (
                        f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.dump"
                    )
                    self.backup_filename_var.set(new_filename)
                else:
                    error_msg = result.stderr or "Unknown error occurred"
                    self.status_var.set("❌ Backup failed!")
                    self.add_to_history(
                        "BACKUP", f"Failed: {error_msg[:100]}...", "", source_db
                    )
                    show_error_dialog(
                        self.root,
                        "Backup Failed",
                        f"❌ Backup operation failed!\n\nError details:\n{error_msg}",
                        font_family=self.font_family,
                    )

            except FileNotFoundError:
                error_msg = "pg_dump not found. Please ensure PostgreSQL is installed and added to PATH."
                self.status_var.set("❌ pg_dump not found")
                self.add_to_history("BACKUP", f"Error: {error_msg}", "", source_db)
                show_error_dialog(
                    self.root, "Error", f"❌ {error_msg}", font_family=self.font_family
                )
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.status_var.set("❌ Backup failed!")
                self.add_to_history("BACKUP", f"Error: {error_msg}", "", source_db)
                show_error_dialog(
                    self.root, "Error", f"❌ {error_msg}", font_family=self.font_family
                )
            finally:
                self.progress_bar.stop()
                self.progress_bar.set(0)
                self.backup_btn.configure(state="normal")

        threading.Thread(target=run_backup, daemon=True).start()

    def restore_database(self):
        # Check PostgreSQL availability first
        if not self.postgres_checker.postgres_status["installed"]:
            messagebox.showerror(
                "PostgreSQL Not Available",
                "❌ PostgreSQL pg_restore command is not available!\n\n"
                "Click '🔧 Check PostgreSQL' button to diagnose and fix the issue.",
            )
            return

        # Get and validate inputs
        target_db = self.restore_db_entry.get("0.0", "end-1c").strip()
        if not self.validate_connection_string(target_db, "Target database"):
            return

        dump_file = self.restore_file_var.get().strip()
        if not dump_file:
            messagebox.showerror(
                "Validation Error",
                "❌ Please select a dump file to restore!\n\nClick 'Select File' to choose a backup file.",
            )
            return

        if not os.path.exists(dump_file):
            messagebox.showerror(
                "File Error",
                f"❌ The selected dump file does not exist!\n\nFile: {dump_file}\n\nPlease select a valid backup file.",
            )
            return

        # Check file size and accessibility
        try:
            file_size = os.path.getsize(dump_file)
            if file_size == 0:
                messagebox.showerror(
                    "File Error",
                    f"❌ The selected dump file is empty!\n\nFile: {os.path.basename(dump_file)}\n\nPlease select a valid backup file with data.",
                )
                return
        except Exception as e:
            messagebox.showerror(
                "File Error",
                f"❌ Cannot access the dump file!\n\nFile: {os.path.basename(dump_file)}\nError: {str(e)}\n\nPlease check file permissions and try again.",
            )
            return

        # Enhanced confirmation dialog with more details
        file_info = f"📁 File: {os.path.basename(dump_file)}\n📊 Size: {self.get_file_size(dump_file)}\n🕒 Modified: {datetime.fromtimestamp(os.path.getmtime(dump_file)).strftime('%Y-%m-%d %H:%M:%S')}"

        confirm = messagebox.askyesno(
            "⚠️ Confirm Restore Operation",
            f"Are you sure you want to restore the database?\n\n"
            f"🎯 Target Database:\n{target_db[:80]}{'...' if len(target_db) > 80 else ''}\n\n"
            f"📁 Source File Details:\n{file_info}\n\n"
            f"⚠️ IMPORTANT WARNING:\n"
            f"• This operation may overwrite existing data in the target database\n"
            f"• The process cannot be undone automatically\n"
            f"• Make sure you have a backup of the target database if needed\n\n"
            f"Do you want to proceed with the restore?",
            icon="warning",
        )

        if not confirm:
            self.status_var.set("🚫 Restore operation cancelled by user")
            return

        def run_restore():
            try:
                # Disable button and show progress
                self.restore_btn.configure(state="disabled")
                self.progress_bar.configure(mode="indeterminate")
                self.progress_bar.start()
                self.status_var.set("🔄 Running restore operation...")

                # pg_restore command
                cmd = [
                    "pg_restore",
                    "--no-owner",
                    "--no-acl",
                    "-d",
                    target_db,
                    "-v",
                    dump_file,
                ]

                # Run the command
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    self.status_var.set("✅ Restore completed successfully!")
                    self.add_to_history(
                        "RESTORE",
                        f"Success: {os.path.basename(dump_file)}",
                        dump_file,
                        target_db,
                    )
                    messagebox.showinfo(
                        "Restore Success",
                        f"✅ Restore completed successfully!\n\n📁 Restored from:\n{dump_file}\n\n🎯 Target database updated successfully.",
                    )
                else:
                    error_msg = result.stderr or "Unknown error occurred"
                    self.status_var.set("❌ Restore failed!")
                    self.add_to_history(
                        "RESTORE", f"Failed: {error_msg[:100]}...", dump_file, target_db
                    )
                    show_error_dialog(
                        self.root,
                        "Restore Failed",
                        f"❌ Restore operation failed!\n\nError details:\n{error_msg}",
                        font_family=self.font_family,
                    )

            except FileNotFoundError:
                error_msg = "pg_restore not found. Please ensure PostgreSQL is installed and added to PATH."
                self.status_var.set("❌ pg_restore not found")
                self.add_to_history(
                    "RESTORE", f"Error: {error_msg}", dump_file, target_db
                )
                show_error_dialog(
                    self.root, "Error", f"❌ {error_msg}", font_family=self.font_family
                )
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.status_var.set("❌ Restore failed!")
                self.add_to_history(
                    "RESTORE", f"Error: {error_msg}", dump_file, target_db
                )
                show_error_dialog(
                    self.root, "Error", f"❌ {error_msg}", font_family=self.font_family
                )
            finally:
                self.progress_bar.stop()
                self.progress_bar.set(0)
                self.restore_btn.configure(state="normal")

        threading.Thread(target=run_restore, daemon=True).start()

    def get_file_size(self, filepath):
        """Get human-readable file size"""
        try:
            size = os.path.getsize(filepath)
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"

    def add_to_history(self, operation, status, file_path, db_string=""):
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operation": operation,
            "status": status,
            "file_path": file_path,
            "database": db_string[:50] + "..." if len(db_string) > 50 else db_string,
        }

        self.history.append(entry)
        self.save_history()
        self.update_history_display()

    def load_history(self):
        """Load operation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except:
            self.history = []

    def save_history(self):
        """Save operation history to file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f, indent=2)
        except:
            pass

    def load_settings(self):
        """Load application settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                    self.save_location = settings.get(
                        "save_location", self.save_location
                    )
            else:
                self.settings = {}
        except:
            self.settings = {}

    def save_settings(self):
        """Save application settings to file"""
        try:
            settings = {"save_location": self.save_location}
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=2)
        except:
            pass

    def clear_history(self):
        """Clear operation history"""
        if messagebox.askyesno(
            "Clear History", "Are you sure you want to clear all operation history?"
        ):
            self.history = []
            self.save_history()
            self.update_history_display()
            self.status_var.set("🗑 History cleared")

    def update_history_display(self):
        """Update history display in the textbox"""
        self.history_textbox.delete("0.0", "end")

        if not self.history:
            self.history_textbox.insert(
                "0.0",
                "📋 No operations recorded yet.\n\nPerform backup or restore operations to see them here.",
            )
            return

        history_text = "📊 DATABASE OPERATIONS HISTORY\n"
        history_text += "=" * 50 + "\n\n"

        for i, entry in enumerate(
            reversed(self.history[-50:]), 1
        ):  # Show last 50 entries
            timestamp = entry.get("timestamp", "Unknown")
            operation = entry.get("operation", "Unknown")
            status = entry.get("status", "Unknown")
            file_path = entry.get("file_path", "N/A")
            database = entry.get("database", "N/A")

            history_text += f"#{i:02d} {operation} - {timestamp}\n"
            history_text += f"    Status: {status}\n"
            history_text += (
                f"    File: {os.path.basename(file_path) if file_path else 'N/A'}\n"
            )
            history_text += f"    Database: {database}\n"
            history_text += "-" * 40 + "\n\n"

        self.history_textbox.insert("0.0", history_text)


def main():
    app = ModernDatabaseManager()

    # Print application data directory information
    print(f"📁 Application data directory: {app.get_app_data_directory()}")
    print("💾 History and settings will be saved in Documents folder")

    app.root.mainloop()


if __name__ == "__main__":
    main()
