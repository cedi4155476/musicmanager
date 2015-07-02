# -*- coding: utf-8 -*-
"""
Module implementing genre.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_genre import Ui_genre

class Genre(QDialog, Ui_genre):
    """
    Genre-Bearbeitung wird hier geregelt und auch per Dialog übersichtlich gestaltet.
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
        self.on_buttonadd_clicked()
    
    def get_allGenres(self):
        """
        Übergibt alle Genres von allen Liedern.
        """
        self.c.execute('SELECT genre_name as genre FROM genre')
        self.genres = self.c.fetchall()
    
    def get_songAllGenres(self):
        """
        Übergibt alle Genres des momentan ausgewählten Songes.
        """
        self.c.execute('''SELECT genre.genre_name as genre, genre.genre_ID as ID FROM genre 
                                                JOIN music_genre 
                                                    ON genre.genre_ID = music_genre.genre_ID 
                                                    WHERE music_genre.music_path = ?''', (self.path, ))
        self.Sgenres = self.c.fetchall()
    
    def set_list(self):
        """
        Erstellt die Listen, welche in den Comboboxes zu finden sind.
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
        Überprüft ob Genre bereits existiert.
        """
        self.c.execute('SELECT genre_ID FROM genre WHERE genre_name = ?',  (genre, ))
        exist = self.c.fetchone()
        if exist:
            return True
        else:
            return False
    
    def genreIsNeeded(self, genre):
        """
        Überprüft ob Genre gebraucht wird.
        """
        self.c.execute('SELECT * FROM genre JOIN music_genre ON music_genre.genre_ID = genre.genre_ID WHERE genre.genre_name = ?', (genre, ))
        if self.c.fetchone():
            return True
        else:
            return False
    
    @pyqtSignature("")
    def on_buttondel_clicked(self):
        """
        Genre wird vom Song entfernt und wenn es nicht mehr gebraucht wird, komplett gelöscht.
        """
        if self.comboboxdel.currentText():
            currentText = unicode(self.comboboxdel.currentText())
            self.c.execute('SELECT genre_ID FROM genre WHERE genre_name = ?',  (currentText, ))
            delgenreID = self.c.fetchone()['genre_ID']
            delete = (self.path, delgenreID)
            self.c.execute('DELETE FROM music_genre WHERE music_path = ? AND genre_ID = ?',  delete)
            self.conn.commit()
            
            if not self.genreIsNeeded(currentText):
                self.c.execute('DELETE FROM genre WHERE genre_name = ?', (currentText, ))
                self.conn.commit()
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())
            else:
                self.comboboxadd.addItem(QString(currentText))
                self.comboboxdel.removeItem(self.comboboxdel.currentIndex())
                
            if not self.comboboxdel.currentText():
                self.c.execute('''SELECT genre_ID from genre WHERE genre_name = "empty" ''')
                genre_ID = self.c.fetchone()['genre_ID']
                inserts = (self.path, genre_ID)
                self.c.execute('INSERT INTO music_genre VALUES(?,?)', inserts)
                self.conn.commit()
    
    @pyqtSignature("")
    def on_buttonadd_clicked(self):
        """
        Genre wird dem Song hinzugefügt und falls es noch nixht existierte, erstellt.
        """
        if self.comboboxadd.currentText():
            if not self.comboboxdel.currentText():
                self.c.execute('''SELECT genre_ID FROM genre WHERE genre_name = "empty" ''')
                delgenreID = self.c.fetchone()['genre_ID']
                delete = (self.path, delgenreID)
                self.c.execute('DELETE FROM music_genre WHERE music_path = ? AND genre_ID = ?',  delete)
                self.conn.commit()
                
                
            currentText = unicode(self.comboboxadd.currentText())
            if not self.genreExists(currentText):
                genreadd = (None, currentText)
                self.c.execute('''INSERT INTO genre VALUES (?,?) ''',  genreadd)
                self.conn.commit()
                
            if self.comboboxdel.findText(currentText) < 0:
                self.c.execute('SELECT genre_ID from genre WHERE genre_name = ?', (currentText, ))
                genre_ID = self.c.fetchone()['genre_ID']
                inserts = (self.path, genre_ID)
                self.c.execute('INSERT INTO music_genre VALUES(?,?)', inserts)
                self.conn.commit()
                self.comboboxdel.addItem(currentText)
                self.comboboxadd.clearEditText()
                self.comboboxadd.removeItem(self.comboboxadd.currentIndex())
    
    @pyqtSignature("")
    def on_buttonfinish_clicked(self):
        """
        Schliesst den Dialog.
        """
        self.close()
