# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music_manager/music_manager/genre.ui'
#
# Created: Tue Aug 11 11:27:33 2015
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

class Ui_genre(object):
    def setupUi(self, genre):
        genre.setObjectName(_fromUtf8("genre"))
        genre.setWindowModality(QtCore.Qt.ApplicationModal)
        genre.resize(265, 121)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(genre.sizePolicy().hasHeightForWidth())
        genre.setSizePolicy(sizePolicy)
        genre.setMinimumSize(QtCore.QSize(265, 121))
        genre.setMaximumSize(QtCore.QSize(265, 121))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(genre)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboboxdel = QtWidgets.QComboBox(genre)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboboxdel.sizePolicy().hasHeightForWidth())
        self.comboboxdel.setSizePolicy(sizePolicy)
        self.comboboxdel.setObjectName(_fromUtf8("comboboxdel"))
        self.gridLayout_2.addWidget(self.comboboxdel, 0, 0, 1, 1)
        self.buttondel = QtWidgets.QPushButton(genre)
        self.buttondel.setAutoDefault(False)
        self.buttondel.setObjectName(_fromUtf8("buttondel"))
        self.gridLayout_2.addWidget(self.buttondel, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboboxadd = QtWidgets.QComboBox(genre)
        self.comboboxadd.setEditable(True)
        self.comboboxadd.setObjectName(_fromUtf8("comboboxadd"))
        self.gridLayout.addWidget(self.comboboxadd, 0, 0, 1, 1)
        self.buttonadd = QtWidgets.QPushButton(genre)
        self.buttonadd.setObjectName(_fromUtf8("buttonadd"))
        self.gridLayout.addWidget(self.buttonadd, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonfinish = QtWidgets.QPushButton(genre)
        self.buttonfinish.setAutoDefault(False)
        self.buttonfinish.setObjectName(_fromUtf8("buttonfinish"))
        self.verticalLayout.addWidget(self.buttonfinish)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(genre)
        QtCore.QMetaObject.connectSlotsByName(genre)

    def retranslateUi(self, genre):
        genre.setWindowTitle(_translate("genre", "Genres manager", None))
        self.buttondel.setText(_translate("genre", "Delete", None))
        self.buttonadd.setText(_translate("genre", "Add", None))
        self.buttonfinish.setText(_translate("genre", "finish", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    genre = QtGui.QDialog()
    ui = Ui_genre()
    ui.setupUi(genre)
    genre.show()
    sys.exit(app.exec_())

