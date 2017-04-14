from kivy.config import ConfigParser
import os
import sys

class FrameConfiguration():
    """
        Class handling the frame configuration
    """
    def __init__(self, config_file='../config.ini', delay_pics = 10, random_direction=True,
                 possible_directions=['right','left','top','bottom'], allow_shuffle=True,
                 max_slides=5, configured_folder=None, use_database=True, icon_perc=20,
                 settings_time=3, database_path='../frame_state.json', show_time=True,
                 clock_refresh=1,clock_format='24h', show_weather=True, 
                 api_key_path='../openweathermap_key', weather_refresh=30,
                 background_quality=10, profile = False):
        """
            Init class with defaul values
        """
        self.delay_pics = delay_pics
        self.random_direction = random_direction
        self.possible_directions =possible_directions
        self.allow_shuffle = allow_shuffle
        self.max_slides = max_slides
        if configured_folder:
            if os.path.isdir(configured_folder):
                self.configured_folder = configured_folder
        else:
            self.configured_folder = None
        self.use_database = use_database
        self.show_time = show_time
        self.clock_refresh = clock_refresh
        self.clock_format = clock_format
        self.show_weather = show_weather
        self.weather_refresh = weather_refresh
        self.location = [None, None]
        self.icon_perc = icon_perc
        self.settings_time = settings_time
        self.background_quality=background_quality
        self.profile = profile
        self.ini = ConfigParser()
        # Try using what has been provided
        # if it does not work, look it up
        if os.path.isfile(database_path):
            self.database_path = database_path
        else:
            self.database_path = FrameConfiguration.find_db_file()
        if os.path.isfile(config_file):
            self.config_file = config_file
        else:
            cfile = FrameConfiguration.find_config_file()
            if cfile:
                self.config_file = cfile
            else:
                #TODO: ERROR handling
                print('No configuration found, left with defaults') 
        if os.path.isfile(api_key_path):
            self.api_key_path = api_key_path
        else:
            self.api_key_path = FrameConfiguration.find_apikey_file()
        self.api_key = self._read_apikey_from_file(api_key_path)
        self.ini.read(self.config_file)
        self.load_from_ini()
        if not self.configured_folder:
            raise ValueError('Cannot proceed to app if no folder for pics is configured')

    @staticmethod
    def find_config_file():
        """
            This function returns the configuration file path
            for the application, it can be saved in /etc/pipyframe
            or bundled with the app
            :return path to config file if found None otherwise
        """
        # By default here is where the config file should be stored
        path = '/etc/pipyframe/config.ini'
        if os.path.isfile(path):
            return path
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
        path = os.path.abspath(os.path.join(path,'config.ini'))
        if os.path.isfile(path):
            return path
        return None

    @staticmethod
    def find_apikey_file():
        """
            This function returns the path to where the api key is stored
            :return path to stored api key
        """
        # By default here is where the config file should be stored
        path = '/etc/pipyframe/openweathermap_key'
        if os.path.isfile(path):
            return path
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
        path = os.path.abspath(os.path.join(path,'openweathermap_key'))
        if os.path.isfile(path):
            return path
        return None
    @staticmethod
    def find_settings_file():
        """
            Find the settings file for the settings panel, it can be saved
            in /etc/pipyframe or bundled with the app
            :return path to settings config file if found None otherwise
        """
        # By default here is where the config file should be stored
        path = '/etc/pipyframe/settings.json'
        if os.path.isfile(path):
            return path
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
        path = os.path.abspath(os.path.join(path,'settings.json'))
        if os.path.isfile(path):
            return path
        return None
    
    @staticmethod
    def find_db_file():
        """
            Find the db file for the app, it can be saved
            in /var/pipyframe or bundled with the app
            :return path to settings config file
        """
        # By default here is where the config file should be stored
        path = '/var/pipyframe/frame_state.json'
        if os.path.isfile(path):
            return path
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)
        path = os.path.abspath(os.path.join(path,'frame_state.json'))
        return path

    @staticmethod
    def _read_apikey_from_file(api_file):
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
        self.icon_perc = self.ini.getint('FrameConfiguration','IconSizePercentage')
        allow_shuffle = self.ini.getboolean('FrameBehaviour','ShufflePics')
        self.profile = self.ini.getboolean('Developer','Profile')
        # This is the size of loaded slides from the Carousel kivy component
        self.max_slides = self.ini.getint('FrameBehaviour','BufferSize')
        self.settings_time = self.ini.getint('FrameBehaviour','SettingsTime')
        configured_folder = self.ini.get('FrameConfiguration','Folder')
        # TODO: Improve the Error handling, by transfering this to a function 
        if os.path.isdir(configured_folder):
            self.configured_folder = configured_folder
        else:
            if configured_folder.startswith('~'):
                configured_folder = os.path.expanduser(configured_folder)
                if os.path.isdir(configured_folder):
                    self.configured_folder = configured_folder
                else:
                    self.configured_folder = None
        self.use_database = self.ini.get('FrameConfiguration','UseDatabase')
        if self.use_database:
            path =  self.ini.get('FrameConfiguration','DatabasePath')
            if os.path.isfile(path):
                self.database_path = path
            else:
                self.database_path = FrameConfiguration.find_db_file()
        else:
            self.database_path = None
        self.show_time = self.ini.getboolean('ClockConfiguration','ShowTime')
        self.clock_refresh = self.ini.getint('ClockConfiguration','RefreshRate')
        self.clock_format = self.ini.get('ClockConfiguration','Format')
        self.show_weather = self.ini.getboolean('WeatherConfiguration','ShowWeather')
        key_path = self.ini.get('WeatherConfiguration','ApiKeyPath')
        if os.path.isfile(key_path):
            self.api_key_path = key_path
        else:
            self.api_key_path = FrameConfiguration.find_apikey_file()
        self.api_key = FrameConfiguration._read_apikey_from_file(self.api_key_path)
        self.weather_refresh =  self.ini.getint('WeatherConfiguration','RefreshRate')
        self.location = [self.ini.get('WeatherConfiguration','Country'), self.ini.get('WeatherConfiguration','City')]
        self.background_quality=self.ini.getint('FrameConfiguration','BackgroundQuality')
