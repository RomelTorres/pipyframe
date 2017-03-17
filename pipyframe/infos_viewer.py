from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
import time
import pyowm

class WeatherViewer(Scatter):
    """
        This class handles the weather information that is
        shown to the user
    """
    def __init__(self, **kwargs):
        super(WeatherViewer, self).__init__(**kwargs)
        # Allow the Viewer tobe on the fron when touched
        self.auto_bring_to_front = True
        API_KEY = '965195b3d4775ac9ac611e19efac1d5c'
        owm = pyowm.OWM(API_KEY)
        self.city_weather = owm.weather_at_place('Lingen,DE')
        self.cweather = Label(text=self._get_current_weather())
        self.add_widget(self.cweather)
        self.clk = Clock.schedule_interval(self.update_weather,30)

    def on_touch_up(self, touch):
        """
            Overload the Scatter on touch up method to save the position
            of the widget
        """
        super(WeatherViewer, self).on_touch_up(touch)
        print("Touch up from the clock, properties are:")
        print(self.center)
        print(self.rotation)

    def _get_current_weather(self):
        """
            GEt the current weather with the proper formatting
        """
        weather = self.city_weather.get_weather()
        weather_str = 'Lingen:{} C - Humidity:{} \n {}\n Sunrise {}'.format(
            weather.get_temperature(unit='celsius').get('temp'), weather.get_humidity(),
            weather.get_detailed_status(), weather.get_sunset_time('iso'))
        
        return weather_str

    def update_weather(self, dt):
        self.cweather.text = self._get_current_weather()

class ClockViewer(Scatter):
    """
        This class handles the time information that is shown 
        to the user
    """
    def __init__(self, **kwargs):
        super(ClockViewer, self).__init__(**kwargs)
        # Allow it to get always into the front on being touched
        self.auto_bring_to_front = True
        self.ctime = Label(text=self._get_current_date())
        self.add_widget(self.ctime)
        # Let the scatter just be the size of the clock
        self.clk = Clock.schedule_interval(self.update_time, 1)

    def on_touch_up(self, touch):
        """
            Overload the Scatter on touch up method to save the position 
            of the widget
        """
        super(ClockViewer, self).on_touch_up(touch)
        print("Touch up from the clock, properties are:")
        print(self.center)
        print(self.rotation)

    def _get_current_date(self):
        """
            Return the current data with the desired configuration
        """
        return time.strftime('%b, %a %d %I %M: %S %p')

    def update_time(self,dt):
        """
            This function does the update of the time on screen
        """
        self.ctime.text = self._get_current_date()

