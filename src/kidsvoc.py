import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.resources import resource_find
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
import arabic_reshaper
from bidi.algorithm import get_display


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()

LabelBase.register(name='ArabicFont', fn_regular='assets/fonts/NotoNaskhArabic-Regular.ttf')
LabelBase.register(name='FrenchFont', fn_regular='assets/fonts/Roboto-Regular.ttf')  # Example for French

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

        # Use the original text directly for testing
        self.label = Label(
            text=text,
            font_size="20sp",
            font_name='ArabicFont' if self.is_arabic(text) else 'FrenchFont',
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=self.size,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='right' if self.is_arabic(text) else 'center',
            valign='middle',
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def is_arabic(self, text):
        """Check if the text contains Arabic characters."""
        return any('\u0600' <= char <= '\u06FF' for char in text)

LANGUAGES = {
    'Français': {
        'start': "Démarrer",
        'settings': "Paramètres",
        'language': "Langue",
        'help': "Aide",
        'about': "À propos",
        'back': "< Retour",
        'categories': [
            "Animaux", "Couleurs", "Fruits", "Légumes", "Nombres", "Formes",
            "Actions", "Famille et Personnes", "Parties du Corps", "Vêtements", "Nourriture et Boissons",
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


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_button = None
        self.settings_button = None
        self.settings_popup = None
        self.language_popup = None
        self.init_ui()

    def init_ui(self):
        # Add background image
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/purple.png'),
            allow_stretch=True, keep_ratio=False
        ))
        
        layout = FloatLayout()

        # Create Start Button
        self.start_button = CustomButton(
            text=self.process_arabic_text(LANGUAGES['Français']['start']),
            size_hint=(None, None),
            size=(dp(240), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        self.start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(self.start_button)

        # Create Settings Button
        self.settings_button = IconButton(
            source='assets/images/icon/settings.png',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'right': 0.95, 'top': 0.95}
        )
        self.settings_button.bind(on_press=self.open_settings_popup)
        layout.add_widget(self.settings_button)

        self.add_widget(layout)

    def update_language(self, language):
        reshaped_text = self.process_arabic_text(LANGUAGES[language]['start'])
        if reshaped_text:
            self.start_button.label.text = reshaped_text
        else:
            self.start_button.label.text = LANGUAGES[language]['start']  # Fallback to the original


    def process_arabic_text(self, text):
        """Reshape and process Arabic text for proper display."""
        if self.is_arabic(text):
            try:
                reshaped_text = arabic_reshaper.reshape(text)
                display_text = get_display(reshaped_text)
                print(f"Processed text: {display_text}")  # Debugging output
                return display_text
            except Exception as e:
                print(f"Error processing Arabic text: {e}")
        return text



    def is_arabic(self, text):
        """Check if the text contains Arabic characters."""
        return any('\u0600' <= char <= '\u06FF' for char in text)

    def open_settings_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        language_button = CustomButton(
            text=self.process_arabic_text(LANGUAGES['Français']['language']),
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        language_button.bind(on_press=self.open_language_popup)
        help_button = CustomButton(
            text=self.process_arabic_text(LANGUAGES['Français']['help']),
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        help_button.bind(on_press=lambda x: print("Help clicked"))
        about_button = CustomButton(
            text=self.process_arabic_text(LANGUAGES['Français']['about']),
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        about_button.bind(on_press=lambda x: print("About clicked"))
        popup_content.add_widget(language_button)
        popup_content.add_widget(help_button)
        popup_content.add_widget(about_button)
        self.settings_popup = Popup(
            title=self.process_arabic_text(LANGUAGES['Français']['settings']),
            content=popup_content,
            size_hint=(None, None),
            size=(dp(300), dp(250)),
            auto_dismiss=True
        )
        self.settings_popup.open()

    def open_language_popup(self, instance):
        if self.settings_popup:
            self.settings_popup.dismiss()  # Close the settings popup

        language_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        arabic_button = CustomButton(
            text=self.process_arabic_text("Arabe"),
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        arabic_button.bind(on_press=lambda x: self.set_language("Arabe"))
        french_button = CustomButton(
            text=self.process_arabic_text("Français"),
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        french_button.bind(on_press=lambda x: self.set_language("Français"))
        language_content.add_widget(arabic_button)
        language_content.add_widget(french_button)
        self.language_popup = Popup(
            title=self.process_arabic_text(LANGUAGES['Français']['language']),
            content=language_content,
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            auto_dismiss=True
        )
        self.language_popup.open()

    def set_language(self, language):
        if self.language_popup:
            self.language_popup.dismiss()  # Close the language popup

        self.manager.language = language
        for screen in self.manager.screens:
            if hasattr(screen, 'update_language'):
                screen.update_language(language)

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.back_button = None
        self.grid = None
        self.scroll_view = None
        self.init_ui()

    def init_ui(self):
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
            allow_stretch=True, keep_ratio=False
        ))
        layout = FloatLayout()
        self.scroll_view = ScrollView(
            size_hint=(None, None),
            size=(dp(320), dp(520)),
            bar_width=dp(10),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint=(None, None),
            width=dp(300),
            size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter('height'))
        categories = LANGUAGES['Français']['categories']
        for category in categories:
            button = CustomButton(
                text=category,
                size_hint=(None, None),
                size=(dp(140), dp(50))
            )
            if category == "Animaux":
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} not implemented yet."))
            self.grid.add_widget(button)
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)
        self.back_button = CustomButton(
            text=LANGUAGES['Français']['back'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'x': 0.05, 'top': 0.1}
        )
        self.back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'first'))
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def update_language(self, language):
        categories = LANGUAGES[language]['categories']
        for i, button in enumerate(self.grid.children[::-1]):
            if i < len(categories):
                button.label.text = categories[i]
        self.back_button.label.text = LANGUAGES[language]['back']

class AnimalCategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'Français'
        self.init_ui()

    def init_ui(self):
        # Set background image
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
            allow_stretch=True,
            keep_ratio=False
        ))

        # Create a FloatLayout for the overall screen
        layout = FloatLayout()

        # ScrollView and GridLayout for displaying categories
        scroll_view = ScrollView(
            size_hint=(None, None),
            size=(dp(320), dp(520)),
            bar_width=dp(10),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint=(None, None),
            width=dp(300),
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Define categories with unique identifiers
        categories = [
            {"id": "domestic_animals", "name": LANGUAGES[self.language]['animalcategories'][0]},
            {"id": "wild_animals", "name": LANGUAGES[self.language]['animalcategories'][1]},
            {"id": "farm_animals", "name": LANGUAGES[self.language]['animalcategories'][2]},
            {"id": "birds", "name": LANGUAGES[self.language]['animalcategories'][3]},
            {"id": "marine_creatures", "name": LANGUAGES[self.language]['animalcategories'][4]},
            {"id": "insects", "name": LANGUAGES[self.language]['animalcategories'][5]}
        ]

        # Create buttons for each category
        for category in categories:
            button = CustomButton(
                text=category["name"],
                size_hint=(None, None),
                size=(dp(140), dp(50))
            )
            if category["id"] == "wild_animals":  # Navigate to WildAnimalsScreen
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'wild_animals'))
            else:  # Placeholder for unimplemented categories
                button.bind(on_press=lambda instance, cat=category["name"]: print(f"{cat} category not implemented yet."))

            grid.add_widget(button)

        scroll_view.add_widget(grid)
        layout.add_widget(scroll_view)

        # Add a back button
        back_button = CustomButton(
            text=LANGUAGES[self.language]['back'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'x': 0.05, 'top': 0.1}
        )
        back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(back_button)

        # Add everything to the screen
        self.add_widget(layout)

    def update_language(self, language):
        # Update the screen's language and refresh buttons
        self.language = language
        self.clear_widgets()
        self.init_ui()


class WildAnimalsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'Français'
        self.back_button = None
        self.init_ui()

    def init_ui(self):
        BUTTON_SIZE = dp(130)
        IMAGE_WIDTH = dp(270)
        IMAGE_HEIGHT = dp(340)
        FRAME_SIZE = (dp(190), dp(210))
        GRID_PADDING = [dp(10), dp(100), dp(10), dp(10)]
        GRID_SPACING = [dp(0), dp(150)]

        # Set background image
        try:
            background_image = resource_find('assets/images/backgrounds/wallpaperlogo.png')
        except (KeyError, IndexError):
            background_image = 'default_background.png'
        self.add_widget(Image(source=background_image, allow_stretch=True, keep_ratio=False))

        # ScrollView and GridLayout for animals
        scroll_view = ScrollView(size_hint=(1, 1))
        grid_layout = GridLayout(
            cols=1,
            spacing=GRID_SPACING,
            padding=GRID_PADDING,
            size_hint_y=None
        )
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Load animal data from manifest
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

        # Create widgets for each animal
        for animal in animals:
            frame_layout = FloatLayout(size_hint=(None, None), size=FRAME_SIZE)

            # Animal image
            img = Image(
                source=resource_find(f'assets/images/animals/{animal["image"]}'),
                size_hint=(None, None),
                size=(IMAGE_WIDTH, IMAGE_HEIGHT),
                pos_hint={'x': 0, 'center_y': 0.65},
                allow_stretch=True,
                keep_ratio=False
            )
            frame_layout.add_widget(img)

            # French audio button
            fr_button = Button(
                size_hint=(None, None),
                size=(BUTTON_SIZE, BUTTON_SIZE),
                pos_hint={'right': 2, 'center_y': 0.70},
                background_normal='',
                background_down='',
                background_color=(0, 0, 0, 0)
            )
            frame_layout.add_widget(fr_button)

            # French audio icon
            fr_icon = Image(
                source='assets/images/icon/speaker.png',
                size_hint=(None, None),
                size=(BUTTON_SIZE, BUTTON_SIZE),
                pos_hint={'right': 2, 'center_y': 0.70},
                allow_stretch=False,
                keep_ratio=True
            )
            frame_layout.add_widget(fr_icon)

            # Arabic audio button
            ar_button = Button(
                size_hint=(None, None),
                size=(BUTTON_SIZE, BUTTON_SIZE),
                pos_hint={'right': 2, 'center_y': 0.10},
                background_normal='',
                background_down='',
                background_color=(0, 0, 0, 0)
            )
            frame_layout.add_widget(ar_button)

            # Arabic audio icon
            ar_icon = Image(
                source='assets/images/icon/speaker.png',
                size_hint=(None, None),
                size=(BUTTON_SIZE, BUTTON_SIZE),
                pos_hint={'right': 2, 'center_y': 0.10},
                allow_stretch=False,
                keep_ratio=True
            )
            frame_layout.add_widget(ar_icon)

            # Bind audio buttons
            fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))
            ar_button.bind(on_press=lambda instance, audio=animal["audio_ar"]: self.play_audio(audio))

            # Add frame to grid layout
            grid_layout.add_widget(frame_layout)

        # Add grid layout to scroll view
        scroll_view.add_widget(grid_layout)
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
        # Play the corresponding audio file
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

    def update_language(self, language):
        self.language = language
        if self.back_button:
            self.back_button.label.text = LANGUAGES[language]['back']

class MyApp(App):
    def build(self):
        self.icon = resource_find('assets/images/icon/appkidicon.png')
        sm = ScreenManager()
        sm.language = 'Français'
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(AnimalCategoryScreen(name='animal_categories'))
        sm.add_widget(WildAnimalsScreen(name='wild_animals'))
        return sm

if __name__ == '__main__':
    MyApp().run()

