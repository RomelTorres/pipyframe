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
    def __init__(self, **kwargs):
        super(FrameScreen, self).__init__(**kwargs)
        self.cviewer = CarouselViewer()
        self.add_widget(self.cviewer)

class FrameScreenApp(App):
    def build(self):
        return FrameScreen()

if __name__ == '__main__':
    FrameScreenApp().run()
