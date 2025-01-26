import sys
import os
from kivy.metrics import dp
from kivy.config import Config
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kidsvoc import MyApp  # Import the main app class


def configure_app_window():
    """Configure the app's window settings."""
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '720')
    Config.set('graphics', 'resizable', False)
    Config.set('graphics', 'fullscreen', '0')
    Config.write()

    Window.size = (400, 720) 
    Window.clearcolor = (1, 1, 1, 1)

    if platform == 'android':
        # Ensure fullscreen and enforce the correct window size
        Clock.schedule_once(lambda dt: setattr(Window, "fullscreen", "auto"), 0.1)
        Clock.schedule_once(lambda dt: setattr(Window, "size", (Window.width, Window.height)), 0.2)

    Clock.schedule_once(lambda dt: Window.canvas.ask_update(), 0.3)

class LoadingScreen(Screen):
    """A screen to display the loading image."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.add_loading_image, 0.1)  # Delay loading the image

    def add_loading_image(self, *args):
        self.add_widget(Image(source="assets/images/backgrounds/loading.png", allow_stretch=True, keep_ratio=False))

    def on_enter(self):
        Clock.schedule_once(self.switch_to_main_app, 5)

    def switch_to_main_app(self, *args):
        self.manager.current = "main_app"


def main():
    """Main entry point of the application."""
    configure_app_window()

    sm = ScreenManager(transition=FadeTransition())
    sm.add_widget(LoadingScreen(name="loading"))

    app_root = MyApp().build()
    main_screen = Screen(name="main_app")
    main_screen.add_widget(app_root)
    sm.add_widget(main_screen)

    sm.current = "loading"

    from kivy.base import runTouchApp
    runTouchApp(sm)


if __name__ == '__main__':
    main()
