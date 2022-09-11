from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EventHandler(QObject):
    def __init__(self, widget_handler, parent = None):
        QObject.__init__(self, parent)
        self.widget_handler = widget_handler
        self.installEventFilter()
        self.make_connections()

    def installEventFilter(self):
        """
        install the Event Filters
        """
        self.widget_handler.GUI.playlistWidget.installEventFilter(self)
        self.widget_handler.GUI.tableWidget.installEventFilter(self)
        self.widget_handler.GUI.playlistTreeView.installEventFilter(self)
        self.widget_handler.GUI.musicdock.installEventFilter(self)

    def make_connections(self):
        """
        create the connects
        """
        self.widget_handler.GUI.playlistSearchLineEdit.view().listviewclose.connect(self.widget_handler.GUI.playlistSearchLineEdit.hidePopup)
        self.widget_handler.GUI.playlistWidget.playlistInfo.connect(self.widget_handler.PLAYLIST.playlist_add_paths)
        self.widget_handler.GUI.tableWidget.returnpressed.connect(self.widget_handler.PLAYLIST.table_to_playlist)
        self.widget_handler.GUI.playlistSearchLineEdit.lineEdit().returnPressed.connect(self.widget_handler.PLAYLIST.search_playlist)
        self.widget_handler.GUI.timebar.release_play.connect(self.widget_handler.MUSICPLAYER.release_play)
        self.widget_handler.GUI.timebar.progress_movement.connect(self.widget_handler.MUSICPLAYER.progress_movement)

    def eventFilter(self, source, e):
        """
        filter events
        """
        if source == self.widget_handler.GUI.playlistWidget:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return:
                    self.playCurrentSong()
                    self.playlistWidget.setCurrentCell(self.widget_handler.GUI.playlistWidget.currentRow(), 1)
                elif e.key() == Qt.Key_Delete:
                    if source.selectedItems():
                        rows = []
                        for i in source.selectedIndexes():
                            rows.append(i.row())
                        rows = list(set(rows))

                        for row in reversed(rows):
                            print(row)
                            print(row[1])
                        #     source.removeRow(row)

        if source == self.widget_handler.GUI.playlistTreeView:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Delete:
                    self.widget_handler.PLAYLIST.delete_selected_file()

        # if source == self.musicdock:
        #     if e.type() == QEvent.Close:
        #         self.closeMusic()
        #         e.ignore()
        #         return True

        return False