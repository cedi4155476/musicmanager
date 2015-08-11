# -*- coding: utf-8 -*-
"""
Module implementing genre.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_genre import Ui_genre

class Genre(QDialog, Ui_genre):
    """
    handle genre editing with dialog
    """
    def __init__(self, c, conn, path, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.c = c
        self.conn = conn
        self.path = path
        self.comboboxadd.lineEdit().returnPressed.connect(self.comboboxAddReturnPressed)
        self.get_songAllGenres()
        self.get_allGenres()
        self.set_list()

    def comboboxAddReturnPressed(self):
        """
        add genre if return is pressed in text field
        """
        self.on_buttonadd_clicked()

    def get_allGenres(self):
        """
        search all genres existing in db
        """
        self.c.execute('SELECT genre_name as genre FROM genre')
        self.genres = self.c.fetchall()

    def get_songAllGenres(self):
        """
        get all genres of editing song
        """
        self.c.execute('''SELECT genre.genre_name as genre, genre.genre_ID as ID FROM genre 
                                                JOIN music_genre 
                                                    ON genre.genre_ID = music_genre.genre_ID 
                                                    WHERE music_genre.music_path = ?''', (self.path, ))
        self.Sgenres = self.c.fetchall()

    def set_list(self):
        """
        create lists for the comboboxes
        """
        genres_name = QStringList()
        Sgenres_name = QStringList()

        for genre in self.Sgenres:
            if genre['genre'] != "empty":
                Sgenres_name.append(QString(genre['genre']))
        self.comboboxdel.addItems(Sgenres_name)

        for genre in self.genres:
            if not Sgenres_name.contains(QString(genre['genre'])):
                if genre['genre'] != "empty":
                    genres_name.append(QString(genre['genre']))
        self.comboboxadd.addItems(genres_name)

    def genreExists(self, genre):
        """
        checks if genre already exists
        """
        self.c.execute('SELECT genre_ID FROM genre WHERE genre_name = ?',  (genre, ))
        exist = self.c.fetchone()
        if exist:
            return True
        else:
            return False

    def genreIsNeeded(self, genre):
        """
        checks if genre is needed
        """
        self.c.execute('SELECT * FROM genre JOIN music_genre ON music_genre.genre_ID = genre.genre_ID WHERE genre.genre_name = ?', (genre, ))
        if self.c.fetchone():
            return True
        else:
            return False

    @pyqtSignature("")
    def on_buttondel_clicked(self):
        """
        genre is removed from song and if not needed, deleted
        """
        if self.comboboxdel.currentText():
            currentText = unicode(self.comboboxdel.currentText())
            self.c.execute('SELECT genre_ID FROM genre WHERE genre_name = ?',  (currentText, ))
            delgenreID = self.c.fetchone()['genre_ID']
            delete = (self.path, delgenreID)
            self.c.execute('DELETE FROM music_genre WHERE music_path = ? AND genre_ID = ?',  delete)

            if not self.genreIsNeeded(currentText):
                self.c.execute('DELETE FROM genre WHERE genre_name = ?', (currentText, ))
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())
            else:
                self.comboboxadd.addItem(QString(currentText))
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())

            if not self.comboboxdel.currentText():
                self.c.execute('''SELECT genre_ID from genre WHERE genre_name = "empty" ''')
                genre_ID = self.c.fetchone()['genre_ID']
                inserts = (self.path, genre_ID)
                self.c.execute('INSERT INTO music_genre VALUES(?,?)', inserts)

    @pyqtSignature("")
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

            currentText = unicode(self.comboboxadd.currentText())
            if not self.genreExists(currentText):
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

    @pyqtSignature("")
    def on_buttonfinish_clicked(self):
        """
        close dialog
        """
        self.close()
