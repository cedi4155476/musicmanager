# -*- coding: utf-8 -*-

"""
Module implementing Edit.
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from handlers import widget_handler

from views.Ui_edit import Ui_Edit


class Edit(QDialog, Ui_Edit):
    """
    Class documentation goes here.
    """
    def __init__(self, widget_handler, db, parent=None):
        """
        Set all LineEdits if they already exist
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.song = None
        
        self.db = db
        self.widget_handler = widget_handler
        self.path = None

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

    def set_infos(self, song):
        self.widget_handler.GUI.trackLE.setText(song.track)
        self.widget_handler.GUI.cdLE.setText(song.cd)
        self.widget_handler.GUI.bpmLE.setText(song.bpm)
        self.widget_handler.GUI.titleLE.setText(song.title)
        self.widget_handler.GUI.artistLE.setText(song.artist)
        self.widget_handler.GUI.composerLE.setText(song.composer)
        self.widget_handler.GUI.albumartistLE.setText(song.albumartist)
        self.widget_handler.GUI.albumLE.setText(song.album)
        self.widget_handler.GUI.yearLE.setText(song.year)
        self.widget_handler.GUI.commentTE.setText(song.comment)

    def get_infos(self):
        return self.widget_handler.GUI.trackLE.text(), self.widget_handler.GUI.cdLE.text(),self.widget_handler.GUI.bpmLE.text(), \
               self.widget_handler.GUI.titleLE.text(), self.widget_handler.GUI.artistLE.text(), \
               self.widget_handler.GUI.composerLE.text(), self.widget_handler.GUI.albumartistLE.text(), \
               self.widget_handler.GUI.albumLE.text(), self.widget_handler.GUI.yearLE.text(), \
               self.widget_handler.GUI.commentTE.toPlainText()

    @pyqtSlot("QAbstractButton*")
    def on_buttonBox_clicked(self, button):
        """
        Save Changes
        """
        if button.text() == 'Save':
            self.accept()
        else:
            self.reject()
    
    @pyqtSlot()
    def on_editGenreButton_clicked(self):
        """
        Open Genre edit Box
        """
        self.gdlg = self.wh.get_genre(self.db, self.path)
        self.gdlg.exec_()
