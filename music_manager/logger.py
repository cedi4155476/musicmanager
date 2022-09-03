import logging
from utils import HOME

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('musicmanager')
        self.add_handler()
        self.logger.setLevel(logging.WARNING)
        self.logger.propagate = False
    
    def add_handler(self):
        self.hdlr = logging.FileHandler(HOME + 'tmp/error.log')
        formatter = logging.Formatter('%(asctime)s %(message)s', "%Y-%m-%d")
        self.hdlr.setFormatter(formatter)
        self.logger.addHandler(self.hdlr)

    
    def warning(self, text):
        self.logger.warning(text)
    
    def close_handler(self):
        self.logger.removeHandler(self.hdlr)