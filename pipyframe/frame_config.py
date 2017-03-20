from ConfigParser import SafeConfigParser
import os

class FrameConfiguration():
    """
        Class handling the frame configuration
    """
    def __init__(self, config_file='../config.ini', delay_pics = 10, random_direction=True,
                 possible_directions=['right','left','top','bottom'], allow_shuffle=True,
                 max_slides=5, configured_folders=None, use_database=True, database_path='../frame_state.json'):
        """
            Init class with defaul values
        """
        self.delay_pics = delay_pics
        self.random_direction = random_direction
        self.possible_directions =possible_directions
        self.allow_shuffle = allow_shuffle
        self.max_slides = max_slides
        self.configured_folders = configured_folders
        self.use_database = use_database
        self.database_path = database_path
        self.ini = SafeConfigParser()
        if os.path.isfile(config_file):
            #TODO: Implement a config file searching function
            self.ini.read(config_file)
            self.load_from_ini()

    def load_from_ini(self):
        """
            Load configuration from the config file
        """
        self.delay_pics = self.ini.getint('FrameBehaviour','delayBetweenPics')
        self.random_direction = self.ini.getboolean('FrameBehaviour','RandomDirection')
        self.possible_directions = [d for d in self.ini.get('FrameBehaviour','PossibleDirections').split(',') if d]
        allow_shuffle = self.ini.getboolean('FrameBehaviour','ShufflePics')
        # This is the size of loaded slides from the Carousel kivy component
        self.max_slides = self.ini.getint('FrameBehaviour','BufferSize')
        self.configured_folders = [folder for folder in self.ini.get('FrameConfiguration','Folders').split('\n') if folder]
        self.use_database = self.ini.get('FrameConfiguration','UseDatabase')
        if self.use_database:
            self.database_path = self.ini.get('FrameConfiguration','DatabasePath')
        else:
            self.database_path = None
