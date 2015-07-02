# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music manager/genre.ui'
#
# Created: Wed Jul  1 11:27:57 2015
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

class Ui_genre(object):
    def setupUi(self, genre):
        genre.setObjectName(_fromUtf8("genre"))
        genre.setWindowModality(QtCore.Qt.ApplicationModal)
        genre.resize(265, 121)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(genre.sizePolicy().hasHeightForWidth())
        genre.setSizePolicy(sizePolicy)
        genre.setMinimumSize(QtCore.QSize(265, 121))
        genre.setMaximumSize(QtCore.QSize(265, 121))
        self.verticalLayout_2 = QtGui.QVBoxLayout(genre)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.comboboxdel = QtGui.QComboBox(genre)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboboxdel.sizePolicy().hasHeightForWidth())
        self.comboboxdel.setSizePolicy(sizePolicy)
        self.comboboxdel.setObjectName(_fromUtf8("comboboxdel"))
        self.gridLayout_2.addWidget(self.comboboxdel, 0, 0, 1, 1)
        self.buttondel = QtGui.QPushButton(genre)
        self.buttondel.setAutoDefault(False)
        self.buttondel.setObjectName(_fromUtf8("buttondel"))
        self.gridLayout_2.addWidget(self.buttondel, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboboxadd = QtGui.QComboBox(genre)
        self.comboboxadd.setEditable(True)
        self.comboboxadd.setObjectName(_fromUtf8("comboboxadd"))
        self.gridLayout.addWidget(self.comboboxadd, 0, 0, 1, 1)
        self.buttonadd = QtGui.QPushButton(genre)
        self.buttonadd.setObjectName(_fromUtf8("buttonadd"))
        self.gridLayout.addWidget(self.buttonadd, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonfinish = QtGui.QPushButton(genre)
        self.buttonfinish.setAutoDefault(False)
        self.buttonfinish.setObjectName(_fromUtf8("buttonfinish"))
        self.verticalLayout.addWidget(self.buttonfinish)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(genre)
        QtCore.QMetaObject.connectSlotsByName(genre)

    def retranslateUi(self, genre):
        genre.setWindowTitle(_translate("genre", "Genres einfügen", None))
        self.buttondel.setText(_translate("genre", "Löschen", None))
        self.buttonadd.setText(_translate("genre", "Hinzufügen", None))
        self.buttonfinish.setText(_translate("genre", "fertig", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    genre = QtGui.QDialog()
    ui = Ui_genre()
    ui.setupUi(genre)
    genre.show()
    sys.exit(app.exec_())

