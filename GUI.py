# -*- coding: utf-8 -*-
    
"""
Module implementing MainWindow.
"""
import pyglet
import magic
import sqlite3
import mutagen
import os.path
import random
from mutagen.easyid3 import *
from mutagen.mp3 import MP3
import xml.etree.cElementTree as ET

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from search import SearchDialog
from genre import Genre
from mplay import Music
from aplay import Amusic
from song import Song
from info import Info
from load import Loading
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
        self.setupUi(self)
        self.musicframe.setVisible(False)
        self.player= pyglet.media.Player()
        self.c.execute('SELECT volume FROM volume')
        self.volume = self.c.fetchone()['volume']
        self.tableWidget.hideColumn(0)
        self.playlistWidget.hideColumn(0)
        self.newPlaylistWidget.hideColumn(0)
        self.newPlaylistWidget.drop.connect(self.drop)
        self.playlistWidget.drop.connect(self.drop)
        self.dlg = SearchDialog()
        ret = self.dlg.exec_()
        if ret == QDialog.Accepted:
            self.currentDir = self.dlg.get_currentdir()
            self.files = self.dlg.get_files()
            self.PATH = self.dlg.get_path()
            self.checkboxes = []
            self.songs = {}
            self.make_Table()
        else:
            QApplication.quit()
        
    def dict_factory(self, cursor, row):
        """
        Für vereinfachte abfrage der SQL Ergebnisse.
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
        
    def create_object(self, path):
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
        self.songs.setdefault(path, Song(path,  data['title'],  data['album'],  data['interpreter'], data['comment'], data['cs'],  genre, data['length'], data['chance'], data['timesplayed'], data['rating']))
        
    def get_objectItems(self, path):
        """
        Vereinfachte Funktion um alles in einem Objekt zu erhalten.
        """
        return self.songs[path].get_all()
        
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
                self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
                self.conn.commit()
            
            self.interpreterIsNeeded(ointerpreter)
            self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name=?', (interpreter, ))
            interpreter_ID = self.c.fetchone()['interpreter_ID']
        return interpreter_ID
        
    def make_Table(self):
        self.load = Loading(len(self.files)-1)
        self.load.show()
        for i in range(len(self.files)):
            path = unicode(self.currentDir.absoluteFilePath(self.files[i]))
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
                        genre = ["unknown", ]
                        
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
                    genre = ["unknown", ]
                    
                info = MP3(path)
                length = int(info.info.length)
                    
                if (not self.searchpath(path)):
                    if (not self.searchartist(artist)):
                        interp = (None, artist)
                        self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
                
                    self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (artist,))
                  
                    interpreter_ID = self.c.fetchone()
                  
                    inserts = (path, title, album, interpreter_ID["interpreter_ID"], comment, 0, length, 100, 0, 10)
                    self.c.execute('INSERT INTO music VALUES(?,?,?,?,?,?,?,?,?,?)', inserts)
                    self.conn.commit()
                else:
                    interpreter_ID = self.testinterpreter(path, artist)
                    inserts = (title, album, interpreter_ID, path)
                    self.c.execute('UPDATE music SET title=?, album=?, interpreter_FK=? WHERE path=?', inserts)
                    self.conn.commit()
                    
                self.genrefactory(path, genre)
                self.create_object(path)
                self.load.set_loading(i)
                if i == len(self.files)-1:
                    self.load.close()
                
        self.fill_Table()
        self.get_allBoxes()
    
    def fill_Table(self):
        """
        Füllt die Tabelle komplett mit allen Songs.
        """
        self.tableWidget.setRowCount(0)
            
        for path in self.songs:
            self.add_line(path)
            
    def fill_row(self):
        song = self.get_objectItems(self.Spath)
        row = self.tableWidget.currentRow()
        qname = QTableWidgetItem(song['path'].split( "/")[-1])
        qtitle = QTableWidgetItem(song['title'])
        qalbum = QTableWidgetItem(song['album'])
        qinterpreter = QTableWidgetItem(song['interpreter'])
        qtimesplayed = QTableWidgetItem(unicode(song['timesplayed']))
        qrating = QTableWidgetItem(unicode(song['rating']))
        qgenres = QTableWidgetItem(', '.join(song['genre']))
        
        songs = [None, qname, qtitle, qalbum, qinterpreter, qgenres, qtimesplayed, qrating]
        
        for i in range(self.tableWidget.columnCount()):
            if i:
                self.tableWidget.setItem(row, i, songs[i])
        
    
    def add_line(self, path):
        """
        Fügt eine Zeile in die Tabelle ein.
        """
        song = self.get_objectItems(path)
        
        
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
        song = self.get_objectItems(self.Spath)
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
        
    def update_db(self):
        """
        Datenbank wird verändert.
        """
        song = self.get_objectItems(self.Spath)
        if not self.searchartist (song['interpreter']):
            interp = (None, song['interpreter'])
            self.c.execute('''INSERT INTO interpreter VALUES(?,?)''', interp)
            
        self.c.execute('SELECT interpreter_ID FROM interpreter WHERE interpreter_name = ?', (unicode(song['interpreter']), ))
        interpreter_ID = self.c.fetchone()
        
        ex = [song['title'], song['album'], interpreter_ID['interpreter_ID'], song['comment'], song['cs'], song['timesplayed'], song['chance'], song['rating'], self.Spath]
        self.c.execute('''UPDATE music SET title=?, album=?, interpreter_FK=?, comment=?, cs =?, times_played=?, chance=?, rating=? WHERE path = ?''', ex)
        self.conn.commit()
        
        if hasattr(self, 'ointerpreter'):
            self.interpreterIsNeeded(self.ointerpreter)
            
    def update_dball(self):
        """
        Datenbank wird verändert bei allen Veränderungen.
        """
        for path in self.songs:
            song = self.get_objectItems(path)
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
                
    def playlist_exists(self):
        self.c.execute('SELECT path FROM playlist')
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False
            
    def create_playlist(self):
        newplaylist = []
#        for row in len(self.newPlaylistWidget.getColumnCount)
        playlist = ET.Element("playlist")
        for path in newplaylist:
            song = ET.SubElement(playlist,  "song")
            ET.SubElement(song, "field1", name="played").text = 0
            ET.SubElement(song, "field2", name="path").text = path
        tree = ET.ElementTree(playlist)
        tree.write("playlists/test.xml")
        
        
                
    def playlist_load(self):
        if not self.playlist_exists():
            songs = []
            for song in self.songs:
                songs.append(song)
            random.shuffle(songs)
            for song in songs:
                self.c.execute('INSERT INTO playlist VALUES (?,0)', (song, ))
            self.conn.commit()
            
        self.c.execute('SELECT path, played FROM playlist')
        self.playlist = self.c.fetchall()
    
    def timeout(self):
        if self.paus < 5:
            self.paus += 1
        if self.player.playing and not self.single:
            self.update_progress()
            if int(self.player.time) >= self.maxlength:
                self.songs[self.Spath].update_timesplayed()
                self.player.seek(self.START)
                self.player.pause()
                self.playing = False
                
    def get_nextsong(self):
        self.update_db()
        self.tableWidget.setCurrentCell(self.index, 0)
        self.Spath = unicode(self.tableWidget.item(self.index,  0).text())
        rpath = os.path.relpath(self.Spath, os.path.abspath(__file__))[3:]
        source= pyglet.resource.media(rpath)
        self.player.queue(source)
        self.get_songinformation()
        
    def get_songinformation(self):
        self.song = self.songs[self.Spath].get_all()
        self.maxlength = self.song['length']
        self.timebar.setRange(0, self.maxlength*50)
        m, s = divmod(self.maxlength, 60)
        self.length.setText("/ %02d:%02d" % (m, s))
        self.timebar.setValue(0)
        self.time.setText("%02d:%02d" % (0, 0))
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
        
    def closeEvent(self, event):
        if hasattr(self, 'player'):
            self.player.pause()
            self.c.execute('UPDATE volume SET volume=? WHERE volume_ID=1', (unicode(self.player.volume), ))
            self.conn.commit()
        event.accept()
    
    @pyqtSignature("QTableWidgetItem*")
    def on_tableWidget_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.
        """
        
        if not self.musicframe.isVisible():
            self.musicframe.setVisible(True)
            self.index = self.tableWidget.currentRow()
            self.paus = 0
            self.playing = False
            self.single = False
            self.loop = QTimer()
            self.loop.timeout.connect(self.timeout)
            self.loop.start(100)
            self.START = 0.000001
            self.timebar.releasePlay.connect(self.releasePlay)
            self.timebar.progressMovement.connect(self.progressMovement)
            self.get_nextsong()
            self.player.play()
            self.player.volume = self.volume
            self.soundSlider.setValue(self.volume)
            self.soundSlider.setSliderPosition(self.volume)
        elif self.paus >= 5:
            self.paus = 0
            self.single = True
            self.index = self.tableWidget.currentRow()
            self.get_nextsong()
            self.player.next()
            self.single = False
            self.player.play()
            


    
    @pyqtSignature("QTableWidgetItem*")
    def on_tableWidget_itemActivated(self, item):
        """
        Wenn Item aktiviert wird, kann man dieses auf der Seite anpassen.
        """
        self.Spath = unicode(self.tableWidget.item(item.row(),  0).text())
        items = self.songs[self.Spath].get_all()
        self.lineEditTitle.setText(items['title'])
        self.lineEditInterpreter.setText(items['interpreter'])
        self.lineEditAlbum.setText(items['album'])
        self.lineEditComment.setText(items['comment'])
        self.spinBoxRating.setValue(int(items['rating']))
        self.csCheckBox.setChecked(items['cs'])

    @pyqtSignature("")
    def on_genreButton_clicked(self):
        """
        Genres zum Lied überarbeiten.
        """
        if hasattr(self, 'Spath'):
            del self.songs[self.Spath]
            self.gdlg = Genre(self.c, self.conn, self.Spath)
            self.gdlg.exec_()
            self.create_object(self.Spath)
            self.update_db()
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
            self.update_db()
            self.get_allBoxes()
            self.update_file()
            self.fill_row()
    
    @pyqtSignature("")
    def on_playbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if hasattr(self, 'play'):
            self.play.closeEvent(QCloseEvent())
        self.play = Music(self.songs)
        self.play.show()
        self.update_dball()
        self.fill_Table()
    
    @pyqtSignature("")
    def on_resetallbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        
        self.playlist = self.playlistWidget.items()
        self.playlistWidget.setRowCount(0)
        
        
        if self.playlist_exists():
            self.c.execute('DELETE FROM playlist')
            self.conn.commit()
            
        songs = []
        for song in self.songs:
            songs.append(song)
        random.shuffle(songs)
        for song in songs:
            self.c.execute('INSERT INTO playlist VALUES (?,0)', (song, ))
        self.conn.commit()
        
        self.c.execute('SELECT path, played FROM playlist')
        self.playlist = self.c.fetchall()
    
    @pyqtSignature("")
    def on_playallbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if hasattr(self, 'play'):
            self.play.closeEvent(QCloseEvent())
        self.playlist_load()
        self.play = Amusic(self.songs, self.playlist, self.c, self.conn)
        self.play.show()
        self.update_dball()
        self.fill_Table()
    
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
                self.get_nextsong()
                self.player.next()
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
            if self.index == len(self.songs) -1:
                self.index = 0
                self.get_nextsong()
            else:
                self.index += 1
                self.get_nextsong()
            self.player.next()
            self.single = False
    
    @pyqtSignature("int")
    def on_soundSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.player.volume = self.soundSlider.value()
    
    @pyqtSignature("int")
    def on_menuDatei_activated(self, itemId):
        """
        Slot documentation goes here.
        """
        if itemId == -5:
            self.dlg = SearchDialog()
            self.dlg.exec_()
            self.songs = {}
            for checkbox in self.checkboxes:
                self.genreLayout.removeWidget(checkbox)
                checkbox.hide()
            self.checkboxes.clear()
            self.currentDir = self.dlg.get_currentdir()
            self.files = self.dlg.get_files()
            self.PATH = self.dlg.get_path()
            self.make_Table()
        elif itemId == -6:
            self.close()
                
    
    @pyqtSignature("int")
    def on_menuInfo_activated(self, itemId):
        """
        Slot documentation goes here.
        """
        if itemId == -7:
            info = Info()
            info.exec_()
    
    @pyqtSignature("")
    def on_filterResetButton_clicked(self):
        """
        Slot documentation goes here.
        """
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)
            
    
    def drop(self, item):
        print "hi"
        
    def drag(self, drag):
        print drag.mimeData()
    
    @pyqtSignature("")
    def on_playlistSaveButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_createPlaylistButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.create_playlist()
