from PyQt4.QtGui import *
from PyQt4.QtCore import *


class MyListView(QListView):
    """
    list view which closes with nearly every key
    """
    listviewclose = pyqtSignal()

    def __init__(self, parent=None):
        QListView.__init__(self)

    def keyPressEvent(self, e):
        if e.type() == QEvent.KeyPress:
            if e.key() == Qt.Key_Return or e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
                QListView.keyPressEvent(self, e)
            else:
                self.listviewclose.emit()
