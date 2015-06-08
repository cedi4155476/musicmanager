# -*- coding: utf-8 -*-

"""
Module implementing Smusic.
"""
import pyglet

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_mplay import Ui_music


class Smusic(QDialog, Ui_music):
    """
    Class documentation goes here.
    """
    def __init__(self, path, song, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.player= pyglet.media.Player()
        source= pyglet.resource.media(path)
        self.player.queue(source)
        self.song = song
        info = self.song.get_all()
        self.maxlength = info['length']
        self.progress.setRange(0, self.maxlength*50)
        m, s = divmod(self.maxlength, 60)
        
        self.spinBoxRating.setValue(int(info['rating']))
        self.titel.setText(info['title'])
        self.album.setText(info['album'])
        self.interpreter.setText(info['interpreter'])
        self.length.setText("/ %02d:%02d" % (m, s))
        self.previousbutton.hide()
        self.nextbutton.hide()
        self.spinBoxRating.setReadOnly(True)
        self.spinBoxRating.setReadOnly(False)
        self.progress.releasePlay.connect(self.releasePlay)
        self.progress.progressMovement.connect(self.progressMovement)
        self.playing = False
        
        self.titelwidth = self.titel.sizeHint().width() - self.scrolltitel.sizeHint().width()
        self.interpreterwidth = self.interpreter.sizeHint().width() - self.scrollinterpreter.sizeHint().width()
        self.albumwidth = self.album.sizeHint().width() - self.scrollalbum.sizeHint().width()
        
        self.setFixedSize(self.size())
        self.titeli = -12
        if self.titelwidth > 0:
            self.titel.setAlignment(Qt.AlignLeft)
            self.titelscroll = QTimer(parent)
            self.titelscroll.timeout.connect(self.titeltimeout)
            self.titelscroll.start(350)
            
        self.albumi = -12
        if self.albumwidth > 0:
            self.album.setAlignment(Qt.AlignLeft)
            self.albumscroll = QTimer(parent)
            self.albumscroll.timeout.connect(self.albumtimeout)
            self.albumscroll.start(350)
            
        self.interpreteri = -12
        if self.interpreterwidth > 0:
            self.interpreter.setAlignment(Qt.AlignLeft)
            self.interpreterscroll = QTimer(parent)
            self.interpreterscroll.timeout.connect(self.interpretertimeout)
            self.interpreterscroll.start(350)
        
        
        
        self.loop = QTimer(parent)
        self.loop.timeout.connect(self.timeout)
        self.loop.start(100)
        
        
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
        
    def update_progress(self):
        self.progress.setValue(int(self.player.time*50))
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
        
    
    def timeout(self):
        if self.player.playing:
            self.update_progress()
            if int(self.player.time) == self.maxlength:
                song.update_timesplayed()
                self.player.seek(0.000001)
    
    def reject(self):
        self.player.pause()
        QDialog.reject(self)
    
    @pyqtSignature("")
    def on_playbutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.player.playing:
            self.player.play()
    
    @pyqtSignature("")
    def on_pausebutton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.player.playing:
            self.player.pause()
            
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
