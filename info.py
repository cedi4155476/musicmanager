# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_info import Ui_Info


class Info(QDialog, Ui_Info):
    """
    show information of programm
    """
    def __init__(self, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
