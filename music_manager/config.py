import os, configparser, pathlib

from utils import HOME

class Config:
    def __init__(self):
        """
        Create the config file if it doesn't exist
        """
        if not os.path.isfile(HOME + 'config.ini'):
            self.config = configparser.ConfigParser()
            self.config.add_section('player')
            self.config.set('player', 'volume', "1")
            self.config.add_section('directory')
            self.config.set('directory', 'path', "")
            self.save_config()
        else:
            self.config = configparser.ConfigParser()
            self.config.read(HOME + 'config.ini')

    def get_directory_path(self):
        return pathlib.Path(self.config.get('directory', 'path'))

    def save_directory_path(self, path):
        self.config.set('directory', 'path', path)
        self.save_config()
        
    def get_volume(self):
        """
        Get the last used volume
        """
        try:
            return int(self.config.get('player', 'volume'))
        except configparser.NoSectionError:
            return 1

    def save_volume(self, volume):
        """
        Save the used volume
        """
        self.config.set('player', 'volume', str(volume))
        self.save_config()
    
    def save_config(self):
        with open(HOME + 'config.ini',  'w') as configfile:
            self.config.write(configfile)
