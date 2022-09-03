# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog

from views.Ui_load import Ui_Load

class Loading(QDialog, Ui_Load):
    """
    little loading screen
    """
    def __init__(self, maximum, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.setMaximum(maximum)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def set_loading(self, progress):
        self.progressBar.setValue(progress)
