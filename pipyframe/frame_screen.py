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
    #TODO: ALL this has to be improved to check properly for the file
    def get_application_config(self):
        return ('../config.ini')

    def build_config(self, config):
        config.read('../config.ini')



    def build_settings(self, settings):
        #TODO: Add a function looking for this json file
        settings.add_json_panel('Frame Settings', self.config,'../settings.json')

if __name__ == '__main__':
    FrameScreenApp().run()
