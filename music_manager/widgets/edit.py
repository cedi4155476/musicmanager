# -*- coding: utf-8 -*-

"""
Module implementing Edit.
"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog

from views.Ui_edit import Ui_Edit


class Edit(QDialog, Ui_Edit):
    """
    Class documentation goes here.
    """
    def __init__(self, wh, db, path, song, parent=None):
        """
        Set all LineEdits if they already exist
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.song = song
        infos = self.song.get_all()
        
        self.db = db
        self.wh = wh
        self.path = path

        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.trackLE.setText(infos['track'])
        self.cdLE.setText(infos['cd'])
        self.bpmLE.setText(infos['bpm'])
        self.titleLE.setText(infos['title'])
        self.interpreterLE.setText(infos['interpreter'])
        self.composerLE.setText(infos['composer'])
        self.albuminterpreterLE.setText(infos['albuminterpreter'])
        self.albumLE.setText(infos['album'])
        self.yearLE.setText(infos['year'])
        self.commentTE.setText(infos['comment'])

    def get_infos(self):
        return self.trackLE.text(), self.cdLE.text(),self.bpmLE.text(), \
               self.titleLE.text(), self.interpreterLE.text(), \
               self.composerLE.text(), self.albuminterpreterLE.text(), \
               self.albumLE.text(), self.yearLE.text(), \
               self.commentTE.toPlainText()

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
