# -*- coding: utf-8 -*-

"""
Module implementing Music.
"""
import pyglet
import os.path
import random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_mplay import Ui_music


class Amusic(QWidget, Ui_music):
    """
    Class documentation goes here.
    """
    def __init__(self, songs, playlist, c, conn,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.player= pyglet.media.Player()
        self.songs = songs
        self.playlist = playlist
        self.index = 0
        self.c = c
        self.conn = conn
        
        for song in self.playlist:
            if not song['played']:
                break
            self.index+=1
        
        self.get_song()
        
        self.spinBoxRating.setReadOnly(True)
        self.spinBoxRating.setReadOnly(False)
        
        #Konstante um zum Liedanfang zu kommen.
        self.START = 0.0001
        
        self.progress.releasePlay.connect(self.releasePlay)
        self.progress.progressMovement.connect(self.progressMovement)
        self.playing = False
        
        self.loop = QTimer(parent)
        self.loop.timeout.connect(self.timeout)
        self.loop.start(100)
        
        self.setFixedSize(self.size())
        
        self.titelscroll = QTimer(parent)
        self.titelscroll.timeout.connect(self.titeltimeout)
        self.titelscroll.start(350)
        
        self.albumscroll = QTimer(parent)
        self.albumscroll.timeout.connect(self.albumtimeout)
        self.albumscroll.start(350)
        
        self.interpreterscroll = QTimer(parent)
        self.interpreterscroll.timeout.connect(self.interpretertimeout)
        self.interpreterscroll.start(350)
        
        self.paus = 0
        self.single = False
        
        
    def titeltimeout(self):
        if self.scrolltitel.horizontalScrollBar().value() < self.scrolltitel.horizontalScrollBar().maximum() and self.titeli >= 0:
            self.scrolltitel.horizontalScrollBar().setValue(self.scrolltitel.horizontalScrollBar().value()+10)
        elif self.titeli >= 4:
            self.scrolltitel.horizontalScrollBar().setValue(0)
            self.titeli = -8
        else:
            self.titeli += 1

        
    def albumtimeout(self):
        if self.scrollalbum.horizontalScrollBar().value() < self.scrollalbum.horizontalScrollBar().maximum() and self.albumi >= 0:
            self.scrollalbum.horizontalScrollBar().setValue(self.scrollalbum.horizontalScrollBar().value()+10)
        elif self.albumi >= 4:
            self.scrollalbum.horizontalScrollBar().setValue(0)
            self.albumi = -8
        else:
            self.albumi += 1
        
    def interpretertimeout(self):
        if self.scrollinterpreter.horizontalScrollBar().value() < self.scrollinterpreter.horizontalScrollBar().maximum() and self.interpreteri >= 0:
            self.scrollinterpreter.horizontalScrollBar().setValue(self.scrollinterpreter.horizontalScrollBar().value()+10)
        elif self.interpreteri >= 4:
            self.scrollinterpreter.horizontalScrollBar().setValue(0)
            self.interpreteri = -8
        else:
            self.interpreteri += 1
    
    def get_song(self):
        
        rpath = os.path.relpath(self.playlist[self.index]['path'], os.path.abspath(__file__))[3:]
                
        self.song = self.songs[self.playlist[self.index]['path']]
        
        source= pyglet.resource.media(rpath)
        self.player.queue(source)
        
        self.get_infos()
        
    def get_infos(self):
        info = self.song.get_all()
        self.maxlength = info['length']
        self.progress.setRange(0, self.maxlength*50)
        m, s = divmod(self.maxlength, 60)
        
        self.spinBoxRating.setValue(int(info['rating']))
        self.titel.setText(info['title'])
        self.album.setText(info['album'])
        self.interpreter.setText(info['interpreter'])
        self.length.setText("/ %02d:%02d" % (m, s))
        self.titeli = -12
        self.albumi = -12
        self.interpreteri = -12
        
        self.update_playlist()
    
    def update_progress(self):
        self.progress.setValue(int(self.player.time*50))
        m, s = divmod(int(self.player.time), 60)
        self.time.setText("%02d:%02d" % (m, s))
    
    def releasePlay(self):
        if not self.player.playing:
            if self.playing:
                self.player.play()
        
    def progressMovement(self, percent):
        if self.player.playing:
            self.player.pause()
        if not percent:
            percent = self.START
        self.player.seek(percent * self.maxlength)
        self.update_progress()
        
    
    def timeout(self):
        if self.paus < 5:
            self.paus += 1
        if self.player.playing:
            self.update_progress()
            if int(self.player.time) == self.maxlength and not self.single:
                self.song.update_timesplayed()
                self.playlist[self.index]['played']  = True
                self.index += 1
                self.get_song()
    
    def closeEvent(self, event):
        self.player.pause()
        event.accept()
        
    def update_playlist(self):
        for song in self.playlist:
            ex = (song['played'], song['path'])
            self.c.execute('UPDATE playlist SET played=? WHERE path=?', ex)
        self.conn.commit()
        
    def reload_playlist(self):
        
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
        self.index = 0
        self.get_song()
    
    @pyqtSignature("")
    def on_playbutton_clicked(self):
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
                self.playlist[self.index]['played']  = False
                self.get_song()
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
            if self.index == len(self.playlist) -1:
                self.reload_playlist()
            else:
                self.playlist[self.index]['played'] = True
                self.index += 1
                self.get_song()
            self.player.next()
            self.single = False
    
    @pyqtSignature("int")
    def on_spinBoxRating_valueChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.song.set_rating(p0)
    
    @pyqtSignature("int")
    def on_soundSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        """
        self.player.volume = self.soundSlider.value()
