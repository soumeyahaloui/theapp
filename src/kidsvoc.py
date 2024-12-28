import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import dp

# Set fixed dimensions for testing consistency
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')  # Match Android width
Config.set('graphics', 'height', '640')  # Match Android height
Config.write()

# Load manifest.json
with open('assets/manifest.json', 'r') as f:
    manifest = json.load(f)

# Screen 1: Welcome Screen
class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Background image
        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][1]}'),
                              allow_stretch=True, keep_ratio=False))

        # Layout and Start Button
        layout = FloatLayout()
        start_button = Button(
            text="Start",
            font_size="24sp",
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=(0.2, 0.5, 0.8, 1),
            background_normal="",
        )

        start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(start_button)
        self.add_widget(layout)


# Screen 2: Categories
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set background image
        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][2]}'),
                              allow_stretch=True))

        # Main layout
        layout = FloatLayout()

        # Add a ScrollView for vertical scrolling
        scroll_view = ScrollView(size_hint=(None, None), size=(dp(320), dp(520)), bar_width=dp(10))
        scroll_view.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add GridLayout for buttons
        grid = GridLayout(
            cols=2,
            spacing=dp(10),
            padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint=(None, None),
            width=dp(300),
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Add all categories to the grid
        categories = [
            "Animals", "Colors", "Fruits", "Vegetables", "Numbers", "Shapes",
            "Actions", "Family and People", "Body Parts", "Clothing", "Food and Drinks",
            "Weather and Nature", "Transportation", "Household Items", "School and Education",
            "Jobs and Careers", "Sports and Hobbies", "Technology", "Places", "Time and Days",
            "Festivals and Celebrations", "Occupations", "Opposites", "Adjectives and Descriptions"
        ]

        for category in categories:
            button = Button(
                text=category,
                size_hint=(None, None),
                size=(dp(140), dp(50)),
                background_color=(0.2, 0.5, 0.8, 1)
            )
            # Navigate to appropriate screens
            if category == "Animals":
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
            grid.add_widget(button)

        # Add GridLayout to ScrollView
        scroll_view.add_widget(grid)

        # Add ScrollView to the main layout
        layout.add_widget(scroll_view)

        # Add layout to the screen
        self.add_widget(layout)


# Screen 3: Animal Categories
class AnimalCategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][1]}'),
                              allow_stretch=True, keep_ratio=False))

        layout = FloatLayout()

        # Animal Categories
        categories = ["Domestic Animals", "Wild Animals", "Farm Animals", "Birds", "Sea Creatures", "Insects"]

        # Grid Layout for Animal Categories
        grid = GridLayout(
            cols=2, spacing=dp(10), padding=[dp(10), dp(20), dp(10), dp(20)],
            size_hint=(None, None),
            width=dp(300),
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Center the grid layout in the parent layout
        grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Create buttons for each animal category
        for category in categories:
            button = Button(
                text=category,
                size_hint=(None, None),
                size=(dp(140), dp(50)),
                background_color=(0.2, 0.5, 0.8, 1)
            )
            # Bind Wild Animals to navigate to WildAnimalsScreen
            if category == "Wild Animals":
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'wild_animals'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
            grid.add_widget(button)

        layout.add_widget(grid)
        self.add_widget(layout)


class WildAnimalsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][0]}'), 
                              allow_stretch=True, keep_ratio=False))

        # Scrollable layout
        scroll_view = ScrollView(size_hint=(1, 1))
        grid_layout = GridLayout(cols=2, spacing=dp(10), padding=dp(10), size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Animal Data (from manifest)
        animals = [
            {"image": manifest["images"]["animals"][1], "audio_ar": manifest["audio"]["ar"][1], "audio_fr": manifest["audio"]["fr"][1]},
            {"image": manifest["images"]["animals"][0], "audio_ar": manifest["audio"]["ar"][0], "audio_fr": manifest["audio"]["fr"][0]},
            {"image": manifest["images"]["animals"][2], "audio_ar": manifest["audio"]["ar"][2], "audio_fr": manifest["audio"]["fr"][2]},
            {"image": manifest["images"]["animals"][3], "audio_ar": manifest["audio"]["ar"][3], "audio_fr": manifest["audio"]["fr"][3]}
        ]

        for animal in animals:
            # Create a FloatLayout for each animal
            animal_layout = FloatLayout(size_hint=(None, None), size=(dp(160), dp(120)))

            # Create and configure the Animal Image
            img = Image(
                source=resource_find(f'assets/images/animals/{animal["image"]}'),
                size_hint=(None, None),
                size=(dp(140), dp(100)),
                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                allow_stretch=True,
                keep_ratio=False
            )
            animal_layout.add_widget(img)

            # Add French Sound Button
            fr_button = Button(text="\U0001F50A FR", size_hint=(None, None),
                               size=(dp(50), dp(30)),
                               pos_hint={'right': 1, 'center_y': 0.3},
                               background_color=(0.2, 0.5, 0.8, 1))
            fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))
            animal_layout.add_widget(fr_button)

            # Add Arabic Sound Button
            ar_button = Button(text="\U0001F50A AR", size_hint=(None, None),
                               size=(dp(50), dp(30)),
                               pos_hint={'right': 1, 'center_y': 0},
                               background_color=(0.2, 0.5, 0.8, 1))
            ar_button.bind(on_press=lambda instance, audio=animal["audio_ar"]: self.play_audio(audio))
            animal_layout.add_widget(ar_button)

            # Add the animal layout to the grid layout
            grid_layout.add_widget(animal_layout)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def play_audio(self, audio_file):
        audio_path = resource_find(f'assets/audio/ar/{audio_file}') or resource_find(f'assets/audio/fr/{audio_file}')
        if audio_path and os.path.exists(audio_path):
            sound = SoundLoader.load(audio_path)
            if sound:
                sound.play()
            else:
                print(f"Failed to load sound: {audio_file}")
        else:
            print(f"Audio file not found: {audio_file}")


# Main App Class
class MyApp(App):
    def build(self):
        self.icon = resource_find(f'assets/images/icons/{manifest["images"]["icons"][0]}')
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(WildAnimalsScreen(name='wild_animals'))
        sm.add_widget(AnimalCategoryScreen(name='animal_categories'))
        return sm

# Run the App
if __name__ == '__main__':
    MyApp().run()
