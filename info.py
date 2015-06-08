# -*- coding: utf-8 -*-

"""
Module implementing Info.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_info import Ui_Info


class Info(QDialog, Ui_Info):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
    
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        
