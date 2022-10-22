from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

class MainTable:
    def __init__(self):
        self.widget_handler = None
        self.song_handler = None
    
    def setup(self, song_handler, widget_handler):
        self.widget_handler = widget_handler
        self.song_handler = song_handler
        self.main_table = self.widget_handler.GUI.tableWidget
        
    def get_table_item(self, song):
        """
        get the tablewidgetitem with song
        """
        for i in range(self.main_table.rowCount()):
            if song.raw_path == self.main_table.item(i, 0).text():
                return self.main_table.item(i, 0)

    def select_row_by_song(self, song):
        self.main_table.clearSelection()
        path_item = self.get_table_item(song)
        self.main_table.item(path_item.row(),1).setSelected(True)
        self.main_table.scrollToItem(path_item)

    def fill_table(self):
        """
        fill the table
        """
        self.main_table.setRowCount(0)

        self.main_table.setSortingEnabled(False)
        for song in self.song_handler.songs.values():
            self.add_line(song)
        self.main_table.setSortingEnabled(True)
    
    def add_line(self, song):
        """
        add row in table
        """
        row = self.main_table.rowCount()
        self.main_table.insertRow(row)
        self.main_table.setItem(row, 0, QTableWidgetItem(song.raw_path))
        self.main_table.setItem(row, 1, QTableWidgetItem(song.path.name))
        self.main_table.setItem(row, 2, QTableWidgetItem(song.title))
        self.main_table.setItem(row, 3, QTableWidgetItem(song.album))
        self.main_table.setItem(row, 4, QTableWidgetItem(song.artist))
        self.main_table.setItem(row, 5, QTableWidgetItem(', '.join(song.genres)))
        self.main_table.setItem(row, 6, QTableWidgetItem(song.times_played))
        self.main_table.setItem(row, 7, QTableWidgetItem(song.rating))

    def update_row(self, song):
        """
        update row in table
        """
        row = self.get_table_item(song).row()
        qpath = QTableWidgetItem(song.raw_path)
        qname = QTableWidgetItem(song.path.name)
        qtitle = QTableWidgetItem(song.title)
        qalbum = QTableWidgetItem(song.album)
        qinterpreter = QTableWidgetItem(song.interpreter)
        qgenres = QTableWidgetItem(', '.join(song.genre))
        qtimesplayed = QTableWidgetItem(song.timesplayed)
        qrating = QTableWidgetItem(song.rating)

        songs = [qpath, qname, qtitle, qalbum, qinterpreter, qgenres, qtimesplayed, qrating]

        for i in range(self.tableWidget.columnCount()):
            if i:
                self.tableWidget.setItem(row, i, songs[i])

    def reload_table(self):
        """
        loads the table with the filtered songs
        """
        self.main_table.setRowCount(0)

        self.main_table.setSortingEnabled(False)
        for song in self.song_handler.filtersongs:
            self.add_line(song)
        self.main_table.setSortingEnabled(True)

    def disable_row(self, song):
        row = self.widget_handler.MAINTABLE.get_table_item(song).row()
        for c in range(self.main_table.columnCount()):
            item = self.main_table.item(row, c)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        path = self.main_table.item(row, 0).text()
        del self.song_handler.songs[path]

    def get_selected_song(self):
        item = self.main_table.item(self.main_table.currentRow(), 0)
        return self.song_handler.get_song_by_path(item.text())

    def table_widget_context_menu(self, pos):
        """
        create context menu for playlist tree
        """
        pass
        # self.contextindex = self.tableWidget.indexAt(pos)
        # if self.contextindex.isValid():
        #     menu = QMenu(self)
        #     menu.addAction('Edit', self.contextEditSong)
        #     menu.exec_(self.tableWidget.mapToGlobal(pos))

    def selection_changed(self, item):
        path = self.main_table.item(item.row(),  0).text()
        song = self.song_handler.songs.get(path)

        if not song.path.exists():
            self.disable_row(song)
            return
        self.widget_handler.SHORTEDIT.set_info(song)
        self.main_table.scrollToItem(item)