from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.resources import resource_find

# Screen 1: Welcome Screen
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background image
        self.add_widget(Image(source=resource_find('assets/images/backgrounds/bubbles.png'), 
                              allow_stretch=True, keep_ratio=False))

        # Layout and Start Button
        layout = FloatLayout()
        start_button = Button(
            text="Start",
            font_size="20sp",
            size_hint=(None, None),
            size=(200, 60),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=(0.2, 0.5, 0.8, 1)
        )
        layout.add_widget(start_button)
        self.add_widget(layout)


# Main App Class
class MyApp(App):
    def build(self):
        self.icon = resource_find('assets/images/icon/appkidicon.png')
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        return sm


# Run the App
if __name__ == '__main__':
    MyApp().run()
