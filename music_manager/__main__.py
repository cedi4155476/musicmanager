#! /usr/bin/python
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from GUI import MainWindow


def launch():
    os.chdir('music_manager')
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    QTimer.singleShot(0,  lambda: mw.start())
    app.exec_()

launch()

if __main__ == "__main__":
    launch()
