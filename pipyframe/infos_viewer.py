# -*- coding: utf-8 -*-
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from frame_config import FrameConfiguration
from math import ceil
import time
import os
import pyowm

class WeatherViewer(ScatterLayout):
    """
        This class handles the weather information that is
        shown to the user
    """
    def __init__(self, **kwargs):
        super(WeatherViewer, self).__init__(**kwargs)
        # Allow the Viewer tobe on the fron when touched
        self.conf = FrameConfiguration()
        # Set the icon size to a percentage of the windows
        self.icon_size = [size_val*self.conf.icon_perc/100 for size_val in Window.size]
        owm = pyowm.OWM(self.conf.api_key)
        self.city_weather = owm.weather_at_place('Lingen,DE')
        self.weather_icon = self._get_current_weather_image()
        self.weather_text = self._get_current_weather()
        self.clk = Clock.schedule_interval(self.update_weather,self.conf.weather_refresh)

    def on_touch_up(self, touch):
        """
            Overload the Scatter on touch up method to save the position
            of the widget
        """
        super(WeatherViewer, self).on_touch_up(touch)
        print("Touch up from the clock, properties are:")
        print(self.size)

    def _get_current_weather(self):
        """
            Get the current weather with the proper formatting
        """
        weather = self.city_weather.get_weather()
        # TODO get city from here
        weather_str = '[color=148F77][b][size={}]Lingen : {}°C [/size][/b][/color]'.format(
            int(self.icon_size[0]), int(ceil(weather.get_temperature(unit='celsius').get('temp'))))
        return weather_str

    def _get_icon_path(self, icon_id):
        """
            Get the path to the icon weather
            :param the icon_id
            return the path to Image
        """
        #TODO: This has to be tested to always find the incons and be coonfigurable
        path =  os.path.join('../docs/weather_icons','{}.png'.format(icon_id))
        return path

    def _get_current_weather_image(self):
        weather = self.city_weather.get_weather()
        icon = weather.get_weather_icon_name()
        return self._get_icon_path(icon)

    def update_weather(self, dt):
        self.weather_icon = self._get_current_weather_image()
        self.weather_text = self._get_current_weather()

class ClockViewer(ScatterLayout):
    """
        This class handles the time information that is shown 
        to the user
    """
    #ctimer_text = StringProperty("")
    def __init__(self, **kwargs):
        super(ClockViewer, self).__init__(**kwargs)
        # Allow it to get always into the front on being touched
        self.conf = FrameConfiguration()
        self.icon_size = [size_val*self.conf.icon_perc/100 for size_val in Window.size]
        self.ctimer_text = self._get_current_date()
        self.clk = Clock.schedule_interval(self.update_time, int(self.conf.clock_refresh))

    def on_touch_up(self, touch):
        """
            Overload the Scatter on touch up method to save the position 
            of the widget
        """
        super(ClockViewer, self).on_touch_up(touch)
        print("Touch up from the clock viewer, properties are:")
        print(self.center)
        print(self.rotation)

    def _get_current_date(self):
        """
            Return the current data with the desired configuration
        """
        if '24h' in self.conf.clock_format:
            date_str = '[color=148F77][b][size={}]%H:%M:%S[/size]\n[size={}]%a, %d %B[/size][/color][/b]'.format(
                int(self.icon_size[0]), int(self.icon_size[1]))
        else:
            date_str = '[color=148F77][b][size={}]%I:%M:%S[/size][size={}] %p[/size]\n[size=25]%a, %d %B[/size][/b][/color]'.format(
                int(self.icon_size[0]), int(self.icon_size[1]))
        return time.strftime(date_str)

    def update_time(self,dt):
        """
            This function does the update of the time on screen
        """
        self.ctimer_text = self._get_current_date()


