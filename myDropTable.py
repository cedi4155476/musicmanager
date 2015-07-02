from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyDropTable(QTableWidget):
    playlistInfo = pyqtSignal(str, bool)
    
    def __init__(self, parent=None):
        QTableWidget.__init__(self)
        self.setAcceptDrops(True)

    def mimeTypes(self):
        types =['application/x-songlistdata', 'text/x-moz-url']
        return types

    def dragEnterEvent(self, e):
         if e.mimeData().hasFormat('application/x-songlistdata') or e.mimeData().hasFormat('text/x-moz-url'):
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        #Funktion MUSS Ueberschrieben werden
        pass

    def dropMimeData(self, row, column, data, action):
        if data.hasFormat('application/x-songlistdata'): 
            bytearray = data.data('application/x-songlistdata')
            paths = bytearray.data().split('\\')
        else:
            paths = []
            for url in data.urls():
                paths.append(url.toString()[7:])

        for path in paths:
            self.playlistInfo.emit(path, True)
        return True
