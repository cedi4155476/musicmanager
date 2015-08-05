# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music manager/info.ui'
#
# Created: Mon Jul  6 15:10:44 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Info(object):
    def setupUi(self, Info):
        Info.setObjectName(_fromUtf8("Info"))
        Info.setWindowModality(QtCore.Qt.ApplicationModal)
        Info.resize(400, 200)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Info.sizePolicy().hasHeightForWidth())
        Info.setSizePolicy(sizePolicy)
        Info.setMinimumSize(QtCore.QSize(400, 200))
        Info.setMaximumSize(QtCore.QSize(600, 400))
        Info.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.verticalLayout = QtGui.QVBoxLayout(Info)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Info)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Info)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(Info)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(Info)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.buttonBox = QtGui.QDialogButtonBox(Info)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Info)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Info.reject)
        QtCore.QMetaObject.connectSlotsByName(Info)

    def retranslateUi(self, Info):
        Info.setWindowTitle(_translate("Info", "Info", None))
        self.label.setText(_translate("Info", "Music Manager", None))
        self.label_2.setText(_translate("Info", "Author: Cédric Christen", None))
        self.label_3.setText(_translate("Info", "Version: 0.1a1", None))
        self.label_4.setText(_translate("Info", "Manage your music files with Music Manager and also use the music player to hear your songs from playlists with different types of randomness.", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Info = QtGui.QDialog()
    ui = Ui_Info()
    ui.setupUi(Info)
    Info.show()
    sys.exit(app.exec_())

