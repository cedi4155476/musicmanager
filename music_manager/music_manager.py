import sys,  os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from widgets.gui import MainWindow

def launch():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec_()

if __name__ == "__main__":
    launch()