from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EventHandler(QObject):
    def __init__(self, wh, parent = None):
        QObject.__init__(self, parent)
        self.wh = wh
        self.installEventFilter()
        self.make_connections()

    def installEventFilter(self):
        """
        install the Event Filters
        """
        self.wh.GUI.playlistWidget.installEventFilter(self)
        self.wh.GUI.tableWidget.installEventFilter(self)
        self.wh.GUI.playlistTreeView.installEventFilter(self)
        self.wh.GUI.musicdock.installEventFilter(self)

    def make_connections(self):
        """
        create the connects
        """
        self.wh.GUI.playlistSearchLineEdit.view().listviewclose.connect(self.listViewClose)
        self.wh.GUI.playlistWidget.playlistInfo.connect(self.playlistAdd)
        self.wh.GUI.tableWidget.returnpressed.connect(self.tableWidgetReturnPressed)
        self.wh.GUI.playlistSearchLineEdit.lineEdit().returnPressed.connect(self.playlistSearchEnterPressed)

    def listViewClose(self):
        """
        close popup if user wants to edit search
        """
        self.wh.GUI.playlistSearchLineEdit.hidePopup()

    def tableWidgetReturnPressed(self):
        """
        add all edit songs to playlist and play song if enter is pressed in edit table
        """
        self.wh.GUI.on_tableWidget_itemDoubleClicked(self.wh.GUI.tableWidget.currentItem())

    # TODO: this one should be done in playlist
    def playlistSearchEnterPressed(self):
        """
        search playlist or folder
        """
        self.search_playlist()

    # TODO: this one should be done in playlist
    def playlistAdd(self, paths, sort):
        """
        add song in playlist
        """
        self.fileAddInDB(paths, True)
        for path in paths:
            exception = False
            existinplaylist = False
            path = path
            for row in range(self.playlistWidget.rowCount()):
                if path == self.playlistWidget.item(row, 0).text():
                    existinplaylist = True

            for excep in self.loadErrors:
                if excep == path:
                    exception = True
                    break

            if not existinplaylist and not exception:
                try:
                    song = self.playlist[path].get_all()
                    m, s = divmod(song['length'], 60)
                    orlength = ('%02d:%02d' % (m, s))

                    qpath = self.getValidQTWI(path)
                    if not song['title']:
                        qtitle = self.getValidQTWI(song['path'].split( "/")[-1])
                    else:
                        qtitle = self.getValidQTWI(song['title'])
                    qlength = self.getValidQTWI(orlength)
                    qlength.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
                    row = self.playlistWidget.rowCount()
                    self.playlistWidget.insertRow(row)
                    self.playlistWidget.setItem(row, 0, qpath)
                    self.playlistWidget.setItem(row, 1, qtitle)
                    self.playlistWidget.setItem(row, 2, qlength)
                    if sort:
                        self.playlistWidget.sortItems(1)
                except (KeyError, UnboundLocalError):
                    pass

    def eventFilter(self, source, e):
        """
        filter events
        """
        # if source == self.playlistWidget:
        #     if e.type() == QEvent.KeyPress:
        #         if e.key() == Qt.Key_Return:
        #             self.playCurrentSong()
        #             self.playlistWidget.setCurrentCell(self.playlistWidget.currentRow(), 1)
        #         elif e.key() == Qt.Key_Delete:
        #             if source.selectedItems():
        #                 rows = []
        #                 for i in source.selectedIndexes():
        #                     rows.append(i.row())
        #                 rows = list(set(rows))

        #                 for row in reversed(rows):
        #                     source.removeRow(row)

        # if source == self.playlistTreeView:
        #     if e.type() == QEvent.KeyPress:
        #         if e.key() == Qt.Key_Delete:
        #             self.delete_selectedFile()

        # if source == self.musicdock:
        #     if e.type() == QEvent.Close:
        #         self.closeMusic()
        #         e.ignore()
        #         return True

        return False