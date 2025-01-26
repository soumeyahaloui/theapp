import sys
import os
from kivy.metrics import dp
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kidsvoc import MyApp

def main():
    # Dynamically set configuration based on platform
    from kivy.utils import platform

    if platform in ['android', 'ios']:
        Config.set('graphics', 'resizable', True)  # Allow resizing for mobile platforms
        Config.set('graphics', 'fullscreen', 'auto')  # Enable fullscreen for mobile
    else:
        Config.set('graphics', 'width', '400')
        Config.set('graphics', 'height', '720')
        Config.set('graphics', 'resizable', True)  # Allow resizing for desktop
        Config.set('graphics', 'fullscreen', '0')

    Config.write()

    # Set dynamic window size for different platforms
    if platform in ['android', 'ios']:
        Window.size = (Window.width, Window.height)  # Use actual screen size for mobile
    else:
        Window.size = (400, 720)  # Default size for development

    Window.clearcolor = (0, 0, 0, 1)  # Reset window background to confirm redraw
    Window.canvas.ask_update()  # Ensure canvas is updated
    Clock.schedule_once(lambda dt: Window.canvas.ask_update(), 0.1)  # Already included, ensure it remains

    app = MyApp()
    app.run()


if __name__ == '__main__':
    main()
