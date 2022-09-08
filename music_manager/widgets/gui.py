# -*- coding: utf-8 -*-
"""
Module implementing MainWindow.
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QSystemTrayIcon, QMenu, QApplication

from views.Ui_GUI import Ui_MainWindow

class GUI(QMainWindow, Ui_MainWindow):
    """
    Main container for all widgets.
    """

    def __init__(self, widget_handler, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self,  parent)
        self.widget_handler = widget_handler
        self.setupUi(self)
        self.adjust_gui()
        self.create_system_tray()
        self.genreWidget.setAccessibleName("genre filter widget")
        self.artistWidget.setAccessibleName("artist filter widget")
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
        self.playlistSearchLineEdit.setView(self.widget_handler.MYLISTVIEW)

    def create_system_tray(self):
        """
        make the system tray icon and what is needed
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setToolTip("Music Manager")
        self.tray_menu = QMenu(self)
        self.tray_menu.addAction("Open", self.open_window)
        self.tray_menu.addAction("Exit", self.exit_window)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.setIcon(QIcon('resources/trayicon.png'))
        self.tray_icon.activated.connect(self.tray_activated)
        self.double_click_timer = QTimer()
        self.double_click_timer.setSingleShot(True)
        self.double_click_timer.timeout.connect(self.wait_for_double_click)
        self.tray_icon.show()

    def open_window(self):
        """
        when open is choosen in tray icon context menu show main window
        """
        self.showNormal()

    def exit_window(self):
        """
        close application if exit is pressed int context menu of tray icon
        """
        self.widget_handler.MUSICPLAYER.pause()
        QApplication.quit()

    def tray_activated(self, type):
        """
        if tray icon is doubleclicked show window or if single clicked show context menu
        """
        if type == 2:
            self.double_click_timer.stop()
            self.showNormal()
        elif type == QSystemTrayIcon.Trigger:
            self.double_click_timer.start(200)

    def wait_for_double_click(self):
        """
        wait if user makes a doubleclick
        """
        self.tray_menu.popup(QCursor.pos())

    @pyqtSlot("QAction*")
    def on_menuBar_triggered(self, action):
        """
        menu bar actions
        """
        if action.text() == "Refresh":
            self.widget_handler.MUSICMANAGER.refresh()

        elif action.text() == "Change Directory":
            self.widget_handler.MUSICMANAGER.change_directory()

        elif action.text() == "Exit":
            QApplication.quit()

        elif action.text() == "Edit":
            self.editSong()

        elif action.text() == "Info":
            self.widget_handler.INFO.show()

    # PYQT FUNCTION
    def closeEvent(self, event):
        """
        handle the close event and stop music and save volume
        """
        if self.widget_handler.MUSICPLAYER.isVisible() or self.musicdock.isVisible():
            self.hide()
        else:
            self.widget_handler.MUSICPLAYER.close()
            self.widget_handler.PLAYLIST.close()
            QApplication.quit()
            event.accept()
        event.ignore()

    @pyqtSlot()
    def on_filterResetButton_clicked(self):
        """
        reset song filter
        """
        self.widget_handler.FILTER.reset()

    @pyqtSlot()
    def on_playlistSaveButton_clicked(self):
        """
        save playlist
        """
        self.widget_handler.PLAYLIST.create_playlist()

    @pyqtSlot("QTableWidgetItem*")
    def on_playlistWidget_itemDoubleClicked(self, item):
        """
        play clicked song
        """
        self.widget_handler.MUSICPLAYER.play_selected_song()

    @pyqtSlot()
    def on_tableWidget_itemSelectionChanged(self):
        """
        change current editable
        """

        if self.tableWidget.selectedItems():
            item = self.tableWidget.selectedItems()[0]
            self.widget_handler.MAINTABLE.selection_changed(item)

    @pyqtSlot("QModelIndex")
    def on_playlistTreeView_doubleClicked(self, index):
        """
        create playlist in clicked folder or load playlist
        """
        if self.model.isDir(index):
            self.playlistTab.setCurrentIndex(1)
        else:
            self.loadFileToPlaylist(index)

    @pyqtSlot()
    def on_playlistCreateFolderButton_clicked(self):
        """
        create folder
        """
        self.widget_handler.PLAYLIST.create_folder()

    # @pyqtSlot()
    # def on_playlistSearchButton_clicked(self):
    #     """
    #     search playlist or folder
    #     """
    #     self.search_playlist()

    @pyqtSlot()
    def on_playlistFolderLineEdit_returnPressed(self):
        """
        search playlist or folder
        """
        self.widget_handler.PLAYLIST.create_folder()

    def playlistSearchEnterPressed(self):
        """
        search playlist or folder
        """
        self.widget_handler.PLAYLIST.search_playlist()

    @pyqtSlot()
    def on_playpausebutton_clicked(self):
        """
        play or pause music
        """
        self.widget_handler.MUSICPLAYER.play_pause_button_clicked()

    @pyqtSlot()
    def on_previousbutton_clicked(self):
        """
        play last song
        """
        self.widget_handler.MUSICPLAYER.load_last()

    @pyqtSlot()
    def on_nextbutton_clicked(self):
        """
        play next song
        """
        self.widget_handler.MUSICPLAYER.load_next()

    @pyqtSlot("int")
    def on_soundSlider_valueChanged(self, value):
        """
        change volume
        """
        self.widget_handler.MUSICPLAYER.change_volume(value)

