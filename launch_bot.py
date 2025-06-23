import os
import sys
import subprocess
import importlib.util

def check_dependency(module_name):
    """Check if a module is installed"""
    return importlib.util.find_spec(module_name) is not None

def main():
    print("==============================================")
    print("        🚀 Starting Trading Bot...")
    print("==============================================")
    
    # Check dependencies
    dependencies = ['flask', 'PIL', 'eel', 'pystray', 'plyer', 'binance']
    missing_deps = [dep for dep in dependencies if not check_dependency(dep)]
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install dependencies.")
            print("Please run: pip install -r requirements.txt")
            input("Press Enter to exit...")
            return 1
    
    # Launch the Trading Bot app
    try:
        import app
        app_instance = app.ElectronStyleApp()
        app_instance.run()
    except KeyboardInterrupt:
        print("\nTrading Bot was stopped by user.")
    except Exception as e:
        print(f"\nError running Trading Bot: {e}")
        input("Press Enter to exit...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())