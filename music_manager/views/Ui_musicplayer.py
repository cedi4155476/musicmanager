# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music_manager/music_manager/musicplayer.ui'
#
# Created: Tue Aug 18 16:45:29 2015
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_music(object):
    def setupUi(self, music):
        music.setObjectName(_fromUtf8("music"))
        music.setWindowModality(QtCore.Qt.NonModal)
        music.resize(653, 164)
        music.setLayoutDirection(QtCore.Qt.LeftToRight)
        music.setSizeGripEnabled(False)
        music.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(music)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)
        self.label_3 = QtWidgets.QLabel(music)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_7.addWidget(self.label_3)
        self.soundSlider = QtWidgets.QSlider(music)
        self.soundSlider.setMaximum(10)
        self.soundSlider.setProperty("value", 1)
        self.soundSlider.setOrientation(QtCore.Qt.Horizontal)
        self.soundSlider.setTickInterval(0)
        self.soundSlider.setObjectName(_fromUtf8("soundSlider"))
        self.verticalLayout_7.addWidget(self.soundSlider)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.scrolltitle = QtWidgets.QScrollArea(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrolltitle.sizePolicy().hasHeightForWidth())
        self.scrolltitle.setSizePolicy(sizePolicy)
        self.scrolltitle.setMaximumSize(QtCore.QSize(16777215, 20))
        self.scrolltitle.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scrolltitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrolltitle.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrolltitle.setLineWidth(0)
        self.scrolltitle.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrolltitle.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrolltitle.setWidgetResizable(True)
        self.scrolltitle.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrolltitle.setObjectName(_fromUtf8("scrolltitle"))
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 479, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_4.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_4.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_4.setObjectName(_fromUtf8("scrollAreaWidgetContents_4"))
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.title = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.title.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout_9.addWidget(self.title)
        self.scrolltitle.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout_8.addWidget(self.scrolltitle)
        self.scrollartist = QtWidgets.QScrollArea(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollartist.sizePolicy().hasHeightForWidth())
        self.scrollartist.setSizePolicy(sizePolicy)
        self.scrollartist.setMaximumSize(QtCore.QSize(16777215, 20))
        self.scrollartist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollartist.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollartist.setLineWidth(0)
        self.scrollartist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollartist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollartist.setWidgetResizable(True)
        self.scrollartist.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollartist.setObjectName(_fromUtf8("scrollartist"))
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 479, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_5.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_5.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_5.setObjectName(_fromUtf8("scrollAreaWidgetContents_5"))
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.artist = QtWidgets.QLabel(self.scrollAreaWidgetContents_5)
        self.artist.setAlignment(QtCore.Qt.AlignCenter)
        self.artist.setObjectName(_fromUtf8("artist"))
        self.verticalLayout_10.addWidget(self.artist)
        self.scrollartist.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_8.addWidget(self.scrollartist)
        self.scrollalbum = QtWidgets.QScrollArea(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollalbum.sizePolicy().hasHeightForWidth())
        self.scrollalbum.setSizePolicy(sizePolicy)
        self.scrollalbum.setMaximumSize(QtCore.QSize(16777215, 20))
        self.scrollalbum.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollalbum.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollalbum.setLineWidth(0)
        self.scrollalbum.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollalbum.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollalbum.setWidgetResizable(True)
        self.scrollalbum.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollalbum.setObjectName(_fromUtf8("scrollalbum"))
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 479, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_6.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_6.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_6.setObjectName(_fromUtf8("scrollAreaWidgetContents_6"))
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.album = QtWidgets.QLabel(self.scrollAreaWidgetContents_6)
        self.album.setAlignment(QtCore.Qt.AlignCenter)
        self.album.setObjectName(_fromUtf8("album"))
        self.verticalLayout_11.addWidget(self.album)
        self.scrollalbum.setWidget(self.scrollAreaWidgetContents_6)
        self.verticalLayout_8.addWidget(self.scrollalbum)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName(_fromUtf8("verticalLayout_12"))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.dockbutton = QtWidgets.QToolButton(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockbutton.sizePolicy().hasHeightForWidth())
        self.dockbutton.setSizePolicy(sizePolicy)
        self.dockbutton.setMinimumSize(QtCore.QSize(0, 0))
        self.dockbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dockbutton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dockbutton.setText(_fromUtf8(""))
        self.dockbutton.setAutoRepeat(False)
        self.dockbutton.setAutoRaise(False)
        self.dockbutton.setArrowType(QtCore.Qt.UpArrow)
        self.dockbutton.setObjectName(_fromUtf8("dockbutton"))
        self.horizontalLayout_4.addWidget(self.dockbutton)
        self.verticalLayout_12.addLayout(self.horizontalLayout_4)
        self.label_4 = QtWidgets.QLabel(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_12.addWidget(self.label_4)
        self.spinBoxRating = QtWidgets.QSpinBox(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRating.sizePolicy().hasHeightForWidth())
        self.spinBoxRating.setSizePolicy(sizePolicy)
        self.spinBoxRating.setMinimumSize(QtCore.QSize(0, 0))
        self.spinBoxRating.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spinBoxRating.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spinBoxRating.setWrapping(False)
        self.spinBoxRating.setFrame(True)
        self.spinBoxRating.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxRating.setKeyboardTracking(False)
        self.spinBoxRating.setMinimum(1)
        self.spinBoxRating.setMaximum(20)
        self.spinBoxRating.setObjectName(_fromUtf8("spinBoxRating"))
        self.verticalLayout_12.addWidget(self.spinBoxRating)
        self.horizontalLayout_3.addLayout(self.verticalLayout_12)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.timelayout = QtWidgets.QHBoxLayout()
        self.timelayout.setObjectName(_fromUtf8("timelayout"))
        self.progress = MyProgressbar(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progress.sizePolicy().hasHeightForWidth())
        self.progress.setSizePolicy(sizePolicy)
        self.progress.setMinimumSize(QtCore.QSize(0, 0))
        self.progress.setMaximumSize(QtCore.QSize(16777215, 10))
        self.progress.setMouseTracking(False)
        self.progress.setProperty("value", 0)
        self.progress.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progress.setTextVisible(False)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.timelayout.addWidget(self.progress)
        self.time = QtWidgets.QLabel(music)
        self.time.setObjectName(_fromUtf8("time"))
        self.timelayout.addWidget(self.time)
        self.length = QtWidgets.QLabel(music)
        self.length.setObjectName(_fromUtf8("length"))
        self.timelayout.addWidget(self.length)
        self.verticalLayout.addLayout(self.timelayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.previousbutton = QtWidgets.QPushButton(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previousbutton.sizePolicy().hasHeightForWidth())
        self.previousbutton.setSizePolicy(sizePolicy)
        self.previousbutton.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/music_layout/resources/previous.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.previousbutton.setIcon(icon)
        self.previousbutton.setIconSize(QtCore.QSize(30, 30))
        self.previousbutton.setAutoDefault(False)
        self.previousbutton.setDefault(False)
        self.previousbutton.setFlat(True)
        self.previousbutton.setObjectName(_fromUtf8("previousbutton"))
        self.horizontalLayout.addWidget(self.previousbutton)
        self.playbutton = QtWidgets.QPushButton(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playbutton.sizePolicy().hasHeightForWidth())
        self.playbutton.setSizePolicy(sizePolicy)
        self.playbutton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/music_layout/resources/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playbutton.setIcon(icon1)
        self.playbutton.setIconSize(QtCore.QSize(30, 30))
        self.playbutton.setAutoDefault(False)
        self.playbutton.setFlat(True)
        self.playbutton.setObjectName(_fromUtf8("playbutton"))
        self.horizontalLayout.addWidget(self.playbutton)
        self.pausebutton = QtWidgets.QPushButton(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pausebutton.sizePolicy().hasHeightForWidth())
        self.pausebutton.setSizePolicy(sizePolicy)
        self.pausebutton.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/music_layout/resources/pause.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pausebutton.setIcon(icon2)
        self.pausebutton.setIconSize(QtCore.QSize(30, 30))
        self.pausebutton.setAutoDefault(False)
        self.pausebutton.setFlat(True)
        self.pausebutton.setObjectName(_fromUtf8("pausebutton"))
        self.horizontalLayout.addWidget(self.pausebutton)
        self.nextbutton = QtWidgets.QPushButton(music)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextbutton.sizePolicy().hasHeightForWidth())
        self.nextbutton.setSizePolicy(sizePolicy)
        self.nextbutton.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/music_layout/resources/next.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nextbutton.setIcon(icon3)
        self.nextbutton.setIconSize(QtCore.QSize(30, 30))
        self.nextbutton.setAutoDefault(False)
        self.nextbutton.setFlat(True)
        self.nextbutton.setObjectName(_fromUtf8("nextbutton"))
        self.horizontalLayout.addWidget(self.nextbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(music)
        QtCore.QMetaObject.connectSlotsByName(music)

    def retranslateUi(self, music):
        music.setWindowTitle(_translate("music", "Music Player", None))
        self.label_3.setText(_translate("music", "Volume", None))
        self.title.setText(_translate("music", "TextLabel", None))
        self.artist.setText(_translate("music", "TextLabel", None))
        self.album.setText(_translate("music", "TextLabel", None))
        self.label_4.setText(_translate("music", "Rating", None))
        self.progress.setFormat(_translate("music", "%p", None))
        self.time.setText(_translate("music", "00:00", None))
        self.length.setText(_translate("music", "11:11", None))

from views.myProgressbar import MyProgressbar
import views.resource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    music = QtGui.QDialog()
    ui = Ui_music()
    ui.setupUi(music)
    music.show()
    sys.exit(app.exec_())

