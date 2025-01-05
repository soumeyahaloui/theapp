import sys
import os
from kivy.metrics import dp
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from kivy.config import Config
from kivy.core.window import Window

Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', str(Window.width))
Config.set('graphics', 'height', str(Window.height))
Config.write()

Window.fullscreen = True  # Use the full screen of the device
Window.size = (Window.width, Window.height) 

from kidsvoc import MyApp

def main():
   app = MyApp()
   app.run()

if __name__ == '__main__':
   main()