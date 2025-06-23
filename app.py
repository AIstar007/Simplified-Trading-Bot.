import threading
import time
import sys
import os
from PIL import Image
from bot import app as flask_app

# Try to import optional dependencies with fallbacks
try:
    import pystray
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False
    print("pystray not available - system tray icon will be disabled")

try:
    from plyer import notification
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    print("plyer not available - desktop notifications will be disabled")

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("pywebview not available - falling back to browser mode")

class TradingBotDesktopApp:
    def __init__(self):
        self.flask_thread = None
        self.tray_icon = None
        self.running = True
        self.window = None
        
    def start_flask(self):
        """Start Flask app in a thread"""
        try:
            flask_app.run(debug=False, port=5000, use_reloader=False, threaded=True)
        except Exception as e:
            print(f"Flask startup error: {e}")

    def notify_startup(self):
        """Desktop notification"""
        if not NOTIFICATION_AVAILABLE:
            print("Desktop notifications not available - notification skipped")
            return
            
        try:
            notification.notify(
                title='💱 Trading Bot Started',
                message='Your Trading Bot is running as a desktop app!',
                timeout=5
            )
        except Exception as e:
            print(f"Notification failed: {e}")

    def create_tray_icon(self):
        """Create system tray icon"""
        if not PYSTRAY_AVAILABLE:
            print("Skipping tray icon creation - pystray not available")
            return
            
        def on_tray_exit(icon, item):
            print("Exit requested from tray")
            icon.stop()
            self.shutdown()
        
        def on_tray_show(icon, item):
            """Show/restore the main window"""
            if self.window and WEBVIEW_AVAILABLE:
                try:
                    # Try to bring window to front (this might not work on all platforms)
                    pass
                except:
                    pass
        
        try:
            # Try to load icon, fallback to default if not found
            try:
                icon_image = Image.open("icon.png")
            except Exception as e:
                print(f"Icon not found: {e}, using default")
                # Create a simple default icon
                icon_image = Image.new('RGB', (64, 64), color='blue')
            
            menu = pystray.Menu(
                pystray.MenuItem("Show", on_tray_show),
                pystray.MenuItem("Exit", on_tray_exit)
            )
            
            self.tray_icon = pystray.Icon("TradingBot", icon_image, menu=menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()
            
        except Exception as e:
            print(f"Tray icon error: {e}")

    def wait_for_flask(self, max_attempts=30):
        """Wait for Flask server to be ready"""
        import urllib.request
        import urllib.error
        
        for attempt in range(max_attempts):
            try:
                urllib.request.urlopen('http://127.0.0.1:5000', timeout=1)
                print("Flask server is ready!")
                return True
            except (urllib.error.URLError, urllib.error.HTTPError):
                if attempt < max_attempts - 1:
                    time.sleep(1)
                    continue
                else:
                    print("Flask server failed to start after 30 seconds")
                    return False
        return False

    def run_webview_app(self):
        """Run the app using PyWebView"""
        if not WEBVIEW_AVAILABLE:
            print("PyWebView not available - opening in browser instead")
            import webbrowser
            webbrowser.open("http://127.0.0.1:5000")
            # Keep the app running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.shutdown()
            return
            
        def on_window_closed():
            """Handle window close event"""
            print("Main window closed")
            self.shutdown()
        
        try:
            # Wait for Flask to be ready before creating window
            if not self.wait_for_flask():
                print("Cannot start desktop app - Flask server not ready")
                return
            
            # Create the main application window
            self.window = webview.create_window(
                title='Trading Bot',
                url='http://127.0.0.1:5000',
                width=1000,  # Normal width instead of 1200
                height=700,  # Normal height instead of 800
                resizable=True,
                min_size=(800, 500),
                maximized=False,
                on_top=False,
                shadow=True,
                background_color='#2c3e50'
            )
            
            # Set up window event handlers
            self.window.events.closed += on_window_closed
            
            print("Starting desktop application window...")
            
            # Start the webview (this blocks until window is closed)
            webview.start(debug=False, http_server=False)
            
        except Exception as e:
            print(f"PyWebView error: {e}")
            # Fallback to opening in browser
            import webbrowser
            webbrowser.open("http://127.0.0.1:5000")
            # Keep the app running
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.shutdown()

    def shutdown(self):
        """Clean shutdown of the application"""
        print("Shutting down Trading Bot...")
        self.running = False
        
        # Clean up tray icon
        if self.tray_icon and PYSTRAY_AVAILABLE:
            try:
                self.tray_icon.stop()
            except:
                pass
        
        # Clean up webview
        if WEBVIEW_AVAILABLE and self.window:
            try:
                webview.destroy_window(self.window)
            except:
                pass
                
        # Exit the application
        sys.exit(0)

    def run(self):
        """Main application entry point"""
        print("Starting Trading Bot Desktop Application...")
        print("Using PyWebView for native desktop experience")
        
        # 1. Start Flask server in background
        print("Starting Flask server...")
        self.flask_thread = threading.Thread(target=self.start_flask, daemon=True)
        self.flask_thread.start()
        
        # 2. Show notification
        self.notify_startup()
        
        # 3. Create system tray icon
        self.create_tray_icon()
        
        # 4. Start PyWebView desktop app (this will wait for Flask internally)
        self.run_webview_app()

if __name__ == '__main__':
    app = TradingBotDesktopApp()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
        app.shutdown()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)