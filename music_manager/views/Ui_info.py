# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music_manager/music_manager/info.ui'
#
# Created: Tue Aug 11 11:27:30 2015
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

class Ui_Info(object):
    trigger = QtCore.pyqtSignal()

    def setupUi(self, Info):
        Info.setObjectName(_fromUtf8("Info"))
        Info.setWindowModality(QtCore.Qt.ApplicationModal)
        Info.resize(400, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Info.sizePolicy().hasHeightForWidth())
        Info.setSizePolicy(sizePolicy)
        Info.setMinimumSize(QtCore.QSize(400, 200))
        Info.setMaximumSize(QtCore.QSize(600, 400))
        Info.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.verticalLayout = QtWidgets.QVBoxLayout(Info)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtWidgets.QLabel(Info)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(Info)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Info)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(Info)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.buttonBox = QtWidgets.QDialogButtonBox(Info)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Info)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(Info.reject)
        # self.trigger.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Info.reject)
        QtCore.QMetaObject.connectSlotsByName(Info)

    def retranslateUi(self, Info):
        Info.setWindowTitle(_translate("Info", "Info", None))
        self.label.setText(_translate("Info", "Music Manager", None))
        self.label_2.setText(_translate("Info", "Author: cedi4155476", None))
        self.label_3.setText(_translate("Info", "Version: 1.2", None))
        self.label_4.setText(_translate("Info", "Manage your music files with the Music Manager and also use the music player to enjoy your songs from a playlist with different types of randomness.", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Info = QtGui.QDialog()
    ui = Ui_Info()
    ui.setupUi(Info)
    Info.show()
    sys.exit(app.exec_())

