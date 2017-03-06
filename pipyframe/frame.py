from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.factory import Factory
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from picbuffering import PicBuffering

class CarouselViewer(Carousel):
    def __init__(self, **kwargs):
        super(CarouselViewer, self).__init__(**kwargs)
        self.picbuffers = PicBuffering()
        #TODO This is just for testing now
        self.picbuffers.add_from_folder('/home/rtorres/Dropbox/Philipphinen/102_PANA', allow_shuffle=True)
        #TODO this goes from a configuration file
        self.direction ='right'
        self.loop = 'True'
        # This is the size of loaded slides from the Carousel kivy component
        self.max_slides = 5
        # Get from the buffer the first pictures to show
        self.current_paths = self.picbuffers.get_next_picture(num=self.max_slides)
        # Create the firs images that are going to be shown 
        self.images = []
        for path in self.current_paths:
            img = Image(source=path,allow_stretch=True, size=Window.size, nocache=True)
            self.images.append(img)
            self.add_widget(img)
        self.clk = Clock.schedule_interval(self.load_next_cb, 2)

        # Get an init variable for the beginning
        self.started = True
        # Get a variable for storing the last index
        self.previous_index = 0
    
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
        # Get the current index to update
        index_update = (self.index + 3) % self.max_slides
        slide_direction = 'up' if (self.previous_index + 1) % self.max_slides == self.index else 'down'
        # Check if we did our first loop and set it to false
        if (slide_direction == 'up'):
            # Save the current image to the seen queue
            self.picbuffers.add_to_seen(self.current_paths[index_update])
            # Get the picture from the top
            src = self.picbuffers.get_next_picture()[0]
            self.images[index_update].source = src
            self.current_paths[index_update] = src
        else:
            # Save the current image to the next queue
            self.picbuffers.add_to_next(self.current_paths[index_update],'front')
            src = self.picbuffers.get_last_from_seen()[0]
            self.images[index_update].source = src
            self.current_paths[index_update] = src

        # Save the last index
        self.previous_index = self.index

class FrameApp(App):
    def build(self):
        return CarouselViewer()

if __name__ == '__main__':
    FrameApp().run()
