# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QSystemTrayIcon, QMenu

from views.Ui_GUI import Ui_MainWindow

class GUI(QMainWindow, Ui_MainWindow):
    """
    Main container for all widgets.
    """

    def __init__(self, wh, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self,  parent)
        self.wh = wh
        self.setupUi(self)
        self.adjust_gui()
        self.createSystemTray()
        self.genreWidget.setAccessibleName("genre filter widget")
        self.interpreterWidget.setAccessibleName("interpreter filter widget")
        self.albumWidget.setAccessibleName("album filter widget")

    def adjust_gui(self):
        """
        adjust the gui
        """
        self.musicframe.setVisible(False)
        self.tableWidget.hideColumn(0)
        self.playlistWidget.hideColumn(0)
        self.playlistWidget.horizontalHeader().setSectionResizeMode (1, QHeaderView.Stretch)
        self.playlistWidget.setColumnWidth(2, 70)
        self.playlistSearchLineEdit.setView(self.wh.MYLISTVIEW)


    # TODO: MAYBE SOMEWHERE ELSE
    def createSystemTray(self):
        """
        make the system tray icon and what is needed
        """
        self.trayicon = QSystemTrayIcon(self)
        self.trayicon.setToolTip("Music Manager")
        self.traymenu = QMenu(self)
        self.traymenu.addAction("Open", self.openWindow)
        self.traymenu.addAction("Exit", self.exitWindow)
        self.trayicon.setContextMenu(self.traymenu)
        self.trayicon.setIcon(QIcon('resources/trayicon.png'))
        self.trayicon.activated.connect(self.trayactivated)
        self.doubleclicktimer = QTimer()
        self.doubleclicktimer.setSingleShot(True)
        self.doubleclicktimer.timeout.connect(self.waitForDoubleclick)
        self.trayicon.show()

    def openWindow(self):
        """
        when open is choosed in tray icon context menu show main window
        """
        self.showNormal()

    def exitWindow(self):
        """
        close application if exit is pressed int context menu of tray icon
        """
        self.pausePlayer()
        QApplication.quit()

    def trayactivated(self, type):
        """
        if tray icon is doubleclicked show window or if single clicked show context menu
        """
        if type == 2:
            self.doubleclicktimer.stop()
            self.showNormal()
        elif type == QSystemTrayIcon.Trigger:
            self.doubleclicktimer.start(200)

    def waitForDoubleclick(self):
        """
        wait if user makes a doubleclick
        """
        self.traymenu.popup(QCursor.pos())

    def tableWidgetContextMenu(self, pos):
        """
        create context menu for playlist tree
        """
        self.contextindex = self.tableWidget.indexAt(pos)
        if self.contextindex.isValid():
            menu = QMenu(self)
            menu.addAction('Edit', self.contextEditSong)
            menu.exec_(self.tableWidget.mapToGlobal(pos))

