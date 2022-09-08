# -*- coding: utf-8 -*-
"""
Module implementing genre.
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from views.Ui_genre import Ui_genre

class Genre(QDialog, Ui_genre):
    """
    handle genre editing with dialog
    """
    def __init__(self, db, song, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.db = db
        self.song = song
        self.comboboxadd.lineEdit().returnPressed.connect(self.comboboxAddReturnPressed)
        self.Sgenres = self.db.get_all_genres_of_song(song)
        self.genres = self.db.get_all_genres()
        self.set_list()

    def comboboxAddReturnPressed(self):
        """
        add genre if return is pressed in text field
        """
        self.on_buttonadd_clicked()

    def set_list(self):
        """
        create lists for the comboboxes
        """
        genres_name = []
        Sgenres_name = []

        for genre in self.Sgenres:
            if genre['genre'] != "empty":
                Sgenres_name.append(genre['genre'])
        self.comboboxdel.addItems(Sgenres_name)

        for genre in self.genres:
            if not Sgenres_name.contains(genre['genre']):
                if genre['genre'] != "empty":
                    genres_name.append(genre['genre'])
        self.comboboxadd.addItems(genres_name)

    @pyqtSlot()
    def on_buttondel_clicked(self):
        """
        genre is removed from song and if not needed, deleted
        """
        if self.comboboxdel.currentText():
            current_text = self.comboboxdel.currentText()
            genre_needed = self.db.remove_genre(current_text)

            if genre_needed:
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())
            else:
                self.comboboxadd.addItem(current_text)
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())

            if not self.comboboxdel.currentText():
                self.db.give_empty_genre(self.path)

    @pyqtSlot()
    def on_buttonadd_clicked(self):
        """
        genre added to song and if not exists, created
        """
        if self.comboboxadd.currentText():
            if not self.comboboxdel.currentText():
                self.c.execute('''SELECT genre_ID FROM genre WHERE genre_name = "empty" ''')
                delgenreID = self.c.fetchone()['genre_ID']
                delete = (self.path, delgenreID)
                self.c.execute('DELETE FROM music_genre WHERE music_path = ? AND genre_ID = ?',  delete)

            currentText = self.comboboxadd.currentText()
            if not self.db.genreExists(currentText):
                genreadd = (None, currentText)
                self.c.execute('''INSERT INTO genre VALUES (?,?) ''',  genreadd)

            if self.comboboxdel.findText(currentText) < 0:
                self.c.execute('SELECT genre_ID from genre WHERE genre_name = ?', (currentText, ))
                genre_ID = self.c.fetchone()['genre_ID']
                inserts = (self.path, genre_ID)
                self.c.execute('INSERT INTO music_genre VALUES(?,?)', inserts)
                self.comboboxdel.addItem(currentText)
                index = self.comboboxadd.findText(currentText)
                if index >= 0:
                    self.comboboxadd.removeItem(index)
                self.comboboxadd.clearEditText()

    @pyqtSlot()
    def on_buttonfinish_clicked(self):
        """
        close dialog
        """
        self.close()
