# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from views.Ui_GUI import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main container for all widgets.
    """

    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self,  parent)
        self.setupUi(self)
