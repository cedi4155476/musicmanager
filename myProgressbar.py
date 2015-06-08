from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyProgressbar(QProgressBar):
    releasePlay = pyqtSignal()
    progressMovement = pyqtSignal(float)
    
    def __init__(self, parent=None):
        QProgressBar.__init__(self)
        
            
    def mousePressEvent(self, e):
        self.mouseMoveEvent(e)
            
    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) is not 0:
            if e.pos().x() < 0:
                self.x = 0
            elif e.pos().x() > self.width():
                self.x = self.width() / self.width()
            else:
                self.x = e.pos().x() / float(self.width())
                
            self.progressMovement.emit(self.x)
            
    def mouseReleaseEvent(self, e):
        self.releasePlay.emit()
