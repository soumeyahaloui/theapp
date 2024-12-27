import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')  # Width for mobile devices
Config.set('graphics', 'height', '640')  # Height for mobile devices
Config.write()

from kidsvoc import MyApp  # Importing the MyApp class from the src folder

def main():
    app = MyApp()
    app.run()

if __name__ == '__main__':
    main()
