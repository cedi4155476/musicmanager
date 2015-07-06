# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_load import Ui_Load

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

    def set_loading(self, progress):
        self.progressBar.setValue(progress)
