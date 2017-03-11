from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from ConfigParser import SafeConfigParser
from random import randint
from picbuffering import PicBuffering
from dbhandler import DbHandler
import os

class CarouselViewer(Carousel):
    """
       The Carousel Viewer expands the Carousel class to show images in a slideshow in a memory
       friendly manner.
    """
    def __init__(self, **kwargs):
        """
            Init function, calls the parent class plus images to be shown
        """
        super(CarouselViewer, self).__init__(**kwargs)
        self.ini = SafeConfigParser()
        # Read configuration file
        self.ini.read('../config.ini')
        # Get initial configured folders to read pictures from
        folders = [folder for folder in self.ini.get('FrameConfiguration','Folders').split('\n') if folder]
        # Get delay between showing pictures
        self.delay_pics = self.ini.getint('FrameBehaviour','delayBetweenPics')
        self.random_direction = self.ini.getboolean('FrameBehaviour','RandomDirection')
        self.possible_directions = [d for d in self.ini.get('FrameBehaviour','PossibleDirections').split(',') if d]
        allow_shuffle = self.ini.getboolean('FrameBehaviour','ShufflePics')
        # This is the size of loaded slides from the Carousel kivy component
        self.max_slides = self.ini.getint('FrameBehaviour','BufferSize')
        use_database = self.ini.get('FrameConfiguration','UseDatabase')
        if use_database:
            self.database = DbHandler(self.ini.get('FrameConfiguration','DatabasePath'))
        else:
            self.disabled = None
        self.picbuffers = PicBuffering(database=self.database)
        # Get a variable for storing the last index
        self.previous_idx = 4
        # At the beginning do not load pictures into the seen queue (until the index_update
        # reaches zero or we have ran out of pictures in the seen queue)
        self.do_not_load = True
        # The current slides direction
        self.slide_direction = 'up'
        # Add pictures to buffer
        for folder in folders:
            self.picbuffers.add_from_folder(folder, allow_shuffle=allow_shuffle)
        # If allowed set a random direction for the pictures to show
        if self.random_direction:
            self.direction = self.get_random_direction()
        else:
            self.direction = self.possible_directions[0]    
        self.loop = False
        # Get from the buffer the first pictures to show
        self.current_paths = self.picbuffers.get_next_picture(num=self.max_slides)
        # Create the firs images that are going to be shown 
        self.images = []
        for path in self.current_paths:
            img = Image(source=path,allow_stretch=True, size=Window.size, nocache=True)
            self.images.append(img)
        # We add the widgets in a separate loop, because this will trigger an on_index event
        for img in self.images:     
            self.add_widget(img)
        # Schedule the clock at the very end
        self.clk = Clock.schedule_interval(self.load_next_cb, self.delay_pics)

    def get_random_direction(self):
        """
            Function to get a random direction from the available list of directions
        """
        return self.possible_directions[randint(0,len(self.possible_directions) - 1)]

    def load_next_cb(self, dt):
        """
            Callback for the load next picture
        """
        self.load_next()


    def on_index(self, *args):
        """
            Overloaded from the on_function in the caroussel class
        """
        super(CarouselViewer, self).on_index(*args)
        # Get the direction of the sliding
        slide_direction = 'up' if (self.previous_idx + 1) % self.max_slides == self.index else 'down'
        if self.slide_direction != slide_direction:
            direction_change = True
        else:
            direction_change = False
        self.slide_direction = slide_direction
        # Get the current index to update
        index_update = (self.index + 3) % self.max_slides
        # if we have rocked aroud once, we can load pictures
        if index_update == 0:
            self.do_not_load = False
        # Check if we did our first loop and set it to false
        if (self.slide_direction == 'up'):
            # Allow looping
            self.loop = True
            # Get the picture from the top
            if not self.do_not_load:
                # Save the current image to the seen queue
                self.picbuffers.add_to_seen(self.current_paths[index_update])
                src = self.picbuffers.get_next_picture()[0]
                self.images[index_update].source = src
                self.current_paths[index_update] = src
        else:
            # Save the current image to the next queue
            src = self.picbuffers.get_last_from_seen()[0]
            # IF the direction has changed we gotta undo the previous
            # step
            if direction_change:
                undo_index_update = (self.previous_idx + 3) % self.max_slides
                to_next = self.current_paths[undo_index_update]
                self.picbuffers.add_to_next(to_next, 'front')
                self.images[undo_index_update].source = src
                self.current_paths[undo_index_update] = src
                src = self.picbuffers.get_last_from_seen()[0]
            if src:
                # Allow looping
                self.loop = True
                # If something is found add it
                to_next = self.current_paths[index_update]
                self.picbuffers.add_to_next(to_next,'front')
                self.images[index_update].source = src
                self.current_paths[index_update] = src
            else:
                # There is nothing to show, deactivate looping
                self.loop = False
                # Don't load pictures in the seen queue
                self.do_not_load = True
        # Save the last index
        self.previous_idx = self.index
        if self.random_direction:
            self.direction = self.get_random_direction()

    def on_touch_down(self, touch):
        """
            Overload the on_touch_down function from the Carousel class
            in order to support actions on taps
        """
        # if zou touch the screen, the only direction allowed is right
        self.direction = 'right'
        # Stop the clock every time we touch a picture
        Clock.unschedule(self.clk)
        # call the parent class function
        if touch.is_double_tap:
            print('Oh double tap')
            print('Blacklisting {}-> {}'.format(self.index, self.current_paths[self.index]))
            # After blacklisting bring the next picture
            self.load_next()
        super(CarouselViewer, self).on_touch_down(touch)
    
    def on_touch_up(self, touch):
        """
            Overload the on_touch_up to restart the clock showing pictures
        """
        # Reschedule the clock
        self.clk = Clock.schedule_interval(self.load_next_cb, self.delay_pics)
        super(CarouselViewer, self).on_touch_up(touch)    

class FrameApp(App):
    def build(self):
        return CarouselViewer()

if __name__ == '__main__':
    FrameApp().run()
