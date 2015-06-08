# -*- coding: utf-8 -*-

"""
Module implementing Music.
"""
import pyglet
import os.path
from random import randrange

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_mplay import Ui_music


class Music(QWidget, Ui_music):
    """
    Class documentation goes here.
    """
    def __init__(self, songs, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags((self.windowFlags() & ~Qt.WindowContextHelpButtonHint) | Qt.WindowMaximizeButtonHint)
        self.player= pyglet.media.Player()
        self.songs = songs
        self.count = float(len(self.songs))
        self.songlist = []
        self.randomcount = 0
        self.index = 0
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
        
    def increase_chance(self):
        for path in self.songs:
            if path != self.song.get_path():
                self.songs[path].increasechance(self.count)
        
    def decrease_chance(self):
        self.songs[self.song.get_path()].decreasechance(self.count)
        
    def get_randomcount(self):
        for path in self.songs:
            self.randomcount += self.songs[path].get_chance()
    
    def get_song(self):
        
        self.get_randomcount()
        randomnumber = randrange(self.randomcount)
        chance = 0
        for path in self.songs:
            chance += self.songs[path].get_chance()
            if chance >= randomnumber:
                songpath = path
                rpath = os.path.relpath(path, os.path.abspath(__file__))[3:]
                break
                
        self.randomcount = 0
        self.song = self.songs[songpath]
        self.songlist.append(self.song)
        self.index = len(self.songlist) - 1
        
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
                self.get_song()
    
    def closeEvent(self, event):
        self.player.pause()
        event.accept()
        
    def get_next(self):
        self.index += 1
        self.song = self.songlist[self.index]
        rpath = os.path.relpath(self.song.get_path(), os.path.abspath(__file__))[3:]
        
        source= pyglet.resource.media(rpath)
        self.player.queue(source)
        self.get_infos()
        
    def get_last(self):
        self.index -= 1
        self.song = self.songlist[self.index]
        rpath = os.path.relpath(self.song.get_path(), os.path.abspath(__file__))[3:]
        
        source= pyglet.resource.media(rpath)
        self.player.queue(source)
        
        self.get_infos()
        
    
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
                self.get_last()
                self.player.next()
        else:
            self.player.seek(self.START)
    
    @pyqtSignature("")
    def on_nextbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.paus == 5:
            self.paus = 0
        
            if self.index == len(self.songlist) - 1:
                self.single = True
                self.increase_chance()
                self.decrease_chance()
                self.get_song()
            else:
                self.get_next()
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
