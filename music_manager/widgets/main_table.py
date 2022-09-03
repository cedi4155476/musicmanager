from PyQt5.QtWidgets import QTableWidgetItem

class MainTable:
    def __init__(self):
        self.widget_handler = None
        self.song_handler = None
    
    def setup(self, song_handler, widget_handler):
        self.widget_handler = widget_handler
        self.song_handler = song_handler


    def fill_table(self):
        """
        fill the table
        """
        self.widget_handler.GUI.tableWidget.setRowCount(0)

        self.widget_handler.GUI.tableWidget.setSortingEnabled(False)
        for song in self.song_handler.songs.values():
            self.add_line(song)
        self.widget_handler.GUI.tableWidget.setSortingEnabled(True)
    
    def add_line(self, song):
        """
        add row in table
        """
        row = self.widget_handler.GUI.tableWidget.rowCount()
        self.widget_handler.GUI.tableWidget.insertRow(row)
        self.widget_handler.GUI.tableWidget.setItem(row, 0, QTableWidgetItem(song.raw_path))
        self.widget_handler.GUI.tableWidget.setItem(row, 1, QTableWidgetItem(song.path.name))
        self.widget_handler.GUI.tableWidget.setItem(row, 2, QTableWidgetItem(song.title))
        self.widget_handler.GUI.tableWidget.setItem(row, 3, QTableWidgetItem(song.album))
        self.widget_handler.GUI.tableWidget.setItem(row, 4, QTableWidgetItem(song.interpreter))
        self.widget_handler.GUI.tableWidget.setItem(row, 5, QTableWidgetItem(', '.join(song.genres)))
        self.widget_handler.GUI.tableWidget.setItem(row, 6, QTableWidgetItem(song.times_played))
        self.widget_handler.GUI.tableWidget.setItem(row, 7, QTableWidgetItem(song.rating))

    def reload_table(self):
        """
        loads the table with the filtered songs
        """
        self.widget_handler.GUI.tableWidget.setRowCount(0)

        self.widget_handler.GUI.tableWidget.setSortingEnabled(False)
        for song in self.song_handler.filtersongs:
            self.add_line(song)
        self.widget_handler.GUI.tableWidget.setSortingEnabled(True)
