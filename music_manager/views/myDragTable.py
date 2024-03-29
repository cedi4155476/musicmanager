from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class MyDragTable(QTableWidget):
    """
    add drag functionality to table
    """
    activate = pyqtSignal(QTableWidgetItem)
    returnpressed = pyqtSignal()

    def __init__(self, parent=None):
        QTableWidget.__init__(self)

    def itemClicked(self, item):
        self.activate.emit(item)

    def keyPressEvent(self, e):
        if e.type() == QEvent.KeyPress:
                if e.key() == Qt.Key_Return:
                    self.returnpressed.emit()
        QTableWidget.keyPressEvent(self, e)

    def mimeTypes(self):
        return ('application/x-songlistdata')

    def mimeData(self, list):
        bytearray = QByteArray()
        for item in list:
            if item.column() == 1:
                bytearray.append(self.item(item.row(), 0).text() + '*-_-*')

        bytearray.chop(5)

        mimeData = QMimeData()
        mimeData.setData('application/x-songlistdata', bytearray)
        return mimeData
