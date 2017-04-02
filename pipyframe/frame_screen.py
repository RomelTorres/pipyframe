from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from carousel_viewer import CarouselViewer
from infos_viewer import ClockViewer
from frame_config import FrameConfiguration
import time

class FrameScreen(FloatLayout):
    """
        This class handles the frame application
    """
    pass

class FrameScreenApp(App):
    """
        App to run the pipyframe
    """
    def build(self):
        return FrameScreen()
    
    def get_application_config(self):
        return FrameConfiguration.find_config_file()

    def build_config(self, config):
        config_path = FrameConfiguration.find_config_file() 
        config.read(config_path)

    def build_settings(self, settings):
        #TODO: Add a function looking for this json file
        settings_file = FrameConfiguration.find_settings_file()
        settings.add_json_panel('Frame Settings', self.config, settings_file)

if __name__ == '__main__':
    FrameScreenApp().run()
