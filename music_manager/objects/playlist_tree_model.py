# from PyQt5.QtWidgets import 
from PyQt5.QtCore import Qt, QVariant, QAbstractItemModel, QModelIndex

from objects.playlist_tree_item import PlaylistTreeItem

class PlaylistTreeModel(QAbstractItemModel):
    def __init__(self, data = None, parent = None):
        super().__init__(parent)
        self.rootItem = PlaylistTreeItem({tr("Title"), tr("Summary")})
        self.setupModelData(data.split("\n"), self.rootItem)
    
    def __del__(self):
        del self.rootItem

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        parentItem = self.rootItem
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = PlaylistTreeItem(parent.internalPointer())

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = PlaylistTreeItem(index.internalPointer())
        parentItem = childItem.parentItem()
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(),0,parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = PlaylistTreeItem(parent.internalPointer())
        return parentItem.childCount()

    def columnCount(self, parent):
        if parent.isValid():
            return PlaylistTreeItem(parent.internalPointer()).columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
        item = PlaylistTreeItem(index.internalPointer())
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return QAbstractItemModel.flags(index)

    def headerData(self, orientation, section, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return QVariant()