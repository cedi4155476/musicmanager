# from PyQt5.QtWidgets import 
from PyQt5.QtCore import QVariant


class PlaylistTreeItem():
    def __init__(self, data, parent = None):
        self.m_itemData = data
        self.m_parentItem = parent

    def __del__(self):
        self.qDeleteAll(self.m.childItems)

    def appendChild(self, item):
        self.m_childItems.append(item)

    def child(self, row):
        if row < 0 or row >= len(self.m_childItems):
            return
        return self.m_childItems[row]
    
    def childCount(self):
        return len(self.m_childItems)

    def row(self):
        if self.m_parentItem:
            return self.m_parentItem.m_childItems.index(self)
        return 0

    def columnCount(self):
        return len(self.m_itemData)

    def data(self, column):
        if column < 0 or column >= len(self.m_itemData):
            return QVariant()
        return self.m_itemData[column]

    def parentItem(self):
        return self.m_parent