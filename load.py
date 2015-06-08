# -*- coding: utf-8 -*-

"""
Module implementing Loading.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_load import Ui_Load


class Loading(QDialog, Ui_Load):
    """
    Class documentation goes here.
    """
    def __init__(self, maximum, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.setMaximum(maximum)
        
    def set_loading(self, progress):
        self.progressBar.setValue(progress)
