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

Window.size = (400, 720)  # Set window size explicitly


from kidsvoc import MyApp

def main():
   app = MyApp()
   app.run()

if __name__ == '__main__':
   main()