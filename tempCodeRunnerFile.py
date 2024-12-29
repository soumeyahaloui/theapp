import sys
import os
from kivy.metrics import dp
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from kivy.config import Config
from kivy.core.window import Window  # Import Window here


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')  # Width for mobile devices
Config.set('graphics', 'height', '720')  # Height for mobile devices
Config.write()

Window.size = (400, 720)

from kidsvoc import MyApp  # Importing the MyApp class from the src folder

def main():
    app = MyApp()
    app.run()

if __name__ == '__main__':
    main()
