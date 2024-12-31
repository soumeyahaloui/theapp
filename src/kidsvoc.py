import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image, CoreImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from PIL import Image as PILImage, ImageDraw, ImageFont
from io import BytesIO
from kivy.resources import resource_find
from kivy.config import Config
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()

with open('assets/manifest.json', 'r') as f:
    manifest = json.load(f)

class IconButton(ButtonBehavior, Image):
    pass

class CustomButton(ButtonBehavior, FloatLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)

        # Background with rounded corners
        with self.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # Background color
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(20)])
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Add the text label, ensuring proper alignment
        self.label = Label(
            text=text,
            font_size="20sp",
            color=(1, 1, 1, 1),  # White text color
            size_hint=(None, None),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle',
        )
        self.label.bind(size=self.label.setter('text_size'))  # Ensure text is properly centered
        self.add_widget(self.label)

    def update_bg(self, *args):
        """Update the background size and position."""
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background image
        self.add_widget(Image(
            source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][1]}'),
            allow_stretch=True, keep_ratio=False
        ))

        # Layout
        layout = FloatLayout()

        # Start Button
        start_button = CustomButton(
            text="Start",
            size_hint=(None, None),
            size=(dp(240), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))

        layout.add_widget(start_button)

        # Settings Icon (Gear Button)
        settings_button = IconButton(
            source='assets/images/icon/settings.png',  # Path to the settings icon
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        settings_button.bind(on_press=self.open_settings_popup)

        layout.add_widget(settings_button)

        self.add_widget(layout)

    def open_settings_popup(self, instance):
        """Open a popup window for settings options."""

        # Create a BoxLayout for the popup content
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add custom buttons for the settings options
        language_button = CustomButton(
            text="Language",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        language_button.bind(on_press=self.open_language_popup)

        help_button = CustomButton(
            text="Help",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        help_button.bind(on_press=lambda x: print("Help clicked"))

        about_button = CustomButton(
            text="About",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        about_button.bind(on_press=lambda x: print("About clicked"))

        # Add buttons to the layout
        popup_content.add_widget(language_button)
        popup_content.add_widget(help_button)
        popup_content.add_widget(about_button)

        # Create and configure the popup
        popup = Popup(
            title="Settings",
            content=popup_content,
            size_hint=(None, None),
            size=(dp(300), dp(250)),
            auto_dismiss=True
        )

        # Open the popup
        popup.open()

    def open_language_popup(self, instance):
        """Open a popup for language selection."""

        # Create a BoxLayout for the language options
        language_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Add buttons for each language
        arabic_button = CustomButton(
            text="Arabic",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        arabic_button.bind(on_press=lambda x: self.set_language("Arabic"))

        french_button = CustomButton(
            text="French",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        french_button.bind(on_press=lambda x: self.set_language("French"))

        # Add language buttons to the layout
        language_content.add_widget(arabic_button)
        language_content.add_widget(french_button)

        # Create and configure the language popup
        language_popup = Popup(
            title="Select Language",
            content=language_content,
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            auto_dismiss=True
        )

        # Open the popup
        language_popup.open()

    def set_language(self, language):
        """Set the selected language."""
        print(f"Language selected: {language}")
        # Implement logic to update the app's language preference here.

class SecondScreen(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.add_widget(Image(
          source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
          allow_stretch=True,
          keep_ratio=False
      ))
      layout = FloatLayout()
      scroll_view = ScrollView(size_hint=(None, None), size=(dp(320), dp(520)), bar_width=dp(10))
      scroll_view.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
      grid = GridLayout(
          cols=2,
          spacing=dp(10),
          padding=[dp(10), dp(20), dp(10), dp(20)],
          size_hint=(None, None),
          width=dp(300),
          size_hint_y=None
      )
      grid.bind(minimum_height=grid.setter('height'))
      categories = [
          "Animals", "Colors", "Fruits", "Vegetables", "Numbers", "Shapes",
          "Actions", "Family and People", "Body Parts", "Clothing", "Food and Drinks",
          "Weather and Nature", "Transportation", "Household Items", "School and Education",
          "Jobs and Careers", "Sports and Hobbies", "Technology", "Places", "Time and Days",
          "Festivals and Celebrations", "Occupations", "Opposites", "Adjectives and Descriptions"
      ]
      for category in categories:
          button = CustomButton(
              text=category,
              size_hint=(None, None),
              size=(dp(140), dp(50))
          )
          if category == "Animals":
              button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
          else:
              button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
          grid.add_widget(button)
      scroll_view.add_widget(grid)
      layout.add_widget(scroll_view)
      back_button = CustomButton(
          text="< Back",
          size_hint=(None, None),
          size=(dp(80), dp(40)),
          pos_hint={'x': 0.05, 'top': 0.1}
      )
      back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'first'))
      layout.add_widget(back_button)
      self.add_widget(layout)




class AnimalCategoryScreen(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.add_widget(Image(
          source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
          allow_stretch=True,
          keep_ratio=False
      ))
      layout = FloatLayout()
      categories = ["Domestic Animals", "Wild Animals", "Farm Animals", "Birds", "Sea Creatures", "Insects"]
      grid = GridLayout(
          cols=2,
          spacing=dp(10),
          padding=[dp(10), dp(20), dp(10), dp(20)],
          size_hint=(None, None),
          width=dp(300),
          size_hint_y=None
      )
      grid.bind(minimum_height=grid.setter('height'))
      grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
      for category in categories:
          button = CustomButton(
              text=category,
              size_hint=(None, None),
              size=(dp(140), dp(50))
          )
          if category == "Wild Animals":
              button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'wild_animals'))
          else:
              button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
          grid.add_widget(button)
      layout.add_widget(grid)
      back_button = CustomButton(
          text="< Back",
          size_hint=(None, None),
          size=(dp(80), dp(40)),
          pos_hint={'x': 0.05, 'top': 0.1}
      )
      back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
      layout.add_widget(back_button)
      self.add_widget(layout)




class WildAnimalsScreen(Screen):
  def __init__(self, **kwargs):
      super().__init__(**kwargs)
      BUTTON_SIZE = dp(130)
      IMAGE_WIDTH = dp(270)
      IMAGE_HEIGHT = dp(340)
      FRAME_SIZE = (dp(190), dp(210))
      GRID_PADDING = [dp(10), dp(100), dp(10), dp(10)]
      GRID_SPACING = [dp(0), dp(150)]
      try:
          background_image = resource_find('assets/images/backgrounds/wallpaperlogo.png')
      except (KeyError, IndexError) as e:
          background_image = 'default_background.png'
      self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))
      scroll_view = ScrollView(size_hint=(1, 1))
      grid_layout = GridLayout(
          cols=1,
          spacing=GRID_SPACING,
          padding=GRID_PADDING,
          size_hint_y=None
      )
      grid_layout.bind(minimum_height=grid_layout.setter('height'))
      try:
          animals = [
              {"image": manifest["images"]["animals"][1], "audio_ar": manifest["audio"]["ar"][1], "audio_fr": manifest["audio"]["fr"][1]},
              {"image": manifest["images"]["animals"][0], "audio_ar": manifest["audio"]["ar"][0], "audio_fr": manifest["audio"]["fr"][0]},
              {"image": manifest["images"]["animals"][2], "audio_ar": manifest["audio"]["ar"][2], "audio_fr": manifest["audio"]["fr"][2]},
              {"image": manifest["images"]["animals"][3], "audio_ar": manifest["audio"]["ar"][3], "audio_fr": manifest["audio"]["fr"][3]}
          ]
      except (KeyError, IndexError) as e:
          animals = []
      for animal in animals:
          frame_layout = FloatLayout(size_hint=(None, None), size=FRAME_SIZE)
          img = Image(
              source=resource_find(f'assets/images/animals/{animal["image"]}'),
              size_hint=(None, None),
              size=(IMAGE_WIDTH, IMAGE_HEIGHT),
              pos_hint={'x': 0, 'center_y': 0.65},
              allow_stretch=True,
              keep_ratio=False
          )
          frame_layout.add_widget(img)
          fr_button = Button(
              size_hint=(None, None),
              size=(BUTTON_SIZE, BUTTON_SIZE),
              pos_hint={'right': 2, 'center_y': 0.70},
              background_normal='',
              background_down='',
              background_color=(0, 0, 0, 0)
          )
          frame_layout.add_widget(fr_button)
          fr_icon = Image(
              source='assets/images/icon/speaker.png',
              size_hint=(None, None),
              size=(BUTTON_SIZE, BUTTON_SIZE),
              pos_hint={'right': 2, 'center_y': 0.70},
              allow_stretch=False,
              keep_ratio=True
          )
          frame_layout.add_widget(fr_icon)
          ar_button = Button(
              size_hint=(None, None),
              size=(BUTTON_SIZE, BUTTON_SIZE),
              pos_hint={'right': 2, 'center_y': 0.10},
              background_normal='',
              background_down='',
              background_color=(0, 0, 0, 0)
          )
          frame_layout.add_widget(ar_button)
          ar_icon = Image(
              source='assets/images/icon/speaker.png',
              size_hint=(None, None),
              size=(BUTTON_SIZE, BUTTON_SIZE),
              pos_hint={'right': 2, 'center_y': 0.10},
              allow_stretch=False,
              keep_ratio=True
          )
          frame_layout.add_widget(ar_icon)
          fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))
          ar_button.bind(on_press=lambda instance, audio=animal["audio_ar"]: self.play_audio(audio))
          grid_layout.add_widget(frame_layout)
      scroll_view.add_widget(grid_layout)
      self.add_widget(scroll_view)
      back_button = CustomButton(
          text="< Back",
          size_hint=(None, None),
          size=(dp(100), dp(50)),
          pos_hint={'x': 0.05, 'top': 0.1}
      )
      back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
      self.add_widget(back_button)




  def play_audio(self, audio_file):
   audio_path = resource_find(f'assets/audio/ar/{audio_file}') or resource_find(f'assets/audio/fr/{audio_file}')
   if not audio_path or not os.path.exists(audio_path):
       print(f"Audio file not found: {audio_file}")
       return
   sound = SoundLoader.load(audio_path)
   if sound:
       sound.play()
   else:
       print(f"Failed to load sound: {audio_file}")






class MyApp(App):
  def build(self):
      self.icon = resource_find('assets/images/icon/appkidicon.png')
      sm = ScreenManager()
      sm.add_widget(FirstScreen(name='first'))
      sm.add_widget(SecondScreen(name='second'))
      sm.add_widget(WildAnimalsScreen(name='wild_animals'))
      sm.add_widget(AnimalCategoryScreen(name='animal_categories'))
      return sm




if __name__ == '__main__':
  MyApp().run()
