import os
import json
from kivy.app import App
from kivy.metrics import dp
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.carousel import Carousel
from kivy.clock import Clock

# Load the manifest file
with open('assets/manifest.json', 'r') as f:
    manifest = json.load(f)

class IconButton(ButtonBehavior, Image):
    """Custom button class with image behavior."""
    pass

class CustomButton(ButtonBehavior, FloatLayout):
    """Custom button with dynamic styling and text wrapping."""
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(20)])
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(
            text=text,
            font_size="20sp",
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=self.size,
            text_size=(self.width - dp(20), None),  # Enable text wrapping
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle',
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.label.bind(texture_size=self.adjust_height)
        self.add_widget(self.label)

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def adjust_height(self, *args):
        """Dynamically adjust the height based on text size."""
        self.size = (self.size[0], max(dp(50), self.label.texture_size[1] + dp(20)))

class FirstScreen(Screen):
    """The main screen displayed on app start."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_button = None
        self.init_ui()

    def init_ui(self):
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/purple.png'),
            allow_stretch=True, keep_ratio=False
        ))

        layout = FloatLayout()

        # Add settings button
        self.settings_button = IconButton(
            source='assets/images/icon/settings.png',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        layout.add_widget(self.settings_button)

        self.add_widget(layout)

class MyApp(App):
    """Main application class."""
    def build(self):
        # Set initial window properties
        Window.size = (400, 720)
        Window.clearcolor = (1, 1, 1, 1)

        # ScreenManager setup
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(FirstScreen(name='first'))
        return sm

if __name__ == '__main__':
    MyApp().run()
