# -*- coding: utf-8 -*-

"""
Module implementing Edit.
"""

from PyQt4.QtCore import pyqtSignature, QString
from PyQt4.QtGui import QDialog

from Ui_edit import Ui_Edit


class Edit(QDialog, Ui_Edit):
    """
    Class documentation goes here.
    """
    def __init__(self, song, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.song = song
        infos = self.song.get_all()
        
        self.trackLE.setText(self.getValidString(infos['track']))
        self.cdLE.setText(self.getValidString(infos['cd']))
        self.bpmLE.setText(self.getValidString(infos['bpm']))
        self.titleLE.setText(self.getValidString(infos['title']))
        self.interpreterLE.setText(self.getValidString(infos['interpreter']))
        self.composerLE.setText(self.getValidString(infos['composer']))
        self.albuminterpreterLE.setText(self.getValidString(infos['albuminterpreter']))
        self.albumLE.setText(self.getValidString(infos['album']))
        self.genreLE.setText(self.getValidString(','.join(infos['genre'])))
        self.yearLE.setText(self.getValidString(infos['year']))
        self.commentTE.setText(self.getValidString(infos['comment']))

    def get_infos(self):
        return unicode(self.trackLE.text()), unicode(self.cdLE.text()), unicode(self.bpmLE.text()), unicode(self.titleLE.text()), unicode(self.interpreterLE.text()), unicode(self.composerLE.text()), unicode(self.albuminterpreterLE.text()), unicode(self.albumLE.text()), unicode(self.yearLE.text()), unicode(self.commentTE.toPlainText())

    def getValidString(self,  value):
        if value:
            return QString(value)
        else:
            return QString()

    @pyqtSignature("QAbstractButton*")
    def on_buttonBox_clicked(self, button):
        """
        Slot documentation goes here.
        """
        if button.text() == 'Save':
            self.accept()
        else:
            self.reject()
