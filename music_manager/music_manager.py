import sys,  os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox


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

    def launch(self):
        app = QApplication(sys.argv)
        self.widget_handler = WidgetHandler(self)
        self.song_handler = SongHandler(self.db, self.widget_handler)
        self.widget_handler.MAINTABLE.setup(self.song_handler, self.widget_handler)
        self.widget_handler.FILTER.setup(self.song_handler, self.widget_handler)
        main_window = self.widget_handler.GUI
        main_window.show()
        self.event_handler = EventHandler(self.widget_handler)

        if self.config.get_directory_path():
            files = list(x for x in self.config.get_directory_path().iterdir() if x.is_file())
        else:
            search_dialog = self.widget_handler.set_search_dialog(self.config, main_window)
            ret = search_dialog.exec_()
            if ret == QDialog.Accepted:
                files = search_dialog.get_files()
            else:
                return QApplication.quit()
        self.info = []
        self.load_songs(files)
        # self.create_tree()
        main_window.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        main_window.tableWidget.customContextMenuRequested.connect(main_window.tableWidgetContextMenu)
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
        if not os.path.exists(HOME + 'playlists'):
            os.makedirs(HOME + 'playlists')

        if not os.path.exists(HOME + 'tmp'):
            os.makedirs(HOME + 'tmp')
            open(HOME+'tmp/error.log',  'a').close()

    def reset_all(self):
        """
        set the programm back to start
        """
        self.widget_handler.GUI.musicframe.setVisible(False)
        # self.files = Widgets.SEARCH.get_files()
        # self.player= pyglet.media.Player()
        # self.mp = MusicPlayer()
        self.songs = {}
        self.filtersongs = []
        self.info = []
        self.loadErrors = []
        self.trayicon.setIcon(QIcon('resources/trayicon.png'))

    def load_songs(self, paths):
        """
        make the table and the checkboxes
        """

        self.song_handler.load_raw_songs(paths)
        self.widget_handler.MAINTABLE.fill_table()
        self.widget_handler.FILTER.get_allBoxes()


if __name__ == "__main__":
    MM = MusicManager()
    MM.launch()