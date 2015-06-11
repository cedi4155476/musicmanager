from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyDropTable(QTableWidget):
    drop = pyqtSignal(QTableWidgetItem)
    
    def __init__(self, parent=None):
        QTableWidget.__init__(self)
        self.setAcceptDrops(True)
        
    def dropEvent(self,  e):
        bytearray = e.mimeData().data('application/x-qabstractitemmodeldatalist')
        paths = self.decode_data(bytearray)
        for path in paths:
            print path
        
    def decode_data(self, bytearray):
        
        ds = QDataStream(bytearray)
        item = []
        while not ds.atEnd():
            row = ds.readInt32()
            column = ds.readInt32()
            
            map_items = ds.readInt32()
            
            for i in range(map_items):
                key = ds.readInt32()
                value = QVariant()
                ds >> value
                if column == 1:
                    item.append(value.toString())
        return item
