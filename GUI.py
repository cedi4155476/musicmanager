# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""
import pyglet, magic, sqlite3, mutagen, os.path, shutil, random, time, ConfigParser
import xml.etree.cElementTree as ET
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from search import SearchDialog
from edit import Edit
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
        """
        the constructor replacement so it does not crash
        """
        self.db_connect()
        self.create_config()
        self.setupUi(self)
        self.adjust_gui()
        self.createSystemTray()
        self.installEventFilter()
        self.make_connections()
        self.mdlg = MusicPlayer()
        self.musicplayersetslots()
        self.dlg = SearchDialog()
        ret = self.dlg.exec_()
        if ret == QDialog.Accepted:
            self.currentDir = self.dlg.get_currentdir()
            self.files = self.dlg.get_files()
            self.player= pyglet.media.Player()
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

    def db_connect(self):
        """
        connect to the db and if it did not exist make the db and it's tables
        """
        self.conn = sqlite3.connect('music.db')
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()
        try:
            self.c.execute('SELECT path FROM music')
        except sqlite3.OperationalError:
            for line in open('dbcreate.py'):
                try:
                    self.c.execute(line)
                except sqlite3.OperationalError:
                    break

    def create_config(self):
        if not os.path.isfile('config.ini'):
            cfgfile = open('config.ini', 'w')
            config = ConfigParser.ConfigParser()
            config.add_section('player')
            config.set('player', 'volume', 1)
            config.add_section('directory')
            config.set('directory', 'path', "")
            config.write(cfgfile)
            cfgfile.close()

    def adjust_gui(self):
        """
        adjust the gui
        """
        self.musicframe.setVisible(False)
        self.tableWidget.hideColumn(0)
        self.playlistWidget.hideColumn(0)
        self.playlistWidget.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        self.playlistWidget.setColumnWidth(2, 70)
        self.playlistSearchLineEdit.setView(MyListView())

    def installEventFilter(self):
        """
        install the Event Filters
        """
        self.playlistWidget.installEventFilter(self)
        self.tableWidget.installEventFilter(self)
        self.playlistTreeView.installEventFilter(self)
        self.musicdock.installEventFilter(self)

    def make_connections(self):
        """
        create the connects
        """
        self.playlistSearchLineEdit.view().listviewclose.connect(self.listViewClose)
        self.playlistWidget.playlistInfo.connect(self.playlistAdd)
        self.tableWidget.returnpressed.connect(self.tableWidgetReturnPressed)
        self.playlistSearchLineEdit.lineEdit().returnPressed.connect(self.playlistSearchEnterPressed)
        self.timebar.releasePlay.connect(self.releasePlay)
        self.timebar.progressMovement.connect(self.progressMovement)

    def musicplayersetslots(self):
        """
        connect the slots with the musicplayer class
        """
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
        """
        make the system tray icon and what is needed
        """
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
        """
        set the programm back to start
        """
        self.musicframe.setVisible(False)
        self.player= pyglet.media.Player()
        self.mdlg = MusicPlayer()
        self.songs = {}
        self.info = []
        self.loadErrors = []
        self.trayicon.setIcon(QIcon('resources/trayicon.png'))

    def dict_factory(self, cursor, row):
        """
        make it easier to read from db
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def editSong(self):
        """
        more edit varieties
        """
        if hasattr(self, 'Spath'):
            edit = Edit(self.songs[self.Spath])
            ret = edit.exec_()
            if ret == QDialog.Accepted:
                self.ointerpreter = self.songs[self.Spath].get_interpreter()
                self.oalbuminterpreter = self.songs[self.Spath].get_albuminterpreter()
                self.ocomposer = self.songs[self.Spath].get_composer()
                track, cd, bpm, title, interpreter, composer, albuminterpreter, album, year, comment = edit.get_infos()

                self.songs[self.Spath].updateInfos(track, cd, bpm, title, interpreter, composer, albuminterpreter, album, year, comment)
                self.update_db(self.songs, self.Spath)
                self.get_allBoxes()
                self.update_file()
                self.fill_row()

    def get_dbData(self, path):
        """
        get all infos from database for defined path
        """
        self.c.execute('''SELECT music.title as title, music.album as album, music.comment as comment, music.cs as cs,  genre.genre_name as genre, interpreter.interpreter_name as interpreter,
                                                music.length as length, music.chance as chance, music.times_played as timesplayed, music.rating as rating, music.bpm as bpm, music.year as year,
                                                music.track as track, composer.composer_name as composer, albuminterpreter.albuminterpreter_name as albuminterpreter, music.cd as cd
                                    FROM music 
                                    LEFT OUTER JOIN music_genre 
                                        ON music.path = music_genre.music_path 
                                    LEFT OUTER JOIN genre 
                                        ON music_genre.genre_ID = genre.genre_ID
                                    LEFT OUTER JOIN interpreter
                                        ON music.interpreter_FK = interpreter.interpreter_ID
                                    LEFT OUTER JOIN albuminterpreter
                                        ON music.albuminterpreter_FK = albuminterpreter.albuminterpreter_ID
                                    LEFT OUTER JOIN composer
                                        ON music.composer_FK = composer.composer_ID
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
        """
        create object for playlist or for editing in table
        """
        if playlist:
            self.playlist.setdefault(path, Song(path,  data['title'],  data['album'],  data['interpreter'], data['comment'], data['cs'],  genre, data['length'], data['chance'], data['timesplayed'], data['rating'], data['track'], data['cd'], data['bpm'], data['composer'], data['albuminterpreter'], data['year']))
        else:
            self.songs.setdefault(path, Song(path,  data['title'],  data['album'],  data['interpreter'], data['comment'], data['cs'],  genre, data['length'], data['chance'], data['timesplayed'], data['rating'], data['track'], data['cd'], data['bpm'], data['composer'], data['albuminterpreter'], data['year']))

    def get_fileGenres(self):
        """
        get the genres of the directory
        """
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
        """
        get the interpreters of the directory
        """
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
        """
        get the albums of the directory
        """
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
        creates the checkboxes for filtering with genres
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
        creates the checkboxes for filtering with interpreters
        """
        i=0
        for interpreter in self.finterpreters:
            if interpreter:
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
        creates the checkboxes for filtering with albums
        """
        i=0
        for album in self.falbums:
            if album:
                self.checkBox = QCheckBox(self.albumWidget)
                self.checkBox.setLayoutDirection(Qt.LeftToRight)
                self.checkBox.setObjectName(album)
                self.albumLayout.setWidget(i, 0, self.checkBox)
                self.checkBox.setText(album)
                self.checkBox.stateChanged.connect(self.checkCheckboxes)
                self.checkboxes.append(self.checkBox)
                i += 1

    def get_allBoxes(self):
        """
        removes then creates all boxes for filtering
        """
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
        """
        checks how many checkboxes are active and which types
        """
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
        checks all checkboxes and shows the filtered ones
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
        """
        filter for genre
        """
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
        """
        filter for album
        """
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
        """
        filter for interpreter
        """
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
        loads the table with the filtered songs
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
        """
        go through all genres in a file and add them to the db
        """
        for genre in genres:
            self.genreadd(path, genre)

    def genreadd(self, path, genre):
        """
        make the connections between song and genre or if it does not exist add the genre to the db and then make connection 
        """
        if not self.searchgenre(genre):
            gen = (None, genre)
            self.c.execute("INSERT INTO genre VALUES (?,?)", gen)

        self.c.execute("SELECT genre_ID FROM genre WHERE genre_name = ?", (genre, ))
        genre_ID = self.c.fetchone()['genre_ID']

        if not self.genre_musicexists(path, genre_ID):
            insert = (path, genre_ID)
            self.c.execute("INSERT INTO music_genre VALUES (?,?)", insert)

    def genre_musicexists(self, path, genre_ID):
        """
        check if connection already exists
        """
        tests = [path, genre_ID]
        self.c.execute('SELECT * FROM music_genre WHERE music_path=? AND genre_ID=?', tests)
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False

    def testAIC(self, path, type, value):
        '''
        check if the file A, I or C is different as the A, I or C in db
        '''
        fk = type + "_FK"
        ID = type + "_ID"
        name = type + "_name"
        self.c.execute('SELECT {id} FROM music WHERE path="{pt}"'.format(id=fk, pt=path))
        type_ID = self.c.fetchone()
        if type_ID:
            type_ID = type_ID[fk]
        self.c.execute('SELECT {nm} FROM {tb} WHERE {id}={tid}'.format(nm=name, tb=type, id=ID, tid=type_ID))
        ovalue = self.c.fetchone()
        if ovalue:
            ovalue = ovalue[name]
        if ovalue != value:
            if not self.searchAIC(type, value):
                ex = (None, value)
                self.c.execute('INSERT INTO {tb} VALUES(?,?)'.format(tb=type), ex)
            
            self.AICIsNeeded(type, ovalue)
            self.c.execute('SELECT {id} FROM {tb} WHERE {nm}=?'.format(id=ID, tb=type, nm=name), (value, ))
            type_ID = self.c.fetchone()
            if type_ID:
                type_ID = type_ID[ID]
        return type_ID

    def make_Table(self):
        """
        make the table and the checkboxes
        """
        paths = []
        for i in range(len(self.files)):
            paths.append(unicode(self.currentDir.absoluteFilePath(self.files[i])))

        self.fileAddInDB(paths, False)
        self.fill_Table()
        self.get_allBoxes()

    def getData(self, path):
        """
        get the fileinfos
        """
        from mutagen.mp3 import MP3, HeaderNotFoundError
        type = magic.from_file(path)
        try:
            info = MP3(path)
            length = int(info.info.length)
            if "MPEG ADTS" in type or "Audio file" in type or length:
                audio = mutagen.easyid3.EasyID3(path)
                try:
                    title = audio["title"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    title = ""

                try:
                    album = audio["album"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    album = ""

                try:
                    genre = audio["genre"]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    genre = ["empty", ]

                try:
                    interpreter = audio["artist"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    interpreter = ""

                try:
                    comment = audio["album"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    comment = ""

                try:
                    bpm = audio["bpm"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    bpm = ""

                try:
                    composer = audio["composer"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    composer = ""

                try:
                    cd = audio["discnumber"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    cd = ""

                try:
                    track = audio["tracknumber"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    track = ""

                try:
                    albuminterpreter = audio["albumartist"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    albuminterpreter = ""

                try:
                    year = audio["date"][0]
                except (mutagen.id3.ID3NoHeaderError, KeyError):
                    year = ""
            else:
                raise ValueError("Could not read File. Are you sure it is a music File?")

        except (mutagen.id3.ID3NoHeaderError):
                title = ""
                album = ""
                interpreter = ""
                comment = ""
                genre = ["empty", ]
                bpm = ""
                composer = ""
                cd = ""
                track = ""
                albuminterpreter = ""
                year = ""

        except HeaderNotFoundError:
            raise ValueError("Could not read File. Are you sure it is a music File?")

        return title, album, interpreter, comment, genre, length, bpm, composer, cd, track, albuminterpreter, year

    def addAIC(self, type, value):
        '''
        add AIC to db
        '''
        ex = (None, value)
        self.c.execute('INSERT INTO {tb} VALUES(?,?)'.format(tb=type), ex)

    def AICID(self, type, value):
        '''
        get ID of AIC
        '''
        ID = type + "_ID"
        name = type + "_name"
        self.c.execute('SELECT {id} FROM {tb} WHERE {nm}=?'.format(id=ID, tb=type, nm=name), (value, ))
        type_ID = self.c.fetchone()
        if type_ID:
            type_ID = type_ID[ID]
        return type_ID

    def addMusic(self, path, title, album, interpreter, comment, genre, length, bpm, composer, cd, track, albuminterpreter, year):
        """
        add song to db
        """
        interpreter_ID = self.AICID('interpreter', interpreter)
        albuminterpreter_ID = self.AICID('albuminterpreter', albuminterpreter)
        composer_ID = self.AICID('composer', composer)

        inserts = (path, title, album, interpreter_ID, comment, 0, length, 0.5, 0, 10, year, albuminterpreter_ID, composer_ID, bpm, track, cd)
        self.c.execute('INSERT INTO music VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', inserts)

    def fileAddInDB(self, paths, playlist):
        """
        add all songs in db and check for errors
        """
        import logging
        logger = logging.getLogger('musicmanager')
        hdlr = logging.FileHandler('tmp/error.log')
        formatter = logging.Formatter('%(asctime)s %(message)s', "%Y-%m-%d")
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.WARNING)
        logger.propagate = False
        
        if isinstance(paths, basestring):
            paths = (paths, )

        self.load = Loading(len(paths))
        self.load.show()
        i = 0
        for path in paths:
            path = unicode(path)
            try:
                title, album, interpreter, comment, genre, length, bpm, composer, cd, track, albuminterpreter, year = self.getData(path)
                if not self.searchpath(path):
                    if (not self.searchAIC('interpreter', interpreter)):
                        self.addAIC('interpreter', interpreter)
                    if (not self.searchAIC('albuminterpreter', albuminterpreter)):
                        self.addAIC('albuminterpreter', albuminterpreter)
                    if (not self.searchAIC('composer', composer)):
                        self.addAIC('composer', composer)
                    self.genrefactory(path, genre)
                    self.addMusic(path, title, album, interpreter, comment, genre, length, bpm, composer, cd, track, albuminterpreter, year)
                else:
                    interpreter_ID = self.testAIC(path, 'interpreter', interpreter)
                    albuminterpreter_ID = self.testAIC(path, 'albuminterpreter', albuminterpreter)
                    composer_ID = self.testAIC(path, 'composer', composer)
                    inserts = (title, album, interpreter_ID, albuminterpreter_ID, composer_ID, path)
                    self.c.execute('UPDATE music SET title=?, album=?, interpreter_FK=?, albuminterpreter_FK=?, composer_FK=? WHERE path=?', inserts)
            except ValueError, e:
                logger.warning("failed to load: %s\tError Message: %s" % (path, e))
                self.loadErrors.append(path)
            try:
                data, genre = self.get_dbData(path)
                self.create_object(path, data, genre, playlist)
            except:
                pass
            i+=1
            self.load.progressBar.setValue(i)
            if i >= len(paths):
                self.load.close()
        logger.removeHandler(hdlr)
        self.conn.commit()

        if len(self.loadErrors) > 0:
            errorBox = QMessageBox(0, "loading Error", str(len(self.loadErrors)) + " files failed to load \n Watch out for special character\n More infos about the files in tmp/error.log file")
            errorBox.exec_()

    def fill_Table(self):
        """
        fill the table
        """
        self.tableWidget.setRowCount(0)

        for path in self.songs:
            self.add_line(path)

    def fill_row(self):
        """
        update row in table
        """
        song = self.songs[self.Spath].get_all()
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
        add row in table
        """
        song = self.songs[path].get_all()

        qname = self.getValidQTWI(song['path'].split( "/")[-1])
        qpath = self.getValidQTWI(song['path'])
        qtitle = self.getValidQTWI(song['title'])
        qalbum = self.getValidQTWI(song['album'])
        qinterpreter = self.getValidQTWI(song['interpreter'])
        qgenres = self.getValidQTWI(', '.join(song['genre']))
        qtimesplayed = self.getValidQTWI(unicode(song['timesplayed']))
        qrating = self.getValidQTWI(unicode(song['rating']))

        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, qpath)
        self.tableWidget.setItem(row, 1, qname)
        self.tableWidget.setItem(row, 2, qtitle)
        self.tableWidget.setItem(row, 3, qalbum)
        self.tableWidget.setItem(row, 4, qinterpreter)
        self.tableWidget.setItem(row, 5, qgenres)
        self.tableWidget.setItem(row, 6, qtimesplayed)
        self.tableWidget.setItem(row, 7, qrating)

    def getValidQTWI(self, value):
        if value:
            return QTableWidgetItem(value)
        else:
            return QTableWidgetItem()

    def searchpath(self,  path):
        """
        check if record already exists
        """
        self.c.execute("SELECT path FROM music WHERE path = ?", (path, ))
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False

    def AICIsNeeded(self, type, value):
        '''
        check if AIC is still needed, else delete it
        '''
        ID = type + "_ID"
        fk = type + "_FK"
        name = type + "_name"
        self.c.execute('SELECT {id} FROM {tb} WHERE {nm}="{vl}"'.format(id=ID, tb=type, nm=name, vl=value))
        type_ID = self.c.fetchone()
        if type_ID:
            type_ID = type_ID[ID]
            
        self.c.execute('SELECT {fk} FROM music WHERE {fk}={tid}'.format(fk=fk, tid=type_ID))
        if self.c.fetchone():
            return True
        else:
            self.c.execute('DELETE FROM {tb} WHERE {id}={tid}'.format(tb=type, id=ID, tid=type_ID))
            self.conn.commit()

    def searchgenre(self, genre):
        """
        check if genre already exists
        """
        self.c.execute("SELECT genre_name FROM genre WHERE genre_name = ?", (genre, ))
        empty = self.c.fetchone()
        if empty:
            return True
        else:
            return False

    def searchAIC(self, type, value):
        '''
        check if AIC already exists
        '''
        name = type + "_name"
        self.c.execute('SELECT {nm} FROM {tb} WHERE {nm}=?'.format(nm=name, tb=type), (value, ))
        exist = self.c.fetchone()
        if exist:
            return True
        else:
            return False

    def update_file(self):
        """
        save changes in file
        """
        song = self.songs[self.Spath].get_all()
        try:
            audio = mutagen.easyid3.EasyID3(self.Spath)
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
        audio["discnumber"] = song["cd"]
        audio["composer"] = song["composer"]
        audio["tracknumber"] = song["track"]
        audio["bpm"] = song["bpm"]
        audio["albumartist"] = song["albuminterpreter"]
        audio["year"] = song["year"]

        audio.save()

    def checkAIC(self, type, song):
        '''
        check for Albuminterpreter, Interpreter, Composer (AIC)
        '''
        ID = type + "_ID"
        name = type + "_name"
        if not self.searchAIC(type, song[type]):
            ex = (None, song[type])
            self.c.execute('INSERT INTO {tb} VALUES(?,?)'.format(tb=type), ex)
        
        self.c.execute('SELECT {id} FROM {tb} WHERE {nm}=?'.format(id=ID, tb=type, nm=name), (unicode(song[type]), ))
        type_ID = self.c.fetchone()
        if type_ID:
            type_ID = type_ID[ID]
        
        return type_ID

    def update_db(self, object, path):
        """
        save changes in db
        """
        song = object[path].get_all()
        interpreter_ID = self.checkAIC('interpreter', song)
        albuminterpreter_ID = self.checkAIC('albuminterpreter', song)
        composer_ID = self.checkAIC('composer', song)

        ex = [song['title'], song['album'], interpreter_ID, albuminterpreter_ID, composer_ID, song['comment'], song['cs'], song['timesplayed'], song['chance'], song['rating'], song['bpm'], song['cd'], song['track'], song['year'], path]
        self.c.execute('''UPDATE music SET title=?, album=?, interpreter_FK=?, albuminterpreter_FK=?, composer_FK=?, comment=?, cs =?, times_played=?, chance=?, rating=?, bpm=?, cd=?, track=?, year=? WHERE path = ?''', ex)
        self.conn.commit()

        if hasattr(self, 'ointerpreter'):
            self.AICIsNeeded('interpreter', self.ointerpreter)

    def update_dball(self, object):
        """
        save all changes in db
        """
        for path in object:
            song = object[path].get_all()
            interpreter_ID = self.checkAIC('interpreter', song)
            albuminterpreter_ID = self.checkAIC('albuminterpreter', song)
            composer_ID = self.checkAIC('composer', song)

            ex = [song['title'], song['album'], interpreter_ID, albuminterpreter_ID, composer_ID, song['comment'], song['cs'], song['timesplayed'], song['chance'], song['rating'], path]
            self.c.execute('''UPDATE music SET title=?, album=?, interpreter_FK=?, albuminterpreter_FK=?, composer_FK=?, comment=?, cs =?, times_played=?, chance=?, rating=? WHERE path = ?''', ex)
        self.conn.commit()

    def get_volume(self):
        try:
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            self.volume = int(config.get('player', 'volume'))
        except ConfigParser.NoSectionError:
            self.volume = 1

    def save_volume(self):
        if hasattr(self, 'volume'):
            config = ConfigParser.ConfigParser()
            config.read('config.ini')
            config.set('player', 'volume', self.volume)
            with open('config.ini',  'wb') as configfile:
                config.write(configfile)

    def get_playlistItemWithPath(self, path):
        """
        get the playlistwidgetitem with path
        """
        for i in range(self.playlistWidget.rowCount()):
            if path == self.playlistWidget.item(i, 0).text():
                return self.playlistWidget.item(i, 0)

    def playerPlayNext(self):
        """
        wait for loading and then start next song
        """
        time.sleep(0.2)
        self.player.next()

    def start_randomplay(self):
        """
        start playing in random mode
        """
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
        self.playPlayer()
        self.get_volume()
        self.player.volume = self.volume
        self.soundSlider.setValue(self.volume)
        self.soundSlider.setSliderPosition(self.volume)

    def increase_chance(self):
        """
        increase the chance in random mode
        """
        for path in self.playlist:
            if path != self.song.get_path():
                self.playlist[path].increasechance(self.count)

    def decrease_chance(self):
        """
        decrease chance in random mode
        """
        self.playlist[self.song.get_path()].decreasechance(self.count)

    def get_randomcount(self):
        """
        get the random count which is needed to calculate the next song
        """
        for path in self.playlist:
            self.randomcount += self.playlist[path].get_chance()

    def timeout(self):
        """
        update the time in the progress bar
        """
        if self.paus < 5:
            self.paus += 1
        if self.player.playing and not self.single:
            self.update_progress()
            self.mdlg.update_progress(self.player.time)
            if int(self.player.time) >= self.maxlength:
                self.playlist[self.Ppath].update_timesplayed()
                self.player.seek(self.START)
                self.on_nextbutton_clicked()

    def playPlayer(self):
        self.trayicon.setIcon(QIcon('resources/trayiconplay.png'))
        self.player.play()

    def pausePlayer(self):
        self.trayicon.setIcon(QIcon('resources/trayiconpause.png'))
        self.player.pause()

    def get_nextRandomSong(self):
        """
        set the next song in random mode
        """
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
        """
        get the next song in random mode after it went back so it will have a structur
        """
        self.song = self.songlist[self.index]
        path = os.path.abspath(self.song.get_path())

        source= pyglet.media.load(path)
        self.player.queue(source)
        self.get_infos()

    def get_last(self):
        """
        get the last song played in random mode
        """
        self.song = self.songlist[self.index]
        path = os.path.abspath(self.song.get_path())

        source= pyglet.resource.media(path)
        self.player.queue(source)

        self.get_infos()

    def get_nextsong(self):
        """
        get next song in normal mode
        """
        self.update_db(self.playlist, self.Ppath)
        self.playlistWidget.setCurrentCell(self.index, 1)
        path = unicode(self.playlistWidget.item(self.index,  0).text())
        path = os.path.abspath(path)
        if os.path.isfile(path):
            self.Ppath = path
            source= pyglet.media.load(path)
            self.player.queue(source)
            self.song = self.playlist[self.Ppath]
            self.get_infos()

    def get_infos(self):
        """
        get song information and set them in the player
        """
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

    def update_progress(self):
        """
        update the progress in time bar and current time
        """
        self.timebar.setValue(int(self.player.time*50))
        m, s = divmod(int(self.player.time), 60)
        self.time.setText("%02d:%02d" % (m, s))

    def releasePlay(self):
        """
        release mouse after changing time in time bar
        """
        if not self.player.playing:
            if self.playing:
                self.playPlayer()
                self.playing = False

    def progressMovement(self, percent):
        """
        change time bar position
        """
        if self.player.playing:
            self.pausePlayer()
            self.playing = True
        if not percent:
            percent = 0.00001
        self.player.seek(percent * self.maxlength)
        self.update_progress()

    def trayactivated(self, type):
        """
        if tray icon is doubleclicked show window or if single clicked show context menu
        """
        if type == 2:
            self.doubleclicktimer.stop()
            self.showNormal()
        elif type == QSystemTrayIcon.Trigger:
            self.doubleclicktimer.start(200)

    def waitForDoubleclick(self):
        """
        wait if user makes a doubleclick
        """
        self.traymenu.popup(QCursor.pos())

    def openWindow(self):
        """
        when open is choosed in tray icon context menu show main window
        """
        self.showNormal()

    def exitWindow(self):
        """
        close application if exit is pressed int context menu of tray icon
        """
        self.pausePlayer()
        QApplication.quit()

    def closeEvent(self, event):
        """
        handle the close event and stop music and save volume
        """
        if self.mdlg.isVisible() or self.musicdock.isVisible():
            self.hide()
        else:
            if hasattr(self, 'player'):
                self.pausePlayer()
                self.save_volume()
                self.update_dball(self.playlist)
            QApplication.quit()
            event.accept()
        event.ignore()

    def playCurrentSong(self):
        """
        play selected song in normal mode
        """
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
            self.playPlayer()
            self.get_volume()
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
            self.playPlayer()

    def create_tree(self):
        """
        create the tree for the playlists
        """
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
        """
        create a new folder for playlists
        """
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
        """
        delete a folder or playlist in playlist tree
        """
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
        """
        get path of selected file or folder
        """
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
        """
        search a playlist or folder
        """
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
        """
        search through all files and return matched
        """
        matchlist = []
        it = QDirIterator(parent.data().toString(), QDirIterator.Subdirectories)
        while it.hasNext():
            tmp = it.next()
            last = tmp.split("/")[-1]
            if name in last or name == tmp:
                matchlist.append(tmp)
        return matchlist

    def loadFileToPlaylist(self, index):
        """
        load a playlist file to active playlist
        """
        if self.playlist and self.playlistLineEdit.text():
            reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.No:
                return
        self.playlistWidget.setRowCount(0)
        self.playlist = {}

        path = self.get_path(index)
        path += unicode(index.data().toString())
        playlistname, songs = self.load_playlist(path)
        paths = []
        self.playlistLineEdit.setText(playlistname['name'])
        for song in songs:
            paths.append(song['path'])
        self.playlistAdd(paths, False)
        self.playlistTab.setCurrentIndex(1)

    def load_playlist(self, path):
        """
        get data from playlist
        """
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
        """
        create a new playlist and save it
        """
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
        """
        send edit table to playlist
        """
        if self.playlist and self.playlistLineEdit.text():
            reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.No:
                return
        self.playlistWidget.setRowCount(0)
        self.playlist = {}
        paths = []
        for path in self.songs:
            paths.append(path)
        self.playlistAdd(paths, False)
        item = self.get_playlistItemWithPath(self.Spath)
        self.playlistWidget.setCurrentItem(item)
        self.playlistWidget.setFocus()
        self.playlistWidget.setCurrentCell(self.playlistWidget.currentRow(), 1)

    def playlistAdd(self, paths, sort):
        """
        add song in playlist
        """
        self.fileAddInDB(paths, True)
        for path in paths:
            exception = False
            existinplaylist = False
            path = unicode(path)
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

                    qpath = QTableWidgetItem(path)
                    qtitle = QTableWidgetItem(song['title'])
                    qlength = QTableWidgetItem(orlength)
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

    def switchPlaylistTab(self):
        """
        change current playlist tab
        """
        self.playlistTab.setCurrentIndex(1)

    def listViewClose(self):
        """
        close popup if user wants to edit search
        """
        self.playlistSearchLineEdit.hidePopup()

    def tableWidgetReturnPressed(self):
        """
        add all edit songs to playlist and play song if enter is pressed in edit table
        """
        self.on_tableWidget_itemDoubleClicked(self.tableWidget.currentItem())

    def playlistTreeContextMenu(self, pos):
        """
        create context menu for playlist tree
        """
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
        add all edit songs to playlist and play song if user double clicks an edit item
        """
        self.tableToPlaylist()
        self.playCurrentSong()

    @pyqtSignature("")
    def on_genreButton_clicked(self):
        """
        change genres for selected song
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
        save changes for song
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
        shuffle playlist
        """
        if hasattr(self, 'playlist'):
            self.playlistWidget.setRowCount(0)
            songs = []
            for song in self.playlist:
                songs.append(song)
            random.shuffle(songs)
            self.playlistAdd(songs, False)
            self.playlistWidget.setFocus()
            self.playlistWidget.setCurrentCell(0, 1)
            self.create_playlist(True)

    @pyqtSignature("")
    def on_playallbutton_clicked(self):
        """
        play playlist
        """
        if hasattr(self, 'playlist'):
            if not self.playlistWidget.selectedIndexes():
                self.playlistWidget.setFocus()
                self.setCurrentCell(0, 1)
            self.playCurrentSong()

    @pyqtSignature("")
    def on_playbutton_clicked(self):
        """
        play playlist in random mode
        """
        self.start_randomplay()

    @pyqtSignature("")
    def on_playbutton_2_clicked(self):
        """
        
        """
        if not self.player.playing:
            self.playPlayer()
            self.playing = True

    @pyqtSignature("")
    def on_playpausebutton_clicked(self):
        """
        play or pause music
        """
        if self.paus >= 5:
            if self.player.playing:
                self.pausePlayer()
                self.playing = False
                self.playpausebutton.setIcon(QIcon('resources/play.png'))
            else:
                self.playPlayer()
                self.playing = True
                self.playpausebutton.setIcon(QIcon('resources/pause.png'))

    @pyqtSignature("")
    def on_previousbutton_clicked(self):
        """
        play last song
        """
        if self.player.time <= 3:
            if self.paus == 5:
                self.paus = 0
                self.single = True
                if self.index > 0:
                    self.index -= 1
                    if self.RANDOMNESS:
                        self.get_last()
                    else:
                        self.get_nextsong()
                    self.playerPlayNext()
                    self.single = False
                elif self.index == 0 and not self.RANDOMNESS:
                    self.index = self.playlistWidget.rowCount()-1
                    self.get_nextsong()
                    self.playerPlayNext()
                    self.single = False
        else:
            self.player.seek(self.START)

    @pyqtSignature("")
    def on_nextbutton_clicked(self):
        """
        play next song
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
        change volume
        """
        self.player.volume = self.soundSlider.value()
        self.volume = self.soundSlider.value()

    @pyqtSignature("QAction*")
    def on_menuBar_triggered(self, action):
        """
        menu bar actions
        """
        if action.text() == "Refresh":
            self.update_dball(self.playlist)
            self.reset_all()
            self.make_Table()

        elif action.text() == "Change Directory":
            self.reset_all()
            self.pausePlayer()
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
        reset song filter
        """
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def eventFilter(self, source, e):
        """
        filter events
        """
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
        save playlist
        """
        self.create_playlist(False)

    @pyqtSignature("QTableWidgetItem*")
    def on_playlistWidget_itemDoubleClicked(self, item):
        """
        play clicked song
        """
        self.playCurrentSong()

    @pyqtSignature("")
    def on_tableWidget_itemSelectionChanged(self):
        """
        change current editable
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
        create playlist in clicked folder or load playlist
        """
        if self.model.isDir(index):
            self.playlistTab.setCurrentIndex(1)
        else:
            self.loadFileToPlaylist(index)

    @pyqtSignature("")
    def on_playlistCreateFolderButton_clicked(self):
        """
        create folder
        """
        self.create_folder()

    @pyqtSignature("")
    def on_playlistSearchButton_clicked(self):
        """
        search playlist or folder
        """
        self.search_playlist()

    @pyqtSignature("")
    def on_playlistFolderLineEdit_returnPressed(self):
        """
        search playlist or folder
        """
        self.create_folder()

    def playlistSearchEnterPressed(self):
        """
        search playlist or folder
        """
        self.search_playlist()

    @pyqtSignature("bool")
    def on_musicdock_topLevelChanged(self, topLevel):
        """
        hide dockwidget and show music player in dialog
        """
        if topLevel:
            self.musicdock.setVisible(False)
            self.mdlg.set_volume(self.volume)
            self.mdlg.showNormal()
            
    def playerClosed(self, int):
        """
        show dockwidget if music player is hidden and close player if music player is closed
        """
        self.musicdock.setVisible(True)
        self.musicdock.setFloating(False)
        if int == 0:
            self.closeMusic()

    def closeMusic(self):
        """
        close music and set it to start position
        """
        if self.player.playing:
            self.pausePlayer()
            self.playing = False
        self.musicframe.setVisible(False)
        self.Ppath = ""
        self.player= pyglet.media.Player()
        self.trayicon.setIcon(QIcon('resources/trayicon.png'))
        self.update_dball(self.playlist)

    def send_songInfos(self, length, timebarrange):
        """
        send songinformations to dialog
        """
        items = self.playlist[self.Ppath].get_all()
        self.mdlg.set_songInfos(items['title'], items['album'], items['interpreter'], items['rating'], length, timebarrange)

    def mpplayclicked(self):
        """
        get clicked signal of dialog
        """
        self.on_playbutton_2_clicked()

    def mppauseclicked(self):
        """
        get clicked signal of dialog
        """
        self.on_pausebutton_clicked()

    def mpnextclicked(self):
        """
        get clicked signal of dialog
        """
        self.on_nextbutton_clicked()

    def mppreviousclicked(self):
        """
        get clicked signal of dialog
        """
        self.on_previousbutton_clicked()

    def mpsoundsliderchanged(self, value):
        """
        get sound changed
        """
        self.on_soundSlider_valueChanged(value)

    def mpratingchanged(self, rating):
        """
        get rating changed
        """
        self.playlist[self.Ppath].set_rating(rating)

    def mptimechanged(self, percent):
        """
        send time changed information
        """
        self.progressMovement(percent)
        self.mdlg.update_progress(int(self.player.time))

    def mprelease(self):
        """
        get signal if mouse is released
        """
        self.releasePlay()
