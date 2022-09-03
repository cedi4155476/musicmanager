from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeView

class MyTreeView(QTreeView):
    """
    tree view with click event
    """

    def __init__(self, parent=None):
        QTreeView.__init__(self)

    def mousePressEvent(self, e):
        self.clearSelection()
        QTreeView.mousePressEvent(self, e)
