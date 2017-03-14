from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
import time

class ClockViewer(Scatter):
    """
        This class handles the information that is shown 
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

