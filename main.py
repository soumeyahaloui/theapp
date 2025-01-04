import sys
import os
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kidsvoc import MyApp  # Importing the main app class from your project

# Configure Kivy graphics settings
Config.set('graphics', 'resizable', False)  # Prevent resizing
Config.set('graphics', 'width', '400')      # Set fixed width
Config.set('graphics', 'height', '720')     # Set fixed height
Config.write()

# Set window size explicitly
Window.size = (400, 720)

# Function to refresh the window after the app starts
def refresh_window():
    Window.canvas.ask_update()  # Force the canvas to redraw
    Window.dispatch('on_resize', *Window.size)  # Trigger resize event for proper scaling

# Main function to run the app
def main():
    app = MyApp()
    # Schedule the refresh after the app starts
    Clock.schedule_once(lambda dt: refresh_window(), 0.1)
    app.run()

# Entry point of the script
if __name__ == '__main__':
    main()
