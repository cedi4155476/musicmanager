from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyDragTable(QTableWidget):
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
                bytearray.append(self.item(item.row(), 0).text() + '\\')
                
        bytearray.chop(1)
        
        mimeData = QMimeData()
        mimeData.setData('application/x-songlistdata', bytearray)
        return mimeData
