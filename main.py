import sys
import os
from kivy.config import Config

# Set screen size to match a typical Android device
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', False)
Config.write()

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kidsvoc import MyApp  # Importing the MyApp class from the kidsvoc module

def main():
    """Main entry point for the application."""
    # Create an instance of the MyApp class and start the application
    app = MyApp()
    app.run()

# Ensure that the main function is called only when this script is executed directly
if __name__ == '__main__':
    main()
