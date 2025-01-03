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

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Loading...", font_size="24sp"))

    def on_enter(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'first'), 2)


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


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_button = None
        self.settings_button = None
        self.settings_popup = None
        self.language_popup = None
        self.language = 'Français'  # Default language
        self.init_ui()

    def init_ui(self):
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/purple.png'),
            allow_stretch=True, keep_ratio=False
        ))
        layout = FloatLayout()

        # Create the start button with default French text
        self.start_button = CustomButton(
            text=LANGUAGES['Français']['start'],
            size_hint=(None, None),
            size=(dp(240), dp(80)),
            pos_hint={'center_x': 0.5, 'center_y': 0.15}
        )
        self.start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(self.start_button)

        # Settings button
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
        self.language = language
        if language == 'Arabe':
            # Replace the button's text with the image for Arabic
            self.start_button.clear_widgets()
            start_button_image = Image(
                source=resource_find('assets/images/text/output.png'),
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(None, None),
                size=self.start_button.size,
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
            )
            self.start_button.add_widget(start_button_image)
        else:
            # Revert to the text label for French
            self.start_button.clear_widgets()
            self.start_button.label.text = LANGUAGES['Français']['start']
            self.start_button.label.font_name = 'FrenchFont'
            self.start_button.add_widget(self.start_button.label)

    def open_settings_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        language_button = CustomButton(
            text=LANGUAGES['Français']['language'],
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        language_button.bind(on_press=self.open_language_popup)
        help_button = CustomButton(
            text=LANGUAGES['Français']['help'],
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        help_button.bind(on_press=lambda x: print("Help clicked"))
        about_button = CustomButton(
            text=LANGUAGES['Français']['about'],
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        about_button.bind(on_press=lambda x: print("About clicked"))
        popup_content.add_widget(language_button)
        popup_content.add_widget(help_button)
        popup_content.add_widget(about_button)
        self.settings_popup = Popup(
            title=LANGUAGES['Français']['settings'],
            content=popup_content,
            size_hint=(None, None),
            size=(dp(300), dp(250)),
            auto_dismiss=True
        )
        self.settings_popup.open()

    def open_language_popup(self, instance):
        if self.settings_popup:
            self.settings_popup.dismiss()
        language_content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        arabic_button = CustomButton(
            text="Arabe",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        arabic_button.bind(on_press=lambda x: self.set_language("Arabe"))
        french_button = CustomButton(
            text="Français",
            size_hint=(1, None),
            size=(dp(200), dp(50))
        )
        french_button.bind(on_press=lambda x: self.set_language("Français"))
        language_content.add_widget(arabic_button)
        language_content.add_widget(french_button)
        self.language_popup = Popup(
            title=LANGUAGES['Français']['language'],
            content=language_content,
            size_hint=(None, None),
            size=(dp(300), dp(200)),
            auto_dismiss=True
        )
        self.language_popup.open()

    def set_language(self, language):
        if self.language_popup:
            self.language_popup.dismiss()
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
        self.language = 'Français'  # Default language
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
        
        self.add_category_buttons()
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)

        # Back Button
        self.back_button = CustomButton(
            text=LANGUAGES[self.language]['back'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'x': 0.05, 'top': 0.1}
        )
        self.back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'first'))
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def add_category_buttons(self):
        categories = LANGUAGES[self.language]['categories']
        for category in categories:
            button = CustomButton(
                text=category if self.language != 'Arabe' else '',
                size_hint=(None, None),
                size=(dp(140), dp(50))
            )

            if self.language == 'Arabe':
                # Use the mapped English filename for Arabic
                image_filename = ARABIC_TO_ENGLISH_IMAGES.get(category, None)
                if image_filename:
                    button.clear_widgets()
                    category_image = Image(
                        source=resource_find(f'assets/images/text/categories/{image_filename}'),
                        allow_stretch=True,
                        keep_ratio=True,
                        size_hint=(None, None),
                        size=button.size,
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}
                    )
                    button.add_widget(category_image)

            # Bind "Animaux" or "الحيوانات" to open AnimalCategoryScreen
            if category in ["Animaux", "الحيوانات"]:
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} selected"))

            self.grid.add_widget(button)


    def update_language(self, language):
        self.language = language
        self.grid.clear_widgets()  # Clear existing buttons
        self.add_category_buttons()

        # Update Back Button
        if language == 'Arabe':
            self.back_button.clear_widgets()
            back_button_image = Image(
                source=resource_find('assets/images/text/back.png'),
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(None, None),
                size=self.back_button.size,
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.back_button.add_widget(back_button_image)
        else:
            self.back_button.clear_widgets()
            self.back_button.label.text = LANGUAGES['Français']['back']
            self.back_button.label.font_name = 'FrenchFont'
            self.back_button.add_widget(self.back_button.label)


class AnimalCategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'Français'
        self.back_button = None
        self.grid = None
        self.scroll_view = None
        self.init_ui()

    def init_ui(self):
        self.add_widget(Image(
            source=resource_find('assets/images/backgrounds/wallpaperlogo.png'),
            allow_stretch=True,
            keep_ratio=False
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

        self.add_category_buttons()
        self.scroll_view.add_widget(self.grid)
        layout.add_widget(self.scroll_view)

        # Back Button
        self.back_button = CustomButton(
            text=LANGUAGES[self.language]['back'],
            size_hint=(None, None),
            size=(dp(80), dp(40)),
            pos_hint={'x': 0.05, 'top': 0.1}
        )
        self.back_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(self.back_button)
        self.add_widget(layout)

    def add_category_buttons(self):
        categories = LANGUAGES[self.language]['animalcategories']
        for category in categories:
            button = CustomButton(
                text=category if self.language != 'Arabe' else '',
                size_hint=(None, None),
                size=(dp(140), dp(50))
            )

            if self.language == 'Arabe':
                # Use the mapped English filename for Arabic animal categories
                image_filename = ANIMAL_ARABIC_TO_ENGLISH_IMAGES.get(category, None)
                if image_filename:
                    button.clear_widgets()
                    category_image = Image(
                        source=resource_find(f'assets/images/text/animalcategories/{image_filename}'),
                        allow_stretch=True,
                        keep_ratio=True,
                        size_hint=(None, None),
                        size=button.size,
                        pos_hint={'center_x': 0.5, 'center_y': 0.5}
                    )
                    button.add_widget(category_image)

            # Bind "Animaux Sauvages" or "حيوانات برية" to open WildAnimalsScreen
            if category in ["Animaux Sauvages", "حيوانات برية"]:
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'wild_animals'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} category selected"))

            self.grid.add_widget(button)


    def update_language(self, language):
        self.language = language
        self.grid.clear_widgets()  # Clear existing buttons
        self.add_category_buttons()

        # Update Back Button
        if language == 'Arabe':
            self.back_button.clear_widgets()
            back_button_image = Image(
                source=resource_find('assets/images/text/back.png'),
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(None, None),
                size=self.back_button.size,
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            self.back_button.add_widget(back_button_image)
        else:
            self.back_button.clear_widgets()
            self.back_button.label.text = LANGUAGES['Français']['back']
            self.back_button.label.font_name = 'FrenchFont'
            self.back_button.add_widget(self.back_button.label)

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

        # Add all screens to the ScreenManager
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(AnimalCategoryScreen(name='animal_categories'))
        sm.add_widget(WildAnimalsScreen(name='wild_animals'))

        # Set the initial screen to the loading screen
        sm.current = 'loading'

        # Trigger a forced layout refresh
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.refresh_layout(sm))

        return sm

    def refresh_layout(self, sm):
        # Refresh the layout for all widgets in the ScreenManager
        sm.do_layout()
        for screen in sm.screens:
            screen.do_layout()



if __name__ == '__main__':
    MyApp().run()