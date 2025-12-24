import sys
import time
import threading
try:
    from gui import File2VideoApp
    import customtkinter
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_app():
    print("Initializing App...")
    app = File2VideoApp()
    print("App Initialized.")
    
    # Schedule destruction
    app.after(2000, lambda: app.destroy())
    print("Starting Mainloop (will exit in 2s)...")
    app.mainloop()
    print("Test Complete.")

if __name__ == "__main__":
    test_app()
