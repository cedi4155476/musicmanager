# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cch/Documents/python/music_manager/music_manager/edit.ui'
#
# Created: Tue Aug 11 11:27:30 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Edit(object):
    def setupUi(self, Edit):
        Edit.setObjectName(_fromUtf8("Edit"))
        Edit.resize(400, 315)
        Edit.setSizeGripEnabled(True)
        Edit.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Edit)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setSpacing(10)
        self.horizontalLayout_15.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_9 = QtGui.QLabel(Edit)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_5.addWidget(self.label_9)
        self.label = QtGui.QLabel(Edit)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_5.addWidget(self.label)
        self.label_2 = QtGui.QLabel(Edit)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_5.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(Edit)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(Edit)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_5.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(Edit)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_5.addWidget(self.label_5)
        self.label_6 = QtGui.QLabel(Edit)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_5.addWidget(self.label_6)
        self.horizontalLayout_15.addLayout(self.verticalLayout_5)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(-1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.trackLE = QtGui.QLineEdit(Edit)
        self.trackLE.setObjectName(_fromUtf8("trackLE"))
        self.horizontalLayout_2.addWidget(self.trackLE)
        self.label_10 = QtGui.QLabel(Edit)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_2.addWidget(self.label_10)
        self.cdLE = QtGui.QLineEdit(Edit)
        self.cdLE.setObjectName(_fromUtf8("cdLE"))
        self.horizontalLayout_2.addWidget(self.cdLE)
        self.label_11 = QtGui.QLabel(Edit)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_2.addWidget(self.label_11)
        self.bpmLE = QtGui.QLineEdit(Edit)
        self.bpmLE.setEnabled(True)
        self.bpmLE.setObjectName(_fromUtf8("bpmLE"))
        self.horizontalLayout_2.addWidget(self.bpmLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.titleLE = QtGui.QLineEdit(Edit)
        self.titleLE.setObjectName(_fromUtf8("titleLE"))
        self.horizontalLayout.addWidget(self.titleLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.interpreterLE = QtGui.QLineEdit(Edit)
        self.interpreterLE.setObjectName(_fromUtf8("interpreterLE"))
        self.horizontalLayout_3.addWidget(self.interpreterLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.composerLE = QtGui.QLineEdit(Edit)
        self.composerLE.setObjectName(_fromUtf8("composerLE"))
        self.horizontalLayout_4.addWidget(self.composerLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.albuminterpreterLE = QtGui.QLineEdit(Edit)
        self.albuminterpreterLE.setEnabled(True)
        self.albuminterpreterLE.setObjectName(_fromUtf8("albuminterpreterLE"))
        self.horizontalLayout_5.addWidget(self.albuminterpreterLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.albumLE = QtGui.QLineEdit(Edit)
        self.albumLE.setObjectName(_fromUtf8("albumLE"))
        self.horizontalLayout_12.addWidget(self.albumLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setSpacing(-1)
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.editGenreButton = QtGui.QPushButton(Edit)
        self.editGenreButton.setObjectName(_fromUtf8("editGenreButton"))
        self.horizontalLayout_11.addWidget(self.editGenreButton)
        self.label_7 = QtGui.QLabel(Edit)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_11.addWidget(self.label_7)
        self.yearLE = QtGui.QLineEdit(Edit)
        self.yearLE.setObjectName(_fromUtf8("yearLE"))
        self.horizontalLayout_11.addWidget(self.yearLE)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_15.addLayout(self.verticalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_15)
        self.label_8 = QtGui.QLabel(Edit)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout.addWidget(self.label_8)
        self.commentTE = QtGui.QTextEdit(Edit)
        self.commentTE.setObjectName(_fromUtf8("commentTE"))
        self.verticalLayout.addWidget(self.commentTE)
        self.buttonBox = QtGui.QDialogButtonBox(Edit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Discard|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Edit)
        QtCore.QMetaObject.connectSlotsByName(Edit)

    def retranslateUi(self, Edit):
        Edit.setWindowTitle(_translate("Edit", "Edit Song", None))
        self.label_9.setText(_translate("Edit", "Track", None))
        self.label.setText(_translate("Edit", "Title", None))
        self.label_2.setText(_translate("Edit", "Interpreter", None))
        self.label_3.setText(_translate("Edit", "Composer", None))
        self.label_4.setText(_translate("Edit", "Album-Interpreter", None))
        self.label_5.setText(_translate("Edit", "Album", None))
        self.label_6.setText(_translate("Edit", "Genre", None))
        self.label_10.setText(_translate("Edit", "CD", None))
        self.label_11.setText(_translate("Edit", "BPM", None))
        self.editGenreButton.setText(_translate("Edit", "Edit Genres", None))
        self.label_7.setText(_translate("Edit", "Year", None))
        self.label_8.setText(_translate("Edit", "Comment:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Edit = QtGui.QDialog()
    ui = Ui_Edit()
    ui.setupUi(Edit)
    Edit.show()
    sys.exit(app.exec_())

