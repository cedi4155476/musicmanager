# -*- coding: utf-8 -*-

"""
Module implementing SearchDialog.
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_search import Ui_Dialog

class SearchDialog(QDialog, Ui_Dialog):
    """
    search directory to edit songs
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUi(self)
        self.currentDir = None
        self.files = []
        self.PATH = None

    def get_path(self):
        return self.PATH

    def get_currentdir(self):
        return self.currentDir

    def get_files(self):
        return self.files

    @pyqtSignature("")
    def on_buttonBox_accepted(self):
        """
        send directory informations
        """
        self.PATH = str(self.lineEditPath.text())
        self.currentDir = QDir(self.PATH)

        self.files = self.currentDir.entryList(QStringList("*"), QDir.Files | QDir.NoSymLinks)
        self.accept()

    @pyqtSignature("")
    def on_directoryPath_clicked(self):
        """
        search for a directory
        """
        self.lineEditPath.setText(QFileDialog.getExistingDirectory())

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        self.reject()
