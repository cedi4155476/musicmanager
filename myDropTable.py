from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyDropTable(QTableWidget):
    drop = pyqtSignal(QTableWidget, list)
    
    def __init__(self, parent=None):
        QTableWidget.__init__(self)
        self.setAcceptDrops(True)
        
    def dropEvent(self,  e):
#        if e.mimeData().fomats()=='application/x-songlist':
            bytearray = e.mimeData().data('application/x-qabstractitemmodeldatalist')
            ds = QDataStream(bytearray)
            rows = []
            while not ds.atEnd():
                rows.append(ds.readInt32())
                ds.readInt32()
                
                map_items = ds.readInt32()
                
                for i in range(map_items):
                    ds.readInt32()
                    value = QVariant()
                    ds >> value
            self.drop.emit(self, rows)
