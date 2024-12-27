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
from kivy.config import Config
from kivy.core.window import Window

# Disable resizing and set fixed dimensions for desktop testing
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')  # Match Android width
Config.set('graphics', 'height', '640')  # Match Android height

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
            size=(Window.width * 0.6, Window.height * 0.1),
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

        # Add all the categories to this list
        categories = [
            "Animals", "Colors", "Fruits", "Vegetables", "Numbers", "Shapes",
            "Actions", "Family and People", "Body Parts", "Clothing", "Food and Drinks",
            "Weather and Nature", "Transportation", "Household Items", "School and Education",
            "Jobs and Careers", "Sports and Hobbies", "Technology", "Places", "Time and Days",
            "Festivals and Celebrations", "Occupations", "Opposites", "Adjectives and Descriptions"
        ]

        # Grid layout for categories
        grid = GridLayout(
            cols=2,
            spacing=10,
            padding=[10, 20, 10, 20],  # Equal padding for all sides
            size_hint=(None, None),
            width=Window.width * 0.8,  # Centered width for the grid
            size_hint_y=None
        )
        grid.bind(minimum_height=grid.setter('height'))  # Ensure dynamic height adjustment

        # Create buttons for each category
        for category in categories:
            button = Button(
                text=category,
                size_hint=(None, None),
                size=(Window.width * 0.4, Window.height * 0.1),  # Adjust button size dynamically
                background_color=(0.2, 0.5, 0.8, 1)
            )
            # Bind Animals to navigate to AnimalCategoryScreen
            if category == "Animals":
                button.bind(on_press=lambda instance: setattr(self.manager, 'current', 'animal_categories'))
            else:
                button.bind(on_press=lambda instance, cat=category: print(f"{cat} screen not yet implemented."))
            grid.add_widget(button)

        # Center the GridLayout horizontally in ScrollView
        wrapper = FloatLayout(size_hint=(1, None), height=grid.height)
        wrapper.add_widget(grid)
        grid.pos_hint = {'center_x': 0.5, 'top': 1}

        # Add GridLayout to ScrollView for scrolling
        scroll_view = ScrollView(size_hint=(1, 1), bar_width=10)
        scroll_view.add_widget(wrapper)

        # Add ScrollView to the main layout
        layout.add_widget(scroll_view)

        # Add the main layout to the screen
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
            cols=2, spacing=10, padding=[0, 20, 0, 20],  # Remove horizontal padding
            size_hint=(None, None),
            size=(Window.width * 0.8, Window.height * 0.5)  # Explicitly set size
        )
        grid.bind(minimum_height=grid.setter('height'))

        # Center the grid layout in the parent layout
        grid.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Create buttons for each animal category
        for category in categories:
            button = Button(
                text=category,
                size_hint=(None, None),
                size=(Window.width * 0.4, Window.height * 0.1),
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
        grid_layout = GridLayout(cols=2, spacing=10, padding=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Animal Data (from manifest)
        animals = [
            {"image": manifest["images"]["animals"][1], "audio_ar": manifest["audio"]["ar"][1], "audio_fr": manifest["audio"]["fr"][1]},
            {"image": manifest["images"]["animals"][0], "audio_ar": manifest["audio"]["ar"][0], "audio_fr": manifest["audio"]["fr"][0]},
            {"image": manifest["images"]["animals"][2], "audio_ar": manifest["audio"]["ar"][2], "audio_fr": manifest["audio"]["fr"][2]},
            {"image": manifest["images"]["animals"][3], "audio_ar": manifest["audio"]["ar"][3], "audio_fr": manifest["audio"]["fr"][3]}
        ]

        for animal in animals:
            animal_layout = FloatLayout(size_hint=(None, None), size=(Window.width * 0.45, Window.height * 0.25))

            # Animal Image
            img = Image(source=resource_find(f'assets/images/animals/{animal["image"]}'), 
                        size_hint=(None, None), size=(Window.width * 0.4, Window.height * 0.2),
                        pos_hint={'center_x': 0.5, 'center_y': 0.65})
            animal_layout.add_widget(img)

            # French Sound Button
            fr_button = Button(text="\U0001F50A FR", size_hint=(None, None),
                            size=(Window.width * 0.1, Window.height * 0.05),
                            pos_hint={'right': 1, 'center_y': 0.60},  # Moved slightly upward
                            background_color=(0.2, 0.5, 0.8, 1))
            fr_button.bind(on_press=lambda instance, audio=animal["audio_fr"]: self.play_audio(audio))
            animal_layout.add_widget(fr_button)

            # Arabic Sound Button
            ar_button = Button(text="\U0001F50A AR", size_hint=(None, None),
                            size=(Window.width * 0.1, Window.height * 0.05),
                            pos_hint={'right': 1, 'center_y': 0.35},  # Kept in the same position
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
