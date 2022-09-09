# from PyQt5.QtWidgets import 
from PyQt5.QtCore import Qt, QVariant, QAbstractItemModel, QModelIndex
from PyQt5.QtGui import QIcon

from objects.playlist_tree_item import PlaylistTreeItem

class PlaylistTreeModel(QAbstractItemModel):
    def __init__(self, data, parent = None):
        super().__init__(parent)
        self.rootItem = PlaylistTreeItem(("icon","id","name","parent"))
        self.folder_icon = QIcon('resources/folder_icon.png')
        self.playlist_icon = QIcon('resources/playlist_icon.png')
        self.setup_model_data(data, self.rootItem)
    
    def __del__(self):
        del self.rootItem

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        parentItem = self.rootItem
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        childItem = index.internalPointer()
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
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())
        elif role == Qt.DecorationRole:
            item = index.internalPointer()
            return item.data(index.column())
        else:
            return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, orientation, section, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return QVariant()

    def setup_model_data(self, data, parent):
        sections = data[0]
        playlists = data[1]
        for section in sections:
            if not section["parent"]:
                section_parent = parent
            else:
                section_parent = parent.find_section(section["parent"])
            section_parent.appendChild([self.folder_icon]+list(section.values()), True)
        for playlist in playlists:
            if not playlist["playlist_section_fk"]:
                section_parent = parent
            else:
                section_parent = parent.find_section(playlist["playlist_section_fk"])
            section_parent.appendChild([self.playlist_icon]+list(playlist.values()), False)
        
    def get_id(self, index):
        if not index.isValid():
            return False
        return index.internalPointer().data(1)
        
    def get_name(self, index):
        if not index.isValid():
            return False
        return index.internalPointer().data(2)
        
    def get_parent(self, index):
        if not index.isValid():
            return False
        return index.internalPointer().data(3)

    def is_section(self, index):
        if not index.isValid():
            return False
        return index.internalPointer().is_section