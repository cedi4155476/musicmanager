# -*- coding: utf-8 -*-
import pdb
import time
"""
Module implementing MainWindow.
"""
import pyglet
import magic
import sqlite3
import mutagen
import os.path
import shutil
import random
from mutagen.easyid3 import *
from mutagen.mp3 import MP3
import xml.etree.cElementTree as ET

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from search import SearchDialog
from genre import Genre
from song import Song
from info import Info
from load import Loading
from musicplayer import MusicPlayer
from mylistview import MyListView
from Ui_GUI import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Das Hauptfenster wird erstellt und alle funktionen eingefügt.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self,  parent)
        
    def start(self):
        self.conn = sqlite3.connect('music.db')
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()
        self.db_create()
        self.setupUi(self)
        self.musicframe.setVisible(False)
        self.player= pyglet.media.Player()
        self.tableWidget.hideColumn(0)
        self.playlistWidget.hideColumn(0)
        self.playlistWidget.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        self.playlistWidget.setColumnWidth(2, 70)
        self.createSystemTray()
        self.playlistWidget.installEventFilter(self)
        self.tableWidget.installEventFilter(self)
        self.playlistTreeView.installEventFilter(self)
        self.musicdock.installEventFilter(self)
        self.playlistSearchLineEdit.setView(MyListView())
        self.playlistSearchLineEdit.view().listviewclose.connect(self.listViewClose)
        self.playlistWidget.playlistInfo.connect(self.playlistAdd)
        self.tableWidget.returnpressed.connect(self.tableWidgetReturnPressed)
        self.playlistSearchLineEdit.lineEdit().returnPressed.connect(self.playlistSearchEnterPressed)
        self.timebar.releasePlay.connect(self.releasePlay)
        self.timebar.progressMovement.connect(self.progressMovement)
        self.mdlg = MusicPlayer()
        self.musicplayersetslots()
        self.dlg = SearchDialog()
        ret = self.dlg.exec_()
        if ret == QDialog.Accepted:
            self.currentDir = self.dlg.get_currentdir()
            self.files = self.dlg.get_files()
            self.checkboxes = []
            self.songs = {}
            self.playlist = {}
            self.info = []
            self.RANDOMNESS = False
            self.loadErrors = []
            self.make_Table()
            self.create_tree()
        else:
            QApplication.quit()
            
    def db_create(self):
        try:
            self.c.execute('SELECT path FROM music')
        except:
            for line in open('dbcreate.sql'):
                try:
                    self.c.execute(line)
                except sqlite3.OperationalError:
                    break
            
    def musicplayersetslots(self):
        self.mdlg.playclicked.connect(self.mpplayclicked)
        self.mdlg.pauseclicked.connect(self.mppauseclicked)
        self.mdlg.nextclicked.connect(self.mpnextclicked)
        self.mdlg.previousclicked.connect(self.mppreviousclicked)
        self.mdlg.soundsliderchanged.connect(self.mpsoundsliderchanged)
        self.mdlg.ratingchanged.connect(self.mpratingchanged)
        self.mdlg.timechanged.connect(self.mptimechanged)
        self.mdlg.release.connect(self.mprelease)
        self.mdlg.playerhidden.connect(self.playerClosed)
        
    def createSystemTray(self):
        self.trayicon = QSystemTrayIcon(self)
        self.trayicon.setToolTip("Music Manager")
        self.traymenu = QMenu(self)
        self.traymenu.addAction("Open", self.openWindow)
        self.traymenu.addAction("Exit", self.exitWindow)
        self.trayicon.setContextMenu(self.traymenu)
        self.trayicon.setIcon(QIcon('resources/trayicon.png'))
        self.trayicon.activated.connect(self.trayactivated)
        self.doubleclicktimer = QTimer()
        self.doubleclicktimer.setSingleShot(True)
        self.doubleclicktimer.timeout.connect(self.waitForDoubleclick)
        self.trayicon.show()

    def reset_all(self):
        self.musicframe.setVisible(False)
        self.player= pyglet.media.Player()
        self.mdlg = MusicPlayer()
        self.songs = {}
        self.info = []
        self.loadErrors = []

    def dict_factory(self, cursor, row):
        """
        Für vereinfachte abfrage der SQL Ergebnisse.
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
        
    def editSong(self):
        #TODO: Add detailed Edit Dialog
        if hasattr(self, 'Spath'):
            pass

    def get_dbData(self, path):
        """
        Erstellt die Objekte für den gegebenen Pfad, welche einfach aufrufbar sind.
        """
        self.c.execute('''SELECT music.title as title, music.album as album, music.comment as comment, music.cs as cs,  genre.genre_name as genre, interpreter.interpreter_name as interpreter, music.length as length, music.chance as chance, music.times_played as timesplayed, music.rating as rating
                                    FROM music 
                                    LEFT OUTER JOIN music_genre 
                                        ON music.path = music_genre.music_path 
                                    LEFT OUTER JOIN genre 
                                        ON music_genre.genre_ID = genre.genre_ID
                                    LEFT OUTER JOIN interpreter
                                        ON music.interpreter_FK = interpreter.interpreter_ID
                                        WHERE music.path = ?''',  (path, ))
        datas = self.c.fetchall()
        i = 0
        genre = []
        for d in datas:
            if i == 0:
                data = d
                genre.append(d['genre'])
            else:
                genre.append(d['genre'])
            i +=1
        return data, genre
        
        
    def create_object(self, path, data, genre, playlist):
        if playlist:
            self.playlist.setdefault(path, Song(path,  data['title'],  data['album'],  data['interpreter'], data['comment'], data['cs'],  genre, data['length'], data['chance'], data['timesplayed'], data['rating']))
        else:
            self.songs.setdefault(path, Song(path,  data['title'],  data['album'],  data['interpreter'], data['comment'], data['cs'],  genre, data['length'], data['chance'], data['timesplayed'], data['rating']))

    def get_objectItems(self, object, path):
        """
        Vereinfachte Funktion um alles in einem Objekt zu erhalten.
        """
        return object[path].get_all()
        
    def get_fileGenres(self):
        self.fgenres = ['empty', ]
        i = 0
        for path in self.songs:
            for genres in self.songs[path].get_genres():
                for genre in self.fgenres:
                    if genres == genre:
                        i = 1
                if i == 0:
                    self.fgenres.append(genres)
                i = 0
        
    def get_fileInterpreters(self):
        self.finterpreters = []
        i = 0
        for path in self.songs:
            for interpreter in self.finterpreters:
                if interpreter == self.songs[path].get_interpreter():
                    i = 1
            if i == 0:
                self.finterpreters.append(self.songs[path].get_interpreter())
            i = 0
        
    def get_fileAlbums(self):
        self.falbums = []
        i = 0
        for path in self.songs:
            for album in self.falbums:
                if album == self.songs[path].get_album():
                    i = 1
            if i == 0:
                self.falbums.append(self.songs[path].get_album())
            i = 0
                
    def get_genresBoxes(self):
        """
        Erstellt die Checkboxes mit welchen man die Lieder nach Genres filtern kann.
        """
        
        i=0
        self.checkBox = QCheckBox(self.genreWidget)
        self.checkBox.setLayoutDirection(Qt.LeftToRight)
        self.checkBox.setObjectName('cs')
        self.genreLayout.setWidget(i, 0, self.checkBox)
        self.checkBox.setText('cs')
        self.checkBox.stateChanged.connect(self.checkCheckboxes)
        self.checkboxes.append(self.checkBox)
        i = 1
        for genre in self.fgenres:
            self.checkBox = QCheckBox(self.genreWidget)
            self.checkBox.setLayoutDirection(Qt.LeftToRight)
            self.checkBox.setObjectName(genre)
            self.genreLayout.setWidget(i, 0, self.checkBox)
            self.checkBox.setText(genre)
            self.checkBox.stateChanged.connect(self.checkCheckboxes)
            self.checkboxes.append(self.checkBox)
            i += 1
            
    def get_interpreterBoxes(self):
        """
        Erstellt die Checkboxes mit welchen man die Lieder nach Genres filtern kann.
        """
        i=0
        for interpreter in self.finterpreters:
            self.checkBox = QCheckBox(self.interpreterWidget)
            self.checkBox.setLayoutDirection(Qt.LeftToRight)
            self.checkBox.setObjectName(interpreter)
            self.interpreterLayout.setWidget(i, 0, self.checkBox)
            self.checkBox.setText(interpreter)
            self.checkBox.stateChanged.connect(self.checkCheckboxes)
            self.checkboxes.append(self.checkBox)
            i += 1
            
    def get_albumBoxes(self):
        """
        Erstellt die Checkboxes mit welchen man die Lieder nach Genres filtern kann.
        """
        i=0
        for album in self.falbums:
            self.checkBox = QCheckBox(self.albumWidget)
            self.checkBox.setLayoutDirection(Qt.LeftToRight)
            self.checkBox.setObjectName(album)
            self.albumLayout.setWidget(i, 0, self.checkBox)
            self.checkBox.setText(album)
            self.checkBox.stateChanged.connect(self.checkCheckboxes)
            self.checkboxes.append(self.checkBox)
            i += 1
            
    def get_allBoxes(self):
        for checkbox in self.checkboxes:
            self.genreLayout.removeWidget(checkbox)
            self.albumLayout.removeWidget(checkbox)
            self.interpreterLayout.removeWidget(checkbox)
            checkbox.hide()
        self.checkboxes = []
        
        self.get_fileGenres()
        self.get_fileAlbums()
        self.get_fileInterpreters()
        
        self.get_interpreterBoxes()
        self.get_albumBoxes()
        self.get_genresBoxes()
            
    def checkBoxTypes(self):
        type = 0
        self.genrecount = 0
        self.albumcount = 0
        self.interpretercount = 0
        genre = False
        album = False
        interpreter = False
        self.activatedcheckboxes = {}
        checkboxlist = []
        checkboxlist.append([])
        checkboxlist.append([])
        checkboxlist.append([])
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                if checkbox.parentWidget() == self.genreWidget:
                    if not genre:
                        genre = True
                        type += 1
                    checkboxlist[0].append(checkbox.text())
                    self.genrecount += 1
                    
                if checkbox.parentWidget() == self.albumWidget:
                    if not album:
                        album = True
                        type += 2
                    checkboxlist[1].append(checkbox.text())
                    self.albumcount += 1
                
                if  checkbox.parentWidget() == self.interpreterWidget:
                    if not interpreter:
                        interpreter = True
                        type += 4
                    checkboxlist[2].append(checkbox.text())
                    self.interpretercount += 1
                    
                if genre:
                    self.activatedcheckboxes.setdefault('genre', checkboxlist[0])
                if album:
                    self.activatedcheckboxes.setdefault('album', checkboxlist[1])
                if interpreter:
                    self.activatedcheckboxes.setdefault('interpreter', checkboxlist[2])
        return type
    
    def checkCheckboxes(self):
        """
        Überprüft die aktivierten Checkboxen und gibt die gesuchten Resultate aus.
        """
        type = self.checkBoxTypes()
        self.filtersongs = []
        self.genrefiltersongs = []
        self.albumfiltersongs = []
        self.interpreterfiltersongs = []
        self.genrefiltered = False
        self.albumfiltered = False
        self.interpreterfiltered = False
        for song in self.songs:
            self.filtersongs.append(self.songs[song])
        if type & 1:
            self.filter_genre(self.activatedcheckboxes)
            
        if type & 2:
            self.filter_album(self.activatedcheckboxes)
            
        if type & 4:
            self.filter_interpreter(self.activatedcheckboxes)
            
        if type:
            self.reload_Table()
        else:
            #Falls nichts ausgewählt wurde wird die komplette Liste ausgegeben.
            self.fill_Table()
            
    def filter_genre(self, titles):
        self.genrefiltered = True
        for song in self.filtersongs:
            i = 0
            cscleared = False
            sgenres = song.get_genres()
            cs = song.get_cs()
            for genre in sgenres:
                for key in titles:
                    for title in titles[key]:
                        if key == 'genre':
                            if title == genre or (title == 'cs' and cs and not cscleared):
                                if cs and not cscleared:
                                    cscleared = True
                                i += 1
                                if i == self.genrecount:
                                    self.genrefiltersongs.append(song)
                            
    def filter_album(self, titles):
        self.albumfiltered = True
        if self.genrefiltersongs:
            songs = self.genrefiltersongs
        else:
            songs = self.filtersongs
        for song in songs:
            i = 0
            album = song.get_album()
            for key in titles:
                for title in titles[key]:
                    if key == 'album':
                        if title == album:
                            i += 1
                            if i == self.albumcount:
                                self.albumfiltersongs.append(song)
            
            
    def filter_interpreter(self, titles):
        self.interpreterfiltered= True
        if self.albumfiltersongs:
            songs = self.albumfiltersongs
        elif self.genrefiltersongs:
            songs = self.genrefiltersongs
        else:
            songs = self.filtersongs
        for song in songs:
            i = 0
            interpreter = song.get_interpreter()
            for key in titles:
                for title in titles[key]:
                    if key == 'interpreter':
                        if title == interpreter:
                            i += 1
                            if i == self.interpretercount:
                                self.interpreterfiltersongs.append(song)
            
        
    def reload_Table(self):
        """
        Gibt nur die gesuchten Genres in der Liste aus.
        """
        self.tableWidget.setRowCount(0)
        if self.interpreterfiltered:
            pastes = self.interpreterfiltersongs
            
        elif self.albumfiltered:
            pastes = self.albumfiltersongs
            
        else:
            pastes = self.genrefiltersongs
        for paste in pastes:
            self.add_line(paste.get_path())
        
    def genrefactory(self, path, genres):
        for genre in genres:
            self.genreadd(path, genre)
            
    def genreadd(self, path, genre):
        if not self.searchgenre(genre):
            gen = (None, genre)
            self.c.execute("INSERT INTO genre VALUES (?,?)", gen)
            self.conn.commit()
                
        self.c.execute("SELECT genre_ID FROM genre WHERE genre_name = ?", (genre, ))
        genre_ID = self.c.fetchone()['genre_ID']
        
        
        if not self.genre_musicexists(path, genre_ID):
            insert = (path, genre_ID)
            self.c.execute("INSERT INTO music_genre VALUES (?,?)", insert)
            self.conn.commit()
                
        
    def genre_musicexists(self, path, genre_ID):
        tests = [path, genre_ID]
        self.c.execute('SELECT * FROM music_genre WHERE music_path=? AND genre_ID=?', tests)
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False
            
    def testinterpreter(self, path, interpreter):
        self.c.execute('SELECT interpreter_FK FROM music WHERE path=?', (path, ))
        interpreter_ID = self.c.fetchone()['interpreter_FK']
        self.c.execute('SELECT interpreter_name FROM interpreter WHERE interpreter_ID=?', (interpreter_ID, ))
        ointerpreter = self.c.fetchone()['interpreter_name']
        if ointerpreter != interpreter:
            if not self.searchartist(interpreter):
                interp = (None, interpreter)
                self.c.execute('INSERT INTO interpreter VALUES(?,?)', interp)
                self.conn.commit()
            
            self.interpreterIsNeeded(ointerpreter)
            self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name=?', (interpreter, ))
            interpreter_ID = self.c.fetchone()['interpreter_ID']
        return interpreter_ID
        
    def make_Table(self):
        paths = []
        for i in range(len(self.files)):
            paths.append(unicode(self.currentDir.absoluteFilePath(self.files[i])))
            
        self.fileAddInDB(paths, False)

        self.fill_Table()
        self.get_allBoxes()
        
    def getData(self, path):
        type = magic.from_file(path)
        if "MPEG ADTS" in type:
            try:
                audio = EasyID3(path)
                try:
                    title = audio["title"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    title = "unknown"
                    
                try:
                    album = audio["album"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    album = "unknown"
                    
                try:
                    genre = audio["genre"]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    genre = ["empty", ]
                    
                try:
                    artist = audio["artist"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    artist = "unknown"
            
                try:
                    comment = audio["album"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    comment = "empty"
            except (mutagen.id3.ID3NoHeaderError):
                title = "unknown"
                album = "unknown"
                artist = "unknown"
                comment = "empty"
                genre = ["empty", ]
                
            info = MP3(path)
            length = int(info.info.length)
        else:
            raise ValueError
        return title, album, artist, comment, genre, length
        
    def addInterpreter(self, artist):
        interp = (None, artist)
        self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
    
    def addMusic(self, path, title, album, artist, comment, genre, length):
        self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (artist,))
      
        interpreter_ID = self.c.fetchone()
      
        inserts = (path, title, album, interpreter_ID["interpreter_ID"], comment, 0, length, 0.5, 0, 10)
        self.c.execute('INSERT INTO music VALUES(?,?,?,?,?,?,?,?,?,?)', inserts)
    
    def fileAddInDB(self, paths, playlist):
        import logging
        logger = logging.getLogger('musicmanager')
        hdlr = logging.FileHandler('tmp/error.log')
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.WARNING)
        
        self.load = Loading(len(paths)*2)
        self.load.show()
        i = 0
        for path in paths:
            try:
                title, album, artist, comment, genre, length = self.getData(path)
                if not self.searchpath(path):
                    if (not self.searchartist(artist)):
                        self.addInterpreter(artist)
                    self.genrefactory(path, genre)
            except ValueError:
                logger.warning("failed to load: "+path)
                self.loadErrors.append(path)
            i+=1
            self.load.progressBar.setValue(i)
        self.conn.commit()
        
        for path in paths:
            try:
                title, album, artist, comment, genre, length = self.getData(path)
                if not self.searchpath(path):
                    self.addMusic(path, title, album, artist, comment, genre, length)
                else:
                    interpreter_ID = self.testinterpreter(path, artist)
                    inserts = (title, album, interpreter_ID, path)
                    self.c.execute('UPDATE music SET title=?, album=?, interpreter_FK=? WHERE path=?', inserts)
            except ValueError:
                pass
            i+=1
            self.load.progressBar.setValue(i)
            if i >= len(paths)*2:
                self.load.close()
        self.conn.commit()
        
        for path in paths:
            try:
                data, genre = self.get_dbData(path)
                self.create_object(path, data, genre, playlist)
            except:
                pass
        if len(self.loadErrors) > 0:
            errorBox = QMessageBox(0, "loading Error", str(len(self.loadErrors)) + " files failed to load \n Watch out for special character or if it is a mp3 file \n More infos about the files in error.log file")
            errorBox.exec_()

    def fill_Table(self):
        """
        Füllt die Tabelle komplett mit allen Songs.
        """
        self.tableWidget.setRowCount(0)
            
        for path in self.songs:
            self.add_line(path)
            
    def fill_row(self):
        song = self.get_objectItems(self.songs, self.Spath)
        row = self.tableWidget.currentRow()
        qname = QTableWidgetItem(song['path'].split( "/")[-1])
        qpath = QTableWidgetItem(song['path'])
        qtitle = QTableWidgetItem(song['title'])
        qalbum = QTableWidgetItem(song['album'])
        qinterpreter = QTableWidgetItem(song['interpreter'])
        qtimesplayed = QTableWidgetItem(unicode(song['timesplayed']))
        qrating = QTableWidgetItem(unicode(song['rating']))
        qgenres = QTableWidgetItem(', '.join(song['genre']))
        
        songs = [qpath, qname, qtitle, qalbum, qinterpreter, qgenres, qtimesplayed, qrating]
        
        for i in range(self.tableWidget.columnCount()):
            if i:
                self.tableWidget.setItem(row, i, songs[i])
        
    
    def add_line(self, path):
        """
        Fügt eine Zeile in die Tabelle ein.
        """
        song = self.get_objectItems(self.songs, path)
        
        
        qname = QTableWidgetItem(song['path'].split( "/")[-1])
        qpath = QTableWidgetItem(song['path'])
        qtitle = QTableWidgetItem(song['title'])
        qalbum = QTableWidgetItem(song['album'])
        qinterpreter = QTableWidgetItem(song['interpreter'])
        qtimesplayed = QTableWidgetItem(unicode(song['timesplayed']))
        qrating = QTableWidgetItem(unicode(song['rating']))
        
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, qpath)
        self.tableWidget.setItem(row, 1, qname)
        self.tableWidget.setItem(row, 2, qtitle)
        self.tableWidget.setItem(row, 3, qalbum)
        self.tableWidget.setItem(row, 4, qinterpreter)
        
        if song['genre'][0]:
            qgenres = QTableWidgetItem(', '.join(song['genre']))
            self.tableWidget.setItem(row, 5, qgenres)
        self.tableWidget.setItem(row, 6, qtimesplayed)
        self.tableWidget.setItem(row, 7, qrating)
        
    
    def searchpath(self,  path):
        """
        Überprüft ob Datei bereits in der Datenbank existiert.
        """
        self.c.execute("SELECT path FROM music WHERE path = ?", (path, ))
        empty = self.c.fetchone()
        if (empty):
            return True
        else:
            return False
        
    def interpreterIsNeeded(self, interpreter):
        """
        Überprüft ob der Interpreter noch benutzt wird, sonst wird er gelöscht.
        """
        self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (unicode(interpreter), ))
        interpreter_ID = self.c.fetchone()
        self.c.execute('SELECT interpreter_FK FROM music WHERE interpreter_FK = ?', (interpreter_ID['interpreter_ID'], ))
        if self.c.fetchone():
            return True
        else:
            self.c.execute('DELETE FROM interpreter WHERE interpreter_ID = ?', (interpreter_ID['interpreter_ID'], ))
            self.conn.commit()
    
    def searchgenre(self, genre):
        self.c.execute("SELECT genre_name FROM genre WHERE genre_name = ?", (genre, ))
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False
    
    def searchartist(self,  artist):
        """
        Überprüft ob der Artist (Interpreter) bereits existiert.
        """
        self.c.execute("SELECT interpreter_name FROM interpreter WHERE interpreter_name = ?", (artist,))
        empty = self.c.fetchone()
        if (empty):
            return True
        else:
            return False
            
    def update_file(self):
        """
        Metadaten der Datei ändern.
        """
        song = self.get_objectItems(self.songs, self.Spath)
        try:
            audio = EasyID3(self.Spath)
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(self.Spath, easy=True)
            audio.add_tags()
        genres = []
        
        for genre in song["genre"]:
            genres.append(genre)
        
        audio["title"] = song["title"]
        audio["album"] = song["album"]
        audio["artist"] = song["interpreter"]
        audio["genre"] = genres
        
        audio.save()
        
    def update_db(self, object, path):
        """
        Datenbank wird verändert.
        """
        song = self.get_objectItems(object, path)
        if not self.searchartist (song['interpreter']):
            interp = (None, song['interpreter'])
            self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
            
        self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (unicode(song['interpreter']), ))
        interpreter_ID = self.c.fetchone()
        
        ex = [song['title'], song['album'], interpreter_ID['interpreter_ID'], song['comment'], song['cs'], song['timesplayed'], song['chance'], song['rating'], path]
        self.c.execute('''UPDATE music SET title=?, album=?, interpreter_FK=?, comment=?, cs =?, times_played=?, chance=?, rating=? WHERE path = ?''', ex)
        self.conn.commit()
        
        if hasattr(self, 'ointerpreter'):
            self.interpreterIsNeeded(self.ointerpreter)
            
    def update_dball(self, object):
        """
        Datenbank wird verändert bei allen Veränderungen.
        """
        for path in object:
            song = self.get_objectItems(object, path)
            if not self.searchartist (song['interpreter']):
                interp = (None, song['interpreter'])
                self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
                self.conn.commit()
                
            self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (unicode(song['interpreter']), ))
            interpreter_ID = self.c.fetchone()
            
            ex = [song['title'], song['album'], interpreter_ID['interpreter_ID'], song['comment'], song['cs'], song['timesplayed'], song['chance'], song['rating'], path]
            self.c.execute('''UPDATE music SET title=?, album=?, interpreter_FK=?, comment=?, cs =?, times_played=?, chance=?, rating=? WHERE path = ?''', ex)
        self.conn.commit()
        
    def get_playlistItemWithPath(self, path):
        for i in range(self.playlistWidget.rowCount()):
            if path == self.playlistWidget.item(i, 0).text():
                return self.playlistWidget.item(i, 0)
                
    def playerPlayNext(self):
            time.sleep(0.2)
            self.player.next()

    def start_randomplay(self):
        if not self.playlist:
            return
        if not self.musicframe.isVisible():
            self.musicframe.setVisible(True)
        alreadystarted =False
        self.RANDOMNESS = True
        self.count = len(self.playlist)
        self.randomcount = 0
        self.songlist = []
        self.index = 0
        self.paus = 0
        self.playing = False
        self.single = False
        self.loop = QTimer()
        self.loop.timeout.connect(self.timeout)
        self.loop.start(100)
        self.START = 0.000001
        if self.player.source:
            alreadystarted = True
        self.get_nextRandomSong()
        if alreadystarted:
            self.playerPlayNext()
        self.player.play()
        self.c.execute('SELECT volume FROM volume')
        self.volume = self.c.fetchone()['volume']
        self.player.volume = self.volume
        self.soundSlider.setValue(self.volume)
        self.soundSlider.setSliderPosition(self.volume)
        
    def increase_chance(self):
        for path in self.playlist:
            if path != self.song.get_path():
                self.playlist[path].increasechance(self.count)
        
    def decrease_chance(self):
        self.playlist[self.song.get_path()].decreasechance(self.count)
        
    def get_randomcount(self):
        for path in self.playlist:
            self.randomcount += self.playlist[path].get_chance()

    def timeout(self):
        if self.paus < 5:
            self.paus += 1
    #TODO: Play Icon and pause Icon
#        if self.player.playing and not self.playset:
#            self.trayicon.setIcon('path')
        if self.player.playing and not self.single:
            self.update_progress()
            self.mdlg.update_progress(self.player.time)
            if int(self.player.time) >= self.maxlength:
                self.playlist[self.Ppath].update_timesplayed()
                self.player.seek(self.START)
                self.on_nextbutton_clicked()
                
    def get_nextRandomSong(self):
        self.get_randomcount()
        randomnumber = random.randrange(int(self.randomcount*1000000))
        chance = 0
        for path in self.playlist:
            chance += int(self.playlist[path].get_chance()*1000000)
            if chance >= randomnumber:
                songpath = os.path.abspath(path)
                break
                
        self.randomcount = 0
        if not 'songpath' in locals():
            self.get_nextRandomSong()
            return
        self.song = self.playlist[songpath]
        self.songlist.append(self.song)
        self.index = len(self.songlist) - 1
        if os.path.isfile(songpath):
            self.Ppath = songpath
            source= pyglet.media.load(songpath)
        self.player.queue(source)
        self.decrease_chance()
        self.increase_chance()
        
        self.get_infos()
        
    def get_next(self):
        self.song = self.songlist[self.index]
        path = os.path.abspath(self.song.get_path())
        
        source= pyglet.media.load(path)
        self.player.queue(source)
        self.get_infos()
        
    def get_last(self):
        self.song = self.songlist[self.index]
        path = os.path.abspath(self.song.get_path())
        
        source= pyglet.resource.media(path)
        self.player.queue(source)
        
        self.get_infos()

    def get_nextsong(self):
        self.update_db(self.playlist, self.Ppath)
        self.playlistWidget.setCurrentCell(self.index, 1)
        path = unicode(self.playlistWidget.item(self.index,  0).text())
        path = os.path.abspath(path)
        if os.path.isfile(path):
            self.Ppath = path
            source= pyglet.media.load(path)
            self.player.queue(source)
            self.song = self.playlist[self.Ppath].get_all()
            self.get_songinformation()
            
    def get_infos(self):
        item = self.get_playlistItemWithPath(self.song.get_path())
        self.playlistWidget.setCurrentItem(item)
        song = self.song.get_all()
        self.maxlength = song['length']
        self.timebar.setRange(0, self.maxlength*50)
        m, s = divmod(self.maxlength, 60)
        self.length.setText("/ %02d:%02d" % (m, s))
        self.timebar.setValue(0)
        self.time.setText("%02d:%02d" % (0, 0))
        length = "/ %02d:%02d" % (m, s)
        range = self.maxlength*50
        self.send_songInfos(length, range)
        self.player.seek(self.START)
        
    def get_songinformation(self):
        self.maxlength = self.song['length']
        self.timebar.setRange(0, self.maxlength*50)
        m, s = divmod(self.maxlength, 60)
        self.length.setText("/ %02d:%02d" % (m, s))
        self.timebar.setValue(0)
        self.time.setText("%02d:%02d" % (0, 0))
        length = "/ %02d:%02d" % (m, s)
        range = self.maxlength*50
        self.send_songInfos(length, range)
        self.player.seek(self.START)
        
    def update_progress(self):
        self.timebar.setValue(int(self.player.time*50))
        m, s = divmod(int(self.player.time), 60)
        self.time.setText("%02d:%02d" % (m, s))
        
    def releasePlay(self):
        if not self.player.playing:
            if self.playing:
                self.player.play()
                self.playing = False
        
    def progressMovement(self, percent):
        if self.player.playing:
            self.player.pause()
            self.playing = True
        if not percent:
            percent = 0.00001
        self.player.seek(percent * self.maxlength)
        self.update_progress()
        
    def trayactivated(self, type):
        if type == 2:
            self.doubleclicktimer.stop()
            self.showNormal()
        elif type == QSystemTrayIcon.Trigger:
            self.doubleclicktimer.start(200)
                
    def waitForDoubleclick(self):
        self.traymenu.popup(QCursor.pos())
        
    def openWindow(self):
        self.showNormal()
        
    def exitWindow(self):
        self.player.pause()
        QApplication.quit()
        
    def closeEvent(self, event):
        if self.mdlg.isVisible() or self.musicdock.isVisible():
            self.hide()
        else:
            if hasattr(self, 'player'):
                self.player.pause()
                self.c.execute('UPDATE volume SET volume=? WHERE volume_ID=1', (unicode(self.player.volume), ))
                self.conn.commit()
                self.update_dball(self.playlist)
            QApplication.quit()
            event.accept()
        event.ignore()

    def playCurrentSong(self):
        if self.RANDOMNESS:
            self.musicframe.setVisible(False)
            self.player = pyglet.media.Player()
            self.RANDOMNESS = False
        if not self.playlist:
            return
        self.playlistTab.setCurrentIndex(1)
        if not self.musicframe.isVisible():
            self.musicframe.setVisible(True)
            self.index = self.playlistWidget.currentRow()
            self.paus = 0
            self.playing = False
            self.single = False
            self.loop = QTimer()
            self.loop.timeout.connect(self.timeout)
            self.loop.start(100)
            self.START = 0.000001
            self.Ppath = unicode(self.playlistWidget.item(self.index,  0).text())
            self.get_nextsong()
            self.player.play()
            self.c.execute('SELECT volume FROM volume')
            self.volume = self.c.fetchone()['volume']
            self.player.volume = self.volume
            self.soundSlider.setValue(self.volume)
            self.soundSlider.setSliderPosition(self.volume)
        elif self.paus >= 5:
            self.paus = 0
            self.single = True
            self.index = self.playlistWidget.currentRow()
            self.get_nextsong()
            self.playerPlayNext()
            self.single = False
            self.player.play()

    def create_tree(self):
        filter = QStringList()
        filter.append("*.xml")
        self.model = QFileSystemModel()
        rootpath = os.path.dirname(os.path.realpath(__file__))+ "/playlists"
        self.model.setRootPath(rootpath)
        self.model.setNameFilters(filter)
        self.playlistTreeView.setModel(self.model)
        index = self.model.index(rootpath)
        self.playlistTreeView.setRootIndex(index)
        self.playlistTreeView.hideColumn(1)
        self.playlistTreeView.hideColumn(2)
        self.playlistTreeView.hideColumn(3)
        self.playlistTreeView.setHeaderHidden(True)
        self.playlistTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.playlistTreeView.customContextMenuRequested.connect(self.playlistTreeContextMenu)
        
    def create_folder(self):
        if self.playlistFolderLineEdit.text():
            name = unicode(self.playlistFolderLineEdit.text())
            
            if self.playlistTreeView.selectedIndexes():
                index = self.playlistTreeView.selectedIndexes()[0]
                path = self.get_path(index)
                path += name
            else:
                path = "playlists/" + name

            if not os.path.exists(path):
                os.makedirs(path)
            else:
                errorBox = QMessageBox(0, "Directory already exists!", "The directory you want to create already exists")
                errorBox.exec_()
        else:
            errorBox = QMessageBox(0, "Missing folder name!", "Please enter a folder name")
            errorBox.exec_()
            
    def delete_selectedFile(self):
        if self.playlistTreeView.selectedIndexes():
            index = self.playlistTreeView.selectedIndexes()[0]
            path = self.get_path(index)
            if self.model.isDir(index):
                reply = QMessageBox.question(self, "Are you sure?", "Are you sure to delete the directory?\n All files and directories in it will be deleted.", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return
                shutil.rmtree(path)
            else:
                path += unicode(index.data().toString())
                reply = QMessageBox.question(self, "Are you sure?", "Are you sure to delete the file?", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return
                os.remove(path)

    def get_path(self, index):
        repath = []
        path = ""
        if self.model.isDir(index):
            repath.append(unicode(index.data().toString()))
        while True:
            index = index.parent()
            repath.append(unicode(index.data().toString()))
            if index.data().toString() == "playlists":
                break

        for rpath in reversed(repath):
            path += rpath + "/"
        return path
    
    def search_playlist(self):
        cursorposition = self.playlistSearchLineEdit.lineEdit().cursorPosition()
        matchlist = self.search_files(unicode(self.playlistSearchLineEdit.currentText()), self.model.index(self.model.rootPath()))
        if len(matchlist) == 1:
            idx = self.model.index(matchlist[0])
            self.playlistTreeView.setCurrentIndex(idx)
            self.playlistSearchLineEdit.clear()
        elif len(matchlist) > 1:
            tmp = self.playlistSearchLineEdit.currentText()
            self.playlistSearchLineEdit.clear()
            for name in matchlist:
                self.playlistSearchLineEdit.addItem(name)
            self.playlistSearchLineEdit.setEditText(tmp)
            self.playlistSearchLineEdit.showPopup()
            self.playlistSearchLineEdit.lineEdit().setFocus(Qt.PopupFocusReason)
            self.playlistSearchLineEdit.lineEdit().setCursorPosition(cursorposition)
            
    def search_files(self, name, parent):
        matchlist = []
        it = QDirIterator(parent.data().toString(), QDirIterator.Subdirectories)
        while it.hasNext():
            tmp = it.next()
            last = tmp.split("/")[-1]
            if name in last or name == tmp:
                matchlist.append(tmp)
        return matchlist
        
    def loadFileToPlaylist(self, index):
        if self.playlist and self.playlistLineEdit.text():
            reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.No:
                return
        self.playlistWidget.setRowCount(0)
        self.playlist = {}
        
        path = self.get_path(index)
        path += unicode(index.data().toString())
        playlistname, songs = self.load_playlist(path)
        self.playlistLineEdit.setText(playlistname['name'])
        for song in songs:
            self.playlistAdd(song['path'], False)
        self.playlistTab.setCurrentIndex(1)

    def songInDB(self, path):
        self.c.execute('SELECT path FROM music WHERE path = ?', (unicode(path), ))
        exist = self.c.fetchone()
        if exist:
            return True
        else:
            return False
            
    def load_playlist(self, path):
        tree = ET.parse(path)
        root = tree.getroot()
        songs = []
        for child in root:
            if child.tag == "name":
                playlistname = child.attrib
            elif child.tag == "song":
                songs.append(child.attrib)
        return playlistname, songs
        
    def create_playlist(self, shuffle):
        playlist = ET.Element("playlist")
        ET.SubElement(playlist, "name",  name=unicode(self.playlistLineEdit.text()))
        for i in range(self.playlistWidget.rowCount()):
            path = unicode(self.playlistWidget.item(i, 0).text())
            ET.SubElement(playlist,  "song", path=path, played="0")
        tree = ET.ElementTree(playlist)
        
        if self.playlistTreeView.selectedIndexes():
            playlistname = self.get_path(self.playlistTreeView.selectedIndexes()[0])
        else:
            playlistname = "playlists/"
        playlistname +=  unicode(self.playlistLineEdit.text()) + ".xml"
        
      
        if not self.playlistLineEdit.text() and not shuffle:
            errorBox = QMessageBox(0, "No Playlist Name", "Please insert a name for the playlist!")
            errorBox.exec_()
            
        elif self.playlistWidget.rowCount() == 0:
            errorBox = QMessageBox(0, "No Songs Selected", "Please Drag and Drop some songs in the Playlist!")
            errorBox.exec_()
            
        elif not os.path.isfile(playlistname):
            tree.write(playlistname)
            
        else:
            if not shuffle:
                reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return
                
            tree.write(playlistname)
        
    def tableToPlaylist(self):
        if self.playlist and self.playlistLineEdit.text():
            reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.No:
                return
        self.playlistWidget.setRowCount(0)
        self.playlist = {}
        for path in self.songs:
            self.playlistAdd(path, False)
        item = self.get_playlistItemWithPath(self.Spath)
        self.playlistWidget.setCurrentItem(item)
        self.playlistWidget.setFocus()
        self.playlistWidget.setCurrentCell(self.playlistWidget.currentRow(), 1)

    def playlistAdd(self, path, sort):
        existinplaylist = False
        exists = False
        path = unicode(path)
        for row in range(self.playlistWidget.rowCount()):
            if path == self.playlistWidget.item(row, 0).text():
                existinplaylist = True
                
        if path in self.songs or self.songInDB(path):
            exists = True
        
        if not existinplaylist:
            if not exists:
                self.fileAddInDB(list(path))
            data, genre = self.get_dbData(path)
            m, s = divmod(data['length'], 60)
            orlength = ('%02d:%02d' % (m, s))
            self.create_object(path, data, genre, True)
            
            qpath = QTableWidgetItem(path)
            qtitle = QTableWidgetItem(data['title'])
            qlength = QTableWidgetItem(orlength)
            qlength.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
            row = self.playlistWidget.rowCount()
            self.playlistWidget.insertRow(row)
            self.playlistWidget.setItem(row, 0, qpath)
            self.playlistWidget.setItem(row, 1, qtitle)
            self.playlistWidget.setItem(row, 2, qlength)
            if sort:
                self.playlistWidget.sortItems(1)

    def switchPlaylistTab(self):
        self.playlistTab.setCurrentIndex(1)

    def listViewClose(self):
        self.playlistSearchLineEdit.hidePopup()

    def tableWidgetReturnPressed(self):
        self.on_tableWidget_itemDoubleClicked(self.tableWidget.currentItem())

    def playlistTreeContextMenu(self, pos):
        index = self.playlistTreeView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            menu.addAction('loeschen', self.delete_selectedFile)
            if self.model.isDir(index):
                menu.addAction('Playlist erstellen', self.switchPlaylistTab)
            menu.exec_(self.playlistTreeView.mapToGlobal(pos))

    @pyqtSignature("QTableWidgetItem*")
    def on_tableWidget_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.
        """
        self.tableToPlaylist()
        self.playCurrentSong()

    @pyqtSignature("")
    def on_genreButton_clicked(self):
        """
        Genres zum Lied überarbeiten.
        """
        if hasattr(self, 'Spath'):
            del self.songs[self.Spath]
            self.gdlg = Genre(self.c, self.conn, self.Spath)
            self.gdlg.exec_()
            data, genre = self.get_dbData(self.Spath)
            self.create_object(self.Spath, data, genre, False)
            self.update_db(self.songs, self.Spath)
            self.update_file()
            self.get_allBoxes()
            self.fill_row()
    
    @pyqtSignature("")
    def on_saveButton_clicked(self):
        """
        Änderungen speichern.
        """
        if hasattr(self,  'Spath'):
            title = unicode(self.lineEditTitle.text())
            interpreter = unicode(self.lineEditInterpreter.text())
            album = unicode(self.lineEditAlbum.text())
            comment = unicode(self.lineEditComment.text())
            cs = self.csCheckBox.isChecked()
            rating = unicode(self.spinBoxRating.value())
            self.ointerpreter = self.songs[self.Spath].get_interpreter()

            self.songs[self.Spath].update(title, album, interpreter, comment,  cs, rating)
            self.update_db(self.songs, self.Spath)
            self.get_allBoxes()
            self.update_file()
            self.fill_row()
    
    @pyqtSignature("")
    def on_resetallbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        
        if hasattr(self, 'playlist'):
            self.playlistWidget.setRowCount(0)
            songs = []
            for song in self.playlist:
                songs.append(song)
            random.shuffle(songs)
            for song in songs:
                self.playlistAdd(song, False)
            self.playlistWidget.setFocus()
            self.playlistWidget.setCurrentCell(0, 1)
            self.create_playlist(True)
    
    @pyqtSignature("")
    def on_playallbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if hasattr(self, 'playlist'):
            if not self.playlistWidget.selectedIndexes():
                self.playlistWidget.setFocus()
                self.setCurrentCell(0, 1)
            self.playCurrentSong()
            
    @pyqtSignature("")
    def on_playbutton_clicked(self):
        self.start_randomplay()

    @pyqtSignature("")
    def on_playbutton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.player.playing:
            self.player.play()
            self.playing = True
    
    @pyqtSignature("")
    def on_pausebutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.player.playing:
            self.player.pause()
            self.playing = False
    
    @pyqtSignature("")
    def on_previousbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.player.time <= 3:
            if self.index > 0:
                self.single = True
                self.index -= 1
                if self.RANDOMNESS:
                    self.get_last()
                else:
                    self.get_nextsong()
                self.playerPlayNext()
                self.single = False
        else:
            self.player.seek(self.START)
    
    @pyqtSignature("")
    def on_nextbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.paus == 5:
            self.paus = 0
            self.single = True
            if self.RANDOMNESS:
                if self.index == len(self.songlist) -1:
                    self.get_nextRandomSong()
                else:
                    self.index += 1
                    self.get_next()
            else:
                if self.index == len(self.playlist) -1:
                    self.index = 0
                    self.get_nextsong()
                else:
                    self.index += 1
                    self.get_nextsong()
            self.playerPlayNext()
            self.single = False

    @pyqtSignature("int")
    def on_soundSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.player.volume = self.soundSlider.value()

    @pyqtSignature("QAction*")
    def on_menuBar_triggered(self, action):
        """
        Slot documentation goes here.
        """
        if action.text() == "Refresh":
            self.update_dball(self.playlist)
            self.reset_all()
            self.make_Table()

        elif action.text() == "Change Directory":
            self.reset_all()
            self.player.pause()
            self.dlg = SearchDialog()
            self.dlg.exec_()
            self.songs = {}
            for checkbox in self.checkboxes:
                self.genreLayout.removeWidget(checkbox)
                checkbox.hide()
            self.checkboxes 
            self.currentDir = self.dlg.get_currentdir()
            self.files = self.dlg.get_files()
            self.make_Table()

        elif action.text() == "Exit":
            QApplication.quit()

        elif action.text() == "Edit":
            self.editSong()

        elif action.text() == "Info":
            self.infowidget = Info(self)
            self.infowidget.show()

    @pyqtSignature("")
    def on_filterResetButton_clicked(self):
        """
        Slot documentation goes here.
        """
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
            
    def eventFilter(self, source, e):
        if source == self.playlistWidget:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return:
                    self.playCurrentSong()
                    self.playlistWidget.setCurrentCell(self.playlistWidget.currentRow(), 1)
                elif e.key() == Qt.Key_Delete:
                    if source.selectedItems():
                        rows = []
                        for i in source.selectedIndexes():
                            rows.append(i.row())
                        rows = list(set(rows))

                        for row in reversed(rows):
                            source.removeRow(row)

        if source == self.playlistTreeView:
            if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Delete:
                    self.delete_selectedFile()
                    
        if source == self.musicdock:
            if e.type() == QEvent.Close:
                self.closeMusic()
                e.ignore()
                return True

        return False

    
    @pyqtSignature("")
    def on_playlistSaveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.create_playlist(False)
        
    @pyqtSignature("QTableWidgetItem*")
    def on_playlistWidget_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.
        """
        self.playCurrentSong()
    
    @pyqtSignature("")
    def on_tableWidget_itemSelectionChanged(self):
        """
        Slot documentation goes here.
        """
        if self.tableWidget.selectedItems():
            item = self.tableWidget.selectedItems()[0]
            self.Spath = unicode(self.tableWidget.item(item.row(),  0).text())
            items = self.songs[self.Spath].get_all()
            self.lineEditTitle.setText(items['title'])
            self.lineEditInterpreter.setText(items['interpreter'])
            self.lineEditAlbum.setText(items['album'])
            self.lineEditComment.setText(items['comment'])
            self.spinBoxRating.setValue(int(items['rating']))
            self.csCheckBox.setChecked(items['cs'])
    
    @pyqtSignature("QModelIndex")
    def on_playlistTreeView_doubleClicked(self, index):
        """
        Slot documentation goes here.
        """
        if self.model.isDir(index):
            self.playlistTab.setCurrentIndex(1)
        else:
            self.loadFileToPlaylist(index)
    
    @pyqtSignature("")
    def on_playlistCreateFolderButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.create_folder()

    @pyqtSignature("")
    def on_playlistSearchButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.search_playlist()
    
    @pyqtSignature("")
    def on_playlistFolderLineEdit_returnPressed(self):
        """
        Slot documentation goes here.
        """
        self.create_folder()
        
    def playlistSearchEnterPressed(self):
        self.search_playlist()
    
    @pyqtSignature("bool")
    def on_musicdock_topLevelChanged(self, topLevel):
        """
        Slot documentation goes here.
        """
        if topLevel:
            self.musicdock.setVisible(False)
            self.mdlg.set_volume(self.volume)
            self.mdlg.showNormal()
            
    def playerClosed(self, int):
        self.musicdock.setVisible(True)
        self.musicdock.setFloating(False)
        if int == 0:
            self.closeMusic()

    def closeMusic(self):
        if self.player.playing:
            self.player.pause()
            self.playing = False
        self.musicframe.setVisible(False)
        self.Ppath = ""
        self.player= pyglet.media.Player()
        self.update_dball(self.playlist)

    def send_songInfos(self, length, timebarrange):
        items = self.get_objectItems(self.playlist, self.Ppath)
        self.mdlg.set_songInfos(items['title'], items['album'], items['interpreter'], items['rating'], length, timebarrange)

    def mpplayclicked(self):
        self.on_playbutton_2_clicked()
        
    def mppauseclicked(self):
        self.on_pausebutton_clicked()
        
    def mpnextclicked(self):
        self.on_nextbutton_clicked()
        
    def mppreviousclicked(self):
        self.on_previousbutton_clicked()
        
    def mpsoundsliderchanged(self, value):
        self.on_soundSlider_valueChanged(value)
        
    def mpratingchanged(self, rating):
        self.playlist[self.Ppath].set_rating(rating)
        
    def mptimechanged(self, percent):
        self.progressMovement(percent)
        self.mdlg.update_progress(int(self.player.time))
    
    def mprelease(self):
        self.releasePlay()
