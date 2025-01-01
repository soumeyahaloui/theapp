from kivy.config import Config
from kivy.core.window import Window 


Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '720')
Config.write()


Window.size = (400, 720)


from kidsvoc import MyApp
