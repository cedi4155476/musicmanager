from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyTreeView(QTreeView):
    """
    tree view with click event
    """

    def __init__(self, parent=None):
        QTreeView.__init__(self)

    def mousePressEvent(self, e):
        self.clearSelection()
        QTreeView.mousePressEvent(self, e)
