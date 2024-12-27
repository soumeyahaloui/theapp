import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find

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
            size=(250, 100),  # Larger size
            pos_hint={'center_x': 0.5, 'center_y': 0.25},  # Slightly higher position
            background_color=(0.2, 0.5, 0.8, 1),
            background_normal="",  # Use a custom background if needed
        )

        start_button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'second'))
        layout.add_widget(start_button)
        self.add_widget(layout)


# Screen 2: Categories
# Screen 2: Categories
# Screen 2: Categories
class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][2]}'),
                              allow_stretch=True, keep_ratio=False))

        layout = FloatLayout()

        # Add all the categories to this list
        categories = [
            "Animals", "Colors", "Fruits", "Vegetables", "Numbers", "Shapes", 
            "Actions", "Family and People", "Body Parts", "Clothing", "Food and Drinks",
            "Weather and Nature", "Transportation", "Household Items", "School and Education",
            "Jobs and Careers", "Sports and Hobbies", "Technology", "Places", "Time and Days",
            "Festivals and Celebrations", "Occupations", "Opposites", "Adjectives and Descriptions"
        ]

        # Dynamic grid layout for categories
        grid = GridLayout(cols=2, spacing=10, padding=20, size_hint=(None, None), size=(400, 600),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.bind(minimum_height=grid.setter('height'))  # Adjust for dynamic content

        # Create buttons for each category
        for category in categories:
            button = Button(
                text=category, size_hint=(None, None), size=(150, 80), 
                background_color=(0.2, 0.5, 0.8, 1)
            )
            # Bind Animals to navigate to AnimalCategoryScreen
            if category == "Animals":
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
            grid.add_widget(button)

        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(grid)
        layout.add_widget(scroll_view)
        self.add_widget(layout)


# Screen 4: Animal Categories
# Screen 4: Animal Categories
class AnimalCategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][1]}'),
                              allow_stretch=True, keep_ratio=False))

        layout = FloatLayout()

        # Animal Categories
        categories = ["Domestic Animals", "Wild Animals", "Farm Animals", "Birds", "Sea Creatures", "Insects"]

        # Grid Layout for Animal Categories
        grid = GridLayout(cols=2, spacing=10, padding=20, size_hint=(None, None), size=(400, 300),
                          pos_hint={'center_x': 0.5, 'center_y': 0.5})
        grid.bind(minimum_height=grid.setter('height'))

        # Create buttons for each animal category
        for category in categories:
            button = Button(
                text=category, size_hint=(None, None), size=(150, 80),
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


# Screen 3: Animals
class WildAnimalsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Image(source=resource_find(f'assets/images/backgrounds/{manifest["images"]["backgrounds"][0]}'), 
                              allow_stretch=True, keep_ratio=False))

        # Scrollable layout
        scroll_view = ScrollView(size_hint=(1, 1))
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        scroll_view.add_widget(main_layout)
        self.add_widget(scroll_view)

        # Animal Data (from manifest)
        animals = [
            {"name_ar": "أسد", "name_fr": "Lion", "image": manifest["images"]["animals"][1],
             "audio_ar": manifest["audio"]["ar"][1], "audio_fr": manifest["audio"]["fr"][1]},
            {"name_ar": "فيل", "name_fr": "Éléphant", "image": manifest["images"]["animals"][0],
             "audio_ar": manifest["audio"]["ar"][0], "audio_fr": manifest["audio"]["fr"][0]},
            {"name_ar": "قرد", "name_fr": "Singe", "image": manifest["images"]["animals"][2],
             "audio_ar": manifest["audio"]["ar"][2], "audio_fr": manifest["audio"]["fr"][2]},
            {"name_ar": "نمر", "name_fr": "Tigre", "image": manifest["images"]["animals"][3],
             "audio_ar": manifest["audio"]["ar"][3], "audio_fr": manifest["audio"]["fr"][3]}
        ]

        # Generate Animal Cards
        for animal in animals:
            row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=100)

            # Animal Image
            img = Image(source=resource_find(f'assets/images/animals/{animal["image"]}'), 
                        size_hint=(None, None), size=(80, 80))
            row.add_widget(img)

            # Play Buttons
            button_layout = BoxLayout(orientation='vertical', spacing=5, size_hint_x=None, width=100)
            ar_button = Button(text="🔊 AR", size_hint_y=None, height=40)
            ar_button.bind(on_press=lambda instance, audio=animal["audio_ar"]: self.play_audio(audio))
            fr_button = Button(text="🔊 FR", size_hint_y=None, height=40)
            fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))
            button_layout.add_widget(ar_button)
            button_layout.add_widget(fr_button)

            row.add_widget(button_layout)
            main_layout.add_widget(row)

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
# Main App Class
class MyApp(App):
    def build(self):
        self.icon = resource_find(f'assets/images/icons/{manifest["images"]["icons"][0]}')
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(WildAnimalsScreen(name='wild_animals'))  # Renamed screen
        sm.add_widget(AnimalCategoryScreen(name='animal_categories'))  # Add the new screen here
        return sm



# Run the App
if __name__ == '__main__':
    MyApp().run()