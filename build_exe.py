import os
import subprocess
import sys
import shutil
import platform


def get_platform_info():
    """Get current platform information"""
    system = platform.system()
    return {
        'system': system,
        'is_windows': system == 'Windows',
        'is_mac': system == 'Darwin',
        'is_linux': system == 'Linux'
    }


def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller

        print("✅ PyInstaller is already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "pyinstaller"]
            )
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            return False


def check_upx_available():
    """Check if UPX compressor is available"""
    try:
        result = subprocess.run(["upx", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ UPX compressor found - will enable compression")
            return True
    except FileNotFoundError:
        pass

    print(
        "💡 UPX compressor not found - download from https://upx.github.io/ for smaller files"
    )
    return False


def build_executable():
    """Build the executable using PyInstaller"""
    plat = get_platform_info()
    print(f"🔨 Building optimized executable for {plat['system']}...")

    # Check for UPX compressor
    upx_available = check_upx_available()

    # Get the PyInstaller path from the virtual environment
    if plat['is_windows']:
        pyinstaller_path = os.path.join(os.path.dirname(sys.executable), "pyinstaller.exe")
    else:
        pyinstaller_path = os.path.join(os.path.dirname(sys.executable), "pyinstaller")

    if not os.path.exists(pyinstaller_path):
        pyinstaller_path = "pyinstaller"  # Fallback to system PATH

    # Base PyInstaller command with optimization options
    cmd = [
        pyinstaller_path,
        "--onefile",  # Create a single executable file
        "--windowed",  # Hide console window (GUI app)
        "--name=PostgreSQL_Database_Manager",  # Name of the executable
        "--optimize=2",  # Maximum Python optimization
        "--strip",  # Strip debug symbols (Linux/macOS, ignored on Windows)
        "--exclude-module=tkinter.test",  # Exclude test modules
        "--exclude-module=test",  # Exclude test modules
        "--exclude-module=unittest",  # Exclude unittest
        "--exclude-module=doctest",  # Exclude doctest
        "--exclude-module=pdb",  # Exclude debugger
        "--exclude-module=pydoc",  # Exclude documentation
        "--exclude-module=email",  # Exclude email module (not used)
        "--exclude-module=xml",  # Exclude XML modules (not used)
        "--exclude-module=urllib",  # Exclude urllib (not used)
        "--exclude-module=http",  # Exclude http modules (not used)
        "--exclude-module=ssl",  # Exclude SSL (not used for local DB ops)
        "--exclude-module=socket",  # Exclude socket (not used)
        "--exclude-module=select",  # Exclude select (not used)
        "--exclude-module=multiprocessing",  # Exclude multiprocessing
        "--exclude-module=concurrent",  # Exclude concurrent.futures
    ]

    # Platform-specific options
    if plat['is_windows']:
        # Windows-specific icon and admin privileges
        if os.path.exists("icon/app-icon.ico"):
            cmd.append("--icon=icon/app-icon.ico")
        cmd.append("--uac-admin")  # Request administrator privileges
        print("🪟 Windows build with UAC admin privileges")
    elif plat['is_mac']:
        # macOS-specific icon
        if os.path.exists("icon/app-icon.icns"):
            cmd.append("--icon=icon/app-icon.icns")
            print("🍎 macOS build with .icns icon")
        elif os.path.exists("icon/app-icon.ico"):
            print("💡 Note: Convert .ico to .icns for proper macOS icon")
            print("   Run: sips -s format icns icon/app-icon.ico --out icon/app-icon.icns")
    elif plat['is_linux']:
        # Linux-specific icon
        if os.path.exists("icon/app-icon.png"):
            cmd.append("--icon=icon/app-icon.png")
        print("🐧 Linux build")

    # Add UPX compression if available
    if upx_available:
        cmd.append("--upx-dir=.")  # Use UPX from current directory or PATH
        print("🗜️ UPX compression enabled")
    else:
        cmd.append("--noupx")  # Disable UPX if not available
        print("📦 Building without UPX compression")

    # Add the main script
    cmd.append("db_manager.py")

    # Add manifest file if it exists (Windows only)
    if plat['is_windows'] and os.path.exists("app.manifest"):
        cmd.insert(-1, "--manifest=app.manifest")
        print("🛡️ Including administrator manifest")

    # Add data files only if they exist (use appropriate separator)
    data_separator = ";" if plat['is_windows'] else ":"
    if os.path.exists("db_operations_history.json"):
        cmd.insert(-1, f"--add-data=db_operations_history.json{data_separator}.")
        print("📄 Including existing history file")

    try:
        print("🔄 Starting PyInstaller build process...")
        print("📝 Build command:", " ".join(cmd))
        print("-" * 60)

        # Run PyInstaller with real-time output
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True, (platform-specific extension)
            plat = get_platform_info()
            if plat['is_windows']:
                exe_name = "PostgreSQL_Database_Manager.exe"
            else:
                exe_name = "PostgreSQL_Database_Manager"

            exe_path = os.path.join("dist", exe_name
            universal_newlines=True,
        )

        # Print output in real-time
        output_lines = []
        if process.stdout:
            while True:
                output = process.stdout.readline()
                if output == "" and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    output_lines.append(output.strip())

        # Wait for process to complete
        return_code = process.wait()

        print("-" * 60)

        if return_code == 0:
            print("✅ Build completed successfully!")
            print("📁 Executable created in 'dist' folder")

            # Check if executable was created
            exe_path = os.path.join("dist", "PostgreSQL_Database_Manager.exe")
            if os.path.exists(exe_path):
                file_size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"🎯 Executable location: {os.path.abspath(exe_path)}")
                print(f"📊 Optimized file size: {file_size_mb:.1f} MB")

                # Show optimization summary
                print("\n🚀 Optimization features enabled:")
                print("   ✅ Python bytecode optimization (--optimize=2)")
                print("   ✅ Excluded unused modules (test, email, xml, etc.)")
                if check_upx_available():
                    print("   ✅ UPX compression enabled")
                else:
                    print(
                        "   💡 UPX compression not available (install UPX for ~30% smaller files)"
                    )

                return True
            else:
                print("❌ Executable not found in expected location")
                return False
        else:
            print("❌ Build failed!")
            print(f"❌ Process exited with code: {return_code}")
            return False

    except FileNotFoundError:
        print("❌ PyInstaller not found. Please install it first.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def cleanlat = get_platform_info()
        print("\n🎉 Optimized build process completed successfully!")
        print("💡 You can now run the executable from the 'dist' folder")

        # Ask if user wants to clean up
        clean_up = input("\n🧹 Do you want to clean up build files? (y/n): ").lower()
        if clean_up in ["y", "yes"]:
            clean_build_files()

        print("\n📋 Summary:")
        if plat['is_windows']:
            exe_name = "PostgreSQL_Database_Manager.exe"
            print(f"- Executable: dist/{exe_name}")
            print("- Runs with administrator privileges")
            print("- Double-click to run (will prompt for admin access)")
        elif plat['is_mac']:
            exe_name = "PostgreSQL_Database_Manager"
            print(f"- Executable: dist/{exe_name}")
            print("- Run with: sudo ./dist/PostgreSQL_Database_Manager")
            print("- Or grant permissions: chmod +x ./dist/PostgreSQL_Database_Manager")
        else:
            exe_name = "PostgreSQL_Database_Manager"
            print(f"- Executable: dist/{exe_name}")
            print("- Run with: sudo ./dist/PostgreSQL_Database_Manager")

        print("- Optimized and compressed for smaller file size
        print("✅ Removed spec file")


def main():
    print("🚀 PostgreSQL Database Manager - Optimized Executable Builder")
    print("=" * 60)

    # Check if main script exists
    if not os.path.exists("db_manager.py"):
        print("❌ db_manager.py not found in current directory")
        return

    # Install PyInstaller if needed
    if not install_pyinstaller():
        return

    # Build the executable
    if build_executable():
        print("\n🎉 Optimized build process completed successfully!")
        print("💡 You can now run the executable from the 'dist' folder")

        # Ask if user wants to clean up
        clean_up = input("\n🧹 Do you want to clean up build files? (y/n): ").lower()
        if clean_up in ["y", "yes"]:
            clean_build_files()

        print("\n📋 Summary:")
        print("- Executable: dist/PostgreSQL_Database_Manager.exe")
        print("- Optimized and compressed for smaller file size")
        print("- Runs with administrator privileges")
        print("- Double-click to run (will prompt for admin access)")
        print("- No Python installation required on target machines")

    else:
        print("\n❌ Build failed. Please check the errors above.")


if __name__ == "__main__":
    main()
