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
        self.root_index = self.index(0,0,QModelIndex())
        self.setup_model_data(data)
    
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

    def setup_model_data(self, data):
        sections = data[0]
        playlists = data[1]
        for section in sections:
            self.add_item(section, True)
        for playlist in playlists:
            self.add_item(playlist, False)

    def add_item(self, obj, section):
        self.layoutAboutToBeChanged.emit()
        if section:
            if not obj["parent"]:
                section_parent = self.rootItem
            else:
                section_parent = self.rootItem.find_section(obj["parent"])
            section_parent.appendChild([self.folder_icon]+list(obj.values()), True)
            self.dataChanged.emit(self.root_index,self.get_index_from_id(obj["playlist_section_id"], section))
        else:
            if not obj["playlist_section_fk"]:
                section_parent = self.rootItem
            else:
                section_parent = self.rootItem.find_section(obj["playlist_section_fk"])
            section_parent.appendChild([self.playlist_icon]+list(obj.values()), False)
            self.dataChanged.emit(self.root_index,self.get_index_from_id(obj["playlist_id"], section))
        self.layoutChanged.emit()

    def get_index_from_id(self, child_id, section, index = QModelIndex()):
        if index.isValid():
            parent = index.internalPointer()
        else:
            parent = self.rootItem
        for i in range(parent.childCount()):
            child = parent.child(i)
            if child.data(1) == child_id and child.is_section() == section:
                return self.index(i, 1, index)
            in_child = self.get_index_from_id(child_id, section, self.index(i, 1, index))
            if in_child:
                return in_child
        return

    def remove_child(self, index):
        self.beginRemoveRows(index.parent(), index.row(), index.row())
        self.removeRow(index.row(), parent=index.parent())
        self.endRemoveRows()

    def removeRow(self, row, parent):
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        
        parentItem.remove_child(row)
        return True

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
        return index.internalPointer().is_section()