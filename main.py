import sys
import os
from kivy.metrics import dp
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

# Add the src directory to the path to ensure proper imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kidsvoc import MyApp  # Import the main app class


def configure_app_window():
    """Configure the app's window settings."""
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '720')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'fullscreen', '0')
    Config.write()

    Window.clearcolor = (1, 1, 1, 1)  # Set default white background

    if platform == 'android':
        Window.size = (Window.width, Window.height)
        Window.canvas.ask_update()  # Ensure canvas is updated
    Clock.schedule_once(lambda dt: Window.canvas.ask_update(), 0.1)  # Redraw for stability


class LoadingScreen(Screen):
    """A screen to display the loading image."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Image(source="assets/images/backgrounds/loading.png", allow_stretch=True, keep_ratio=False))

    def on_enter(self):
        # Simulate loading time, then transition to the main app
        Clock.schedule_once(self.switch_to_main_app, 3)  # Adjust time as needed

    def switch_to_main_app(self, *args):
        self.manager.current = "main_app"  # Switch to the main app screen


def main():
    """Main entry point of the application."""
    configure_app_window()

    # Setup ScreenManager
    sm = ScreenManager(transition=FadeTransition())

    # Add the loading screen
    sm.add_widget(LoadingScreen(name="loading"))

    # Wrap MyApp's root widget in a Screen and add it to ScreenManager
    app_root = MyApp().build()
    main_screen = Screen(name="main_app")
    main_screen.add_widget(app_root)
    sm.add_widget(main_screen)

    # Set the starting screen
    sm.current = "loading"

    # Run the app
    from kivy.base import runTouchApp
    runTouchApp(sm)



if __name__ == '__main__':
    main()
