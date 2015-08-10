#! /usr/bin/python
import sys,  os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from GUI import MainWindow


def launch():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    QTimer.singleShot(0,  lambda: mw.start())
    app.exec_()

launch()
