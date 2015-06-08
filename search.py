# -*- coding: utf-8 -*-

"""
Module implementing SearchDialog.
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_search import Ui_Dialog

class SearchDialog(QDialog, Ui_Dialog):
    """
    Dient zur einfach suche des Ordners in welchem die Lieder sich befinden.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUi(self)
        # WEGEN TESTZWECKEN DAMIT ES EINFACHER IST
        self.lineEditPath.setText('/home/cch/Documents/python/music manager/files')
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
        Slot documentation goes here.
        """
        self.PATH = str(self.lineEditPath.text())
        self.currentDir = QDir(self.PATH)
  
        self.files = self.currentDir.entryList(QStringList("*"), QDir.Files | QDir.NoSymLinks)
        self.accept()
    
    @pyqtSignature("")
    def on_directoryPath_clicked(self):
        """
        Slot documentation goes here.
        """
        self.lineEditPath.setText(QFileDialog.getExistingDirectory())

    @pyqtSignature("")
    def on_buttonBox_rejected(self):
        self.reject()
