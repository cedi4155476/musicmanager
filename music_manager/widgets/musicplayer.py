import pyglet

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from views.Ui_musicplayer import Ui_music

class MusicPlayer(QDialog, Ui_music):
    """
    music player dialog for listening to the songs
    """
    playclicked = pyqtSignal()
    pauseclicked = pyqtSignal()
    nextclicked = pyqtSignal()
    previousclicked = pyqtSignal()
    soundsliderchanged = pyqtSignal(int)
    ratingchanged = pyqtSignal(int)
    timechanged = pyqtSignal(float)
    release = pyqtSignal()
    playerhidden = pyqtSignal(int)

    def __init__(self, wh, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.titeli = -12
        self.albumi = -12
        self.interpreteri = -12

        self.spinBoxRating.setReadOnly(True)
        self.spinBoxRating.setReadOnly(False)

        self.setFixedSize(self.size())

        self.progress.releasePlay.connect(self.releasePlay)
        self.progress.progressMovement.connect(self.progressMovement)

        self.titelscroll = QTimer(parent)
        self.titelscroll.timeout.connect(self.titeltimeout)
        self.titelscroll.start(350)

        self.albumscroll = QTimer(parent)
        self.albumscroll.timeout.connect(self.albumtimeout)
        self.albumscroll.start(350)

        self.interpreterscroll = QTimer(parent)
        self.interpreterscroll.timeout.connect(self.interpretertimeout)
        self.interpreterscroll.start(350)
        self.wh = wh
        self.player= pyglet.media.Player()
        self.musicplayersetslots()

    def titeltimeout(self):
        """
        scrolling for long titles
        """
        if self.scrolltitel.horizontalScrollBar().value() < self.scrolltitel.horizontalScrollBar().maximum() and self.titeli >= 0:
            self.scrolltitel.horizontalScrollBar().setValue(self.scrolltitel.horizontalScrollBar().value()+10)
        elif self.titeli >= 4:
            self.scrolltitel.horizontalScrollBar().setValue(0)
            self.titeli = -8
        else:
            self.titeli += 1

    def albumtimeout(self):
        """
        scrolling for long albums
        """
        if self.scrollalbum.horizontalScrollBar().value() < self.scrollalbum.horizontalScrollBar().maximum() and self.albumi >= 0:
            self.scrollalbum.horizontalScrollBar().setValue(self.scrollalbum.horizontalScrollBar().value()+10)
        elif self.albumi >= 4:
            self.scrollalbum.horizontalScrollBar().setValue(0)
            self.albumi = -8
        else:
            self.albumi += 1

    def interpretertimeout(self):
        """
        scrolling for long interpreters
        """
        if self.scrollinterpreter.horizontalScrollBar().value() < self.scrollinterpreter.horizontalScrollBar().maximum() and self.interpreteri >= 0:
            self.scrollinterpreter.horizontalScrollBar().setValue(self.scrollinterpreter.horizontalScrollBar().value()+10)
        elif self.interpreteri >= 4:
            self.scrollinterpreter.horizontalScrollBar().setValue(0)
            self.interpreteri = -8
        else:
            self.interpreteri += 1

    def set_songInfos(self, title, album, interpreter, rating, length, range):
        """
        set song infos
        """
        self.titel.setText(title)
        self.album.setText(album)
        self.interpreter.setText(interpreter)
        self.spinBoxRating.setValue(rating)
        self.progress.setRange(0, range)
        self.length.setText(length)

    def set_volume(self, volume):
        """
        change volume
        """
        self.soundSlider.setValue(volume)

    def update_progress(self, time):
        """
        set progress
        """
        self.progress.setValue(time*50)
        m, s = divmod(time, 60)
        self.time.setText("%02d:%02d" % (m, s))

    def releasePlay(self):
        """
        give signal if mouse is released
        """
        self.release.emit()

    def progressMovement(self, percent):
        """
        send signal if time is changed
        """
        self.timechanged.emit(percent)

    def closeEvent(self, e):
        """
        close window
        """
        e.ignore()
        self.hide()
        self.playerhidden.emit(0)

    @pyqtSlot()
    def on_dockbutton_clicked(self):
        """
        hide window and show dockwidget as music player
        """
        self.hide()
        self.playerhidden.emit(1)

    @pyqtSlot()
    def on_playbutton_clicked(self):
        """
        send click signal
        """
        self.playclicked.emit()

    @pyqtSlot()
    def on_pausebutton_clicked(self):
        """
        send click signal
        """
        self.pauseclicked.emit()

    @pyqtSlot()
    def on_previousbutton_clicked(self):
        """
        send click signal
        """
        self.previousclicked.emit()

    @pyqtSlot()
    def on_nextbutton_clicked(self):
        """
        send click signal
        """
        self.nextclicked.emit()

    @pyqtSlot("int")
    def on_spinBoxRating_valueChanged(self, p0):
        """
        send signal when rating is changed
        """
        self.ratingchanged.emit(p0)

    @pyqtSlot("int")
    def on_soundSlider_valueChanged(self, value):
        """
        send signal when volume is changed
        """
        self.soundsliderchanged.emit(value)

    def musicplayersetslots(self):
        """
        connect the slots with the musicplayer class
        """
        self.wh.GUI.timebar.releasePlay.connect(self.releasePlay)
        self.wh.GUI.timebar.progressMovement.connect(self.progressMovement)
        self.playclicked.connect(self.mpplayclicked)
        self.pauseclicked.connect(self.mppauseclicked)
        self.nextclicked.connect(self.mpnextclicked)
        self.previousclicked.connect(self.mppreviousclicked)
        self.soundsliderchanged.connect(self.mpsoundsliderchanged)
        self.ratingchanged.connect(self.mpratingchanged)
        self.timechanged.connect(self.mptimechanged)
        self.release.connect(self.mprelease)
        self.playerhidden.connect(self.playerClosed)

    def playerClosed(self, int):
        """
        show dockwidget if music player is hidden and close player if music player is closed
        """
        self.musicdock.setVisible(True)
        self.musicdock.setFloating(False)
        if int == 0:
            self.closeMusic()

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

    def releasePlay(self):
        """
        release mouse after changing time in time bar
        """
        if not self.player.playing:
            if self.playing:
                self.playPlayer()
                self.playing = True

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
