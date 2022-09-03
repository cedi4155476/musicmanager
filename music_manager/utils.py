from PyQt5.QtCore import *

from os.path import expanduser
HOME = expanduser("~")
HOME += "/Documents/music_manager/"


def call_method(obj, method, *args, **kwargs):
    getattr(obj, method)(args,kwargs)


# def getValidString(value):
#     if value:
#         return QString(value)
#     else:
#         return QString()