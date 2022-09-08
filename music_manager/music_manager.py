import sys,  os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QMenu


from handlers import WidgetHandler, EventHandler, SongHandler
from objects import Song
from utils import HOME
from db.db_manager import DBManager
from config import Config

class MusicManager:

    def __init__(self):
        self.create_home()
        self.db = DBManager()
        self.checkDirectories()
        self.config = Config()

    def setup_widget_handler(self):
        self.widget_handler.MAINTABLE.setup(self.song_handler, self.widget_handler)
        self.widget_handler.FILTER.setup(self.song_handler, self.widget_handler)
        self.widget_handler.PLAYLIST.setup(self.song_handler)

    def launch(self):
        app = QApplication(sys.argv)
        self.widget_handler = WidgetHandler(self, self.config, self.db)
        self.song_handler = SongHandler(self.db, self.widget_handler)
        self.setup_widget_handler()
        self.widget_handler.GUI.show()
        self.event_handler = EventHandler(self.widget_handler)

        if not self.config.get_directory_path():
            search_dialog = self.widget_handler.set_search_dialog(self.config, self.widget_handler.GUI)
            ret = search_dialog.exec_()
            if not ret == QDialog.Accepted:
                return QApplication.quit()
        self.info = []
        self.load_songs()
        # self.create_tree()
        self.widget_handler.GUI.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget_handler.GUI.tableWidget.customContextMenuRequested.connect(self.widget_handler.MAINTABLE.table_widget_context_menu)
        app.exec_()

    def create_home(self):
        """
        Create, if not exist, the home folder: music_manager
        """
        if not os.path.exists(HOME):
            os.makedirs(HOME)

    def checkDirectories(self):
        """
        Create directories in home if not exist
        """
        if not os.path.exists(HOME + 'tmp'):
            os.makedirs(HOME + 'tmp')
            open(HOME+'tmp/error.log',  'a').close()

    def reset_all(self):
        """
        set the programm back to start
        """
        self.widget_handler.GUI.musicframe.setVisible(False)
        self.widget_handler.reload_musicplayer()
        self.songs = {}
        self.filtersongs = []
        self.info = []
        self.widget_handler.GUI.trayicon.setIcon(QIcon('resources/trayicon.png'))

    def load_songs(self):
        """
        make the table and the checkboxes
        """
        paths = list(x for x in self.config.get_directory_path().iterdir() if x.is_file())
        self.song_handler.load_raw_songs(paths)
        self.widget_handler.MAINTABLE.fill_table()
        self.widget_handler.FILTER.get_allBoxes()
    
    def change_directory(self):
        self.db.update_playlist(self.widget_handler.PLAYLIST.playlist, self.widget_handler.PLAYLIST.name)
        self.widget_handler.MUSICPLAYER.pause_player()
        self.reset_all()

        search_dialog = self.widget_handler.set_search_dialog(self.config, self.widget_handler.GUI)
        search_dialog.exec_()
        self.song_handler.songs = {}
        self.widget_handler.FILTER.remove_all_checkboxes()
        self.load_songs()

    def refresh(self):
        self.db.update_playlist(self.widget_handler.PLAYLIST.playlist, self.widget_handler.PLAYLIST.name)
        self.reset_all()
        self.load_songs()

if __name__ == "__main__":
    MM = MusicManager()
    MM.launch()