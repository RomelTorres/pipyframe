from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from carousel_viewer import CarouselViewer
from infos_viewer import ClockViewer
from frame_config import FrameConfiguration
import time

class FrameScreen(FloatLayout):
    """
        This class handles the frame application
    """
    
    def __init__(self, **kwargs):
        super(FrameScreen, self).__init__(**kwargs)
        self.clk = None
        self.conf = FrameConfiguration()
    
    def call_settings(self, dt):
        """
            This will call the settings screen on a long press
        """
        if self.clk:
            Clock.unschedule(self.clk)
        app = App.get_running_app()
        app.open_settings()

    def on_touch_up(self, touch):
        """
            Unschedule the clock
        """
        super(FrameScreen, self).on_touch_up(touch)
        if self.clk:
            Clock.unschedule(self.clk)

    def on_touch_down(self, touch):
        """
           Schedule a clock to call the settings screen
        """
        super(FrameScreen, self).on_touch_down(touch)
        self.clk = Clock.schedule_interval(self.call_settings, self.conf.settings_time)

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
