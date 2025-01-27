import sys
import os
from kivy.config import Config

# Configure the screen size for Android devices
Config.set('graphics', 'resizable', False)  # Disable resizing
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '780')
Config.set('graphics', 'fullscreen', 'false')  # Ensure fullscreen works correctly
Config.write()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kidsvoc import MyApp  # Importing the MyApp class from the kidsvoc module

def main():
    """Main entry point for the application."""
    # Create an instance of the MyApp class and start the application
    app = MyApp()
    app.run()

# Ensure the script runs only when executed directly
if __name__ == '__main__':
    main()