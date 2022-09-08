from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

from os.path import expanduser
HOME = expanduser("~")
HOME += "/Documents/music_manager/"


def call_method(obj, method, *args, **kwargs):
    getattr(obj, method)(args,kwargs)

def show_error_box(title, message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Warning)
    error_box.setText(message)
    error_box.setWindowTitle(title)
    error_box.setStandardButtons(QMessageBox.Ok)
    error_box.exec()

def show_confirmation_box(title, message):
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Warning)
    error_box.setText(message)
    error_box.setWindowTitle(title)
    error_box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
    return error_box.exec()


# def getValidString(value):
#     if value:
#         return QString(value)
#     else:
#         return QString()