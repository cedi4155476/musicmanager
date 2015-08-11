# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music_manager/music_manager/load.ui'
#
# Created: Tue Aug 11 11:27:31 2015
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

class Ui_Load(object):
    def setupUi(self, Load):
        Load.setObjectName(_fromUtf8("Load"))
        Load.resize(400, 130)
        self.verticalLayout = QtGui.QVBoxLayout(Load)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.progressBar = QtGui.QProgressBar(Load)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Load)
        QtCore.QMetaObject.connectSlotsByName(Load)

    def retranslateUi(self, Load):
        Load.setWindowTitle(_translate("Load", "Load Songs", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Load = QtGui.QDialog()
    ui = Ui_Load()
    ui.setupUi(Load)
    Load.show()
    sys.exit(app.exec_())

