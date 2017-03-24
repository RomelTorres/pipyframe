from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from carousel_viewer import CarouselViewer
from infos_viewer import ClockViewer
import time

class FrameScreen(FloatLayout):
    """
        This class handles the frame application
    """
    pass

class FrameScreenApp(App):
    def build(self):
        return FrameScreen()

if __name__ == '__main__':
    FrameScreenApp().run()
