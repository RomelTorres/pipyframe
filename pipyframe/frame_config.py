from kivy.config import ConfigParser
import os

class FrameConfiguration():
    """
        Class handling the frame configuration
    """
    def __init__(self, config_file='../config.ini', delay_pics = 10, random_direction=True,
                 possible_directions=['right','left','top','bottom'], allow_shuffle=True,
                 max_slides=5, configured_folder=None, use_database=True, 
                 database_path='../frame_state.json',show_time=True,clock_refresh=1,clock_format='24h',
                 show_weather=True, api_key_path='../openweathermap_key', weather_refresh=30,
                 background_quality=10):
        """
            Init class with defaul values
        """
        self.delay_pics = delay_pics
        self.random_direction = random_direction
        self.possible_directions =possible_directions
        self.allow_shuffle = allow_shuffle
        self.max_slides = max_slides
        self.configured_folder = configured_folder
        self.use_database = use_database
        self.database_path = database_path
        self.show_time = show_time
        self.clock_refresh = clock_refresh
        self.clock_format = clock_format
        self.show_weather = show_weather
        self.api_key_path = api_key_path
        self.api_key = self._read_apikey_from_file(api_key_path)
        self.weather_refresh = weather_refresh
        self.location = [None, None]
        self.ini = ConfigParser()
        self.background_quality=background_quality
        if os.path.isfile(config_file):
            #TODO: Implement a config file searching function
            self.ini.read(config_file)
            self.load_from_ini()

    def _read_apikey_from_file(elf, api_file):
        '''
            Read the api key from a given file
            :param api_file the name of the file where the api is 
            located
        '''
        api_key = ''
        try:
            with open(api_file,'r') as f:
                api_key = ''.join(f.readlines()).strip()
        except (OSError, IOError) as e:
            api_key = None
        return api_key

    def load_from_ini(self):
        """
            Load configuration from the config file
        """
        #TODO: Apply a sanity check in here to some of the values, like paths
        self.delay_pics = self.ini.getint('FrameBehaviour','delayBetweenPics')
        self.random_direction = self.ini.getboolean('FrameBehaviour','RandomDirection')
        self.possible_directions = [d for d in self.ini.get('FrameBehaviour','PossibleDirections').split(',') if d]
        allow_shuffle = self.ini.getboolean('FrameBehaviour','ShufflePics')
        # This is the size of loaded slides from the Carousel kivy component
        self.max_slides = self.ini.getint('FrameBehaviour','BufferSize')
        self.configured_folder = self.ini.get('FrameConfiguration','Folder')
        self.use_database = self.ini.get('FrameConfiguration','UseDatabase')
        if self.use_database:
            self.database_path = self.ini.get('FrameConfiguration','DatabasePath')
        else:
            self.database_path = None
        self.show_time = self.ini.getboolean('ClockConfiguration','ShowTime')
        self.clock_refresh = self.ini.getint('ClockConfiguration','RefreshRate')
        self.clock_format = self.ini.get('ClockConfiguration','Format')
        self.show_weather = self.ini.getboolean('WeatherConfiguration','ShowWeather')
        self.api_key_path = self.ini.get('WeatherConfiguration','ApiKeyPath')
        self.api_key = self._read_apikey_from_file(self.api_key_path)
        self.weather_refresh =  self.ini.getint('WeatherConfiguration','RefreshRate')
        self.location = [self.ini.get('WeatherConfiguration','Country'), self.ini.get('WeatherConfiguration','City')]
        self.background_quality=self.ini.getint('FrameConfiguration','BackgroundQuality')
