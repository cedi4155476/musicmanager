# -*- coding: utf-8 -*-

"""
Module implementing SearchDialog.
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pathlib import Path
from os.path import expanduser

from views.Ui_search import Ui_Dialog

class SearchDialog(QDialog, Ui_Dialog):
    """
    search directory to edit songs
    """
    def __init__(self, config, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUi(self)
        self.files = []
        self.path = None
        self.config = config
        self.lineEditPath.setText(self.config.get_directory_path())

    def get_path(self):
        return self.path

    def get_files(self):
        self.files = list(x for x in self.path.iterdir() if x.is_file())
        return self.files

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        send directory informations
        """
        self.path = Path(self.lineEditPath.text())
        self.files = list(x for x in self.path.iterdir() if x.is_file())
        self.config.save_directory_path(str(self.path.resolve()))
        self.accept()

    @pyqtSlot()
    def on_directoryPath_clicked(self):
        """
        search for a directory
        """
        if self.lineEditPath.text():
            start = self.lineEditPath.text()
        else:
            start = expanduser("~")
        self.lineEditPath.setText(QFileDialog.getExistingDirectory(self, "Choose directory", start))

    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.reject()
