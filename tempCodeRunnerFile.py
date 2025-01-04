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
from kivy.uix.screenmanager import ScreenManager, Screen



LabelBase.register(name='ArabicFont', fn_regular='assets/fonts/NotoNaskhArabic-Regular.ttf')
LabelBase.register(name='FrenchFont', fn_regular='assets/fonts/Roboto-Regular.ttf')

with open('assets/manifest.json', 'r') as f:
    manifest = json.load(f)

class IconButton(ButtonBehavior, Image):
    pass

class CustomButton(ButtonBehavior, FloatLayout):
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
            text_size=(self.width - dp(20), None),  # Allow wrapping within button
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
        # Dynamically adjust the height based on the label's texture size
        self.size = (self.size[0], max(dp(50), self.label.texture_size[1] + dp(20)))


LANGUAGES = {
    'Français': {
        'start': "Démarrer",
        'settings': "Paramètres",
        'language': "Langue",
        'help': "Aide",
        'about': "À propos",
        'back': "< Retour",
        'categories': [
            "Couleurs", "Formes", "Nombres", "Fruits", "Légumes", "Actions",
            "Parties du Corps", "Animaux", "Famille et Personnes", "Vêtements", "Nourriture et Boissons",
            "Temps et Nature", "Transport", "Objets Ménagers", "École et Éducation",
            "Métiers", "Sports et Loisirs", "Technologie", "Lieux", "Temps et Jours",
            "Festivals et Célébrations", "Professions", "Contraires", "Adjectifs et Descriptions"
        ],
        'animalcategories': [
            "Animaux Domestiques", "Animaux Sauvages", "Animaux de Ferme", "Oiseaux", "Créatures Marines", "Insectes"
        ]
    },
    'Arabe': {
        'start': "ابدأ",
        'settings': "إعدادات",
        'language': "اللغة",
        'help': "مساعدة",
        'about': "حول",
        'back': "< رجوع",
        'categories': [
            "الحيوانات", "الألوان", "الفواكه", "الخضروات", "الأرقام", "الأشكال",
            "الأفعال", "العائلة والأشخاص", "أجزاء الجسم", "الملابس", "الطعام والمشروبات",
            "الطقس والطبيعة", "المواصلات", "الأشياء المنزلية", "المدرسة والتعليم",
            "المهن", "الرياضة والترفيه", "التكنولوجيا", "الأماكن", "الوقت والأيام",
            "المهرجانات والاحتفالات", "المهن", "المتضادات", "الصفات والوصف"
        ],
        'animalcategories': [
            "حيوانات أليفة", "حيوانات برية", "حيوانات المزرعة", "طيور", "كائنات بحرية", "حشرات"
        ]
    }
}

ARABIC_TO_ENGLISH_IMAGES = {
    "الحيوانات": "animals.png",
    "الألوان": "colors.png",
    "الفواكه": "fruits.png",
    "الخضروات": "vegetables.png",
    "الأرقام": "numbers.png",
    "الأشكال": "shapes.png",
    "الأفعال": "actions.png",
    "العائلة والأشخاص": "family_and_people.png",
    "أجزاء الجسم": "body_parts.png",
    "الملابس": "clothing.png",
    "الطعام والمشروبات": "food_and_drinks.png",
    "الطقس والطبيعة": "weather_and_nature.png",
    "المواصلات": "transportation.png",
    "الأشياء المنزلية": "household_items.png",
    "المدرسة والتعليم": "school_and_education.png",
    "المهن": "professions.png",
    "الرياضة والترفيه": "sports_and_entertainment.png",
    "التكنولوجيا": "technology.png",
    "الأماكن": "places.png",
    "الوقت والأيام": "time_and_days.png",
    "المهرجانات والاحتفالات": "festivals_and_celebrations.png",
    "المتضادات": "opposites.png",
    "الصفات والوصف": "adjectives_and_descriptions.png",
}

ANIMAL_ARABIC_TO_ENGLISH_IMAGES = {
    "حيوانات أليفة": "domestic_animals.png",
    "حيوانات برية": "wild_animals.png",
    "حيوانات المزرعة": "farm_animals.png",
    "طيور": "birds.png",
    "كائنات بحرية": "marine_creatures.png",
    "حشرات": "insects.png",
}

class WildAnimalsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'Français'
        self.back_button = None
        self.init_ui()

    def init_ui(self):
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
            allow_stretch=True,
            keep_ratio=False
        ))

        # Create a horizontal ScrollView
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=False)
        horizontal_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(70),
            padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint_x=None,
            height=dp(520)
        )
        horizontal_layout.bind(minimum_width=horizontal_layout.setter('width'))

        try:
            animals = [
                {
                    "image": manifest["images"]["animals"][i],
                    "audio_ar": manifest["audio"]["ar"][i],
                    "audio_fr": manifest["audio"]["fr"][i]
                }
                for i in range(len(manifest["images"]["animals"]))
            ]
        except (KeyError, IndexError):
            animals = []

        for animal in animals:
            frame_layout = FloatLayout(size_hint=(None, None), size=(dp(320), dp(520)))

            img = Image(
                source=resource_find(f'assets/images/animals/{animal["image"]}'),
                size_hint=(None, None),
                size=(dp(300), dp(400)),
                pos_hint={'x': 0, 'top': 1},
                allow_stretch=True,
                keep_ratio=False
            )
            frame_layout.add_widget(img)

            ar_button = Button(
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={'right': 1.2, 'center_y': 0.35},
                background_normal='',
                background_down='',
                background_color=(0, 0, 0, 0)
            )
            frame_layout.add_widget(ar_button)

            ar_icon = Image(
                source='assets/images/icon/speaker.png',
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={'right': 1.2, 'center_y': 0.35},
                allow_stretch=False,
                keep_ratio=True
            )
            frame_layout.add_widget(ar_icon)

            fr_button = Button(
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={'right': 1.2, 'center_y': 0.62},
                background_normal='',
                background_down='',
                background_color=(0, 0, 0, 0)
            )
            frame_layout.add_widget(fr_button)

            fr_icon = Image(
                source='assets/images/icon/speaker.png',
                size_hint=(None, None),
                size=(dp(100), dp(100)),
                pos_hint={'right': 1.2, 'center_y': 0.62},
                allow_stretch=False,
                keep_ratio=True
            )
            frame_layout.add_widget(fr_icon)

            ar_button.bind(on_press=lambda instance, audio=animal["audio_ar"]: self.play_audio(audio))
            fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))

            horizontal_layout.add_widget(frame_layout)

        scroll_view.add_widget(horizontal_layout)
        self.add_widget(scroll_view)

        # Back button
        self.back_button = CustomButton(
            text=LANGUAGES[self.language]['back'],
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            pos_hint={'x': 0.05, 'top': 0.1}
        )
        self.back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
        self.add_widget(self.back_button)

    def play_audio(self, audio_file):
        audio_path = (
            resource_find(f'assets/audio/ar/{audio_file}') or
            resource_find(f'assets/audio/fr/{audio_file}')
        )
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
        Window.size = (400, 720)
        sm = ScreenManager()
        sm.language = 'Français'
        sm.add_widget(WildAnimalsScreen(name='wild_animals'))
        return sm

if __name__ == '__main__':
    MyApp().run()