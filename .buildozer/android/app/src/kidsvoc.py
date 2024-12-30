
import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.image import Image, CoreImage
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import ButtonBehavior
from PIL import Image as PILImage, ImageDraw, ImageFont
from io import BytesIO


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()


import logging
logging.getLogger("PIL").setLevel(logging.ERROR)


with open('assets/manifest.json', 'r') as f:
   manifest = json.load(f)


def render_arabic_text_as_image(text, font_path, font_size=40):
   image_width, image_height = 400, 100
   pil_image = PILImage.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
   draw = ImageDraw.Draw(pil_image)
   font = ImageFont.truetype(font_path, font_size)
   text_bbox = font.getbbox(text)
   text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
   x = (image_width - text_width) // 2
   y = (image_height - text_height) // 2
   draw.text((x, y), text, font=font, fill="white")
   buffer = BytesIO()
   pil_image.save(buffer, format="PNG")
   buffer.seek(0)
   return CoreImage(buffer, ext="png")


class CustomButton(ButtonBehavior, FloatLayout):
   def __init__(self, text, **kwargs):
       super().__init__(**kwargs)
       font_path = "assets/fonts/NotoNaskhArabic-VariableFont_wght.ttf"
       text_image = render_arabic_text_as_image(text, font_path)
       with self.canvas.before:
           Color(0.2, 0.5, 0.8, 1)
           self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(20)])
       self.bind(size=self.update_bg, pos=self.update_bg)
       self.text_image = Image(
           texture=text_image.texture,
           size_hint=(None, None),
           size=(dp(240), dp(80)),
           pos_hint={'center_x': 0.5, 'center_y': 0.5}
       )
       self.add_widget(self.text_image)


   def update_bg(self, *args):
       self.bg_rect.size = self.size
       self.bg_rect.pos = self.pos


class FirstScreen(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.add_widget(Image(
           source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][1]}'),
           allow_stretch=True, keep_ratio=False
       ))
       layout = FloatLayout()
       start_button = CustomButton(
           text="ابدأ",
           size_hint=(None, None),
           size=(dp(240), dp(80)),
           pos_hint={'center_x': 0.5, 'center_y': 0.15}
       )
       start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
       layout.add_widget(start_button)
       self.add_widget(layout)


class SecondScreen(Screen):
   def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.add_widget(Image(
           source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][0]}'),
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
           source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][0]}'),
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
           background_image = resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][0]}')
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
       if audio_path and os.path.exists(audio_path):
           sound = SoundLoader.load(audio_path)
           if sound:
               sound.play()


class MyApp(App):
   def build(self):
       self.icon = resource_find(f'assets/images/icon/{manifest["images"]["icon"][0]}')
       sm = ScreenManager()
       sm.add_widget(FirstScreen(name='first'))
       sm.add_widget(SecondScreen(name='second'))
       sm.add_widget(WildAnimalsScreen(name='wild_animals'))
       sm.add_widget(AnimalCategoryScreen(name='animal_categories'))
       return sm


if __name__ == '__main__':
   MyApp().run()
