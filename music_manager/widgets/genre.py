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
        self.comboboxadd.lineEdit().returnPressed.connect(self.on_buttonadd_clicked)
        self.Sgenres = self.db.get_all_genres_of_song(song)
        self.genres = self.db.get_all_genres()
        self.set_list()

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
            if not genre['genre'] in Sgenres_name:
                if genre['genre'] != "empty":
                    genres_name.append(genre['genre'])
        self.comboboxadd.addItems(genres_name)

    @pyqtSlot()
    def on_buttondel_clicked(self):
        """
        genre is removed from song and if not needed, deleted
        """
        if self.comboboxdel.currentText():
            current_index = self.comboboxdel.currentIndex()
            current_text = self.comboboxdel.currentText()
            genre_needed = self.db.remove_genre(current_text, self.song)

            if genre_needed:
                self.comboboxadd.addItem(current_text)
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())
            else:
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())

            if not self.comboboxdel.currentText():
                self.db.add_genre_to_song(self.song, "empty")
            self.comboboxdel.setCurrentIndex(current_index)

    @pyqtSlot()
    def on_buttonadd_clicked(self):
        """
        genre added to song and if not exists, created
        """
        if not self.comboboxadd.currentText():
            return

        current_index = self.comboboxadd.currentIndex()
        if not self.comboboxdel.currentText():
            self.db.remove_genre("empty", self.song)

        genre_name = self.comboboxadd.currentText()
        self.db.add_genre_to_song(self.song, genre_name)

        if self.comboboxdel.findText(genre_name) < 0:
            self.comboboxdel.addItem(genre_name)
            index = self.comboboxadd.findText(genre_name)
            if index >= 0:
                self.comboboxadd.removeItem(index)
            self.comboboxadd.clearEditText()
        self.comboboxadd.setCurrentIndex(current_index)

    @pyqtSlot()
    def on_buttonfinish_clicked(self):
        """
        close dialog
        """
        self.close()
