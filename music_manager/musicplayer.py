from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_musicplayer import Ui_music

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

    def __init__(self, parent=None):
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

    @pyqtSignature("")
    def on_dockbutton_clicked(self):
        """
        hide window and show dockwidget as music player
        """
        self.hide()
        self.playerhidden.emit(1)

    @pyqtSignature("")
    def on_playbutton_clicked(self):
        """
        send click signal
        """
        self.playclicked.emit()

    @pyqtSignature("")
    def on_pausebutton_clicked(self):
        """
        send click signal
        """
        self.pauseclicked.emit()

    @pyqtSignature("")
    def on_previousbutton_clicked(self):
        """
        send click signal
        """
        self.previousclicked.emit()

    @pyqtSignature("")
    def on_nextbutton_clicked(self):
        """
        send click signal
        """
        self.nextclicked.emit()

    @pyqtSignature("int")
    def on_spinBoxRating_valueChanged(self, p0):
        """
        send signal when rating is changed
        """
        self.ratingchanged.emit(p0)

    @pyqtSignature("int")
    def on_soundSlider_valueChanged(self, value):
        """
        send signal when volume is changed
        """
        self.soundsliderchanged.emit(value)
