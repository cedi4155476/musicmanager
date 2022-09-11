# from PyQt5.QtWidgets import 
from PyQt5.QtCore import QVariant, QObject


class PlaylistTreeItem:
    def __init__(self, data, section = False, parent = None):
        self.item_data = data
        self.parent_item = parent
        self.child_items = []
        self.section = section

    def __del__(self):
        del self.child_items

    def appendChild(self, item, section):
        self.child_items.append(PlaylistTreeItem(item, section, self))

    def child(self, row):
        if row < 0 or row >= len(self.child_items):
            return
        return self.child_items[row]
    
    def childCount(self):
        return len(self.child_items)

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0

    def columnCount(self):
        return len(self.item_data)

    def data(self, column):
        if column < 0 or column >= len(self.item_data):
            return QVariant()
        return self.item_data[column]

    def parentItem(self):
        return self.parent_item

    def is_section(self):
        return self.section

    def remove_child(self, row):
        if row < 0 or row > len(self.child_items):
            return False
        self.child_items.pop(row)
        return True

    def find_section(self, section_id):
        for child in self.child_items:
            if child.data(1) == section_id:
                return child
            in_child = child.find_section(section_id)
            if in_child:
                return in_child
        return None