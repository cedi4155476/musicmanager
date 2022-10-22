from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from random import randint, shuffle
from soupsieve import select

from utils import show_error_box, show_confirmation_box
from objects import PlaylistTreeModel
from exceptions import FileDeletedException

class Playlist:
    def __init__(self, widget_handler, db):
        self.db = db
        self.playlist = {}
        self.RANDOMNESS = False
        self.playlist_name = ""
        self.playlist_id = None
        self.section_name = None
        self.section_id = None
        self.selected_section_id = None
        self.amount_played = 0
        self.widget_handler = widget_handler

    def setup(self, song_handler):
        self.song_handler = song_handler
        self.widget_handler.GUI.playlistLineEdit.textChanged.connect(self.playlist_name_changed)
        self.playlist_widget = self.widget_handler.GUI.playlistWidget
        self.create_tree()

    def close(self):
        self.update_db_playlist()

    def playlist_name_changed(self, value):
        self.playlist_name = value

    def reset_all(self):
        self.playlist = {}
        self.RANDOMNESS = False
        self.playlist_name = ""
        self.playlist_id = None
        self.section_name = None
        self.section_id = None
        self.selected_section_id = None
        self.amount_played = 0

    def update_db_playlist(self):
        self.db.update_playlist(self.playlist, self.playlist_id, self.playlist_name, self.amount_played)

    def selection_changed(self, item):
        path = self.playlist_widget.item(item.row(),  0).text()
        song = self.song_handler.songs.get(path)

        if not song.path.exists():
            self.disable_row(song)
            return
        self.widget_handler.SHORTEDIT.set_info(song)
        self.playlist_widget.scrollToItem(item)
        self.widget_handler.MAINTABLE.select_row_by_song(song)

    def get_playlist_item(self, song):
        """
        get the playlistwidgetitem with song
        """
        for i in range(self.playlist_widget.rowCount()):
            if song.raw_path == self.playlist_widget.item(i, 0).text():
                return self.playlist_widget.item(i, 0)

    def disable_row(self, song):
        row = self.widget_handler.PLAYLIST.get_playlist_item(song.raw_path).row()
        for c in range(self.playlist_widget.columnCount()):
            item = self.playlist_widget.item(row, c)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

    def get_not_disabled_songs(self):
        """
        get not disabled songs
        """
        song_list = []
        for song in self.playlist.values():
            if not song.disabled:
                song_list.append(song)
        return song_list

    def get_song_with_index(self, index):
        """
        set the next song in normal mode
        """
        path = self.playlist_widget.item(index,  0).text()
        song = self.playlist[path]
        if not song.path.exists() or song.disabled:
            song.disable()
            self.disable_row(song)
            raise FileDeletedException()
        return song

    def get_next_random_song(self):
        """
        set the next song in random mode
        """
        enabled_songs = self.get_not_disabled_songs()
        if self.amount_played % 10 == 0:
            temp_playlist = []
            for song in enabled_songs:
                if song.playlist_played < self.amount_played/(10*len(self.playlist)) and not song.disabled:
                    temp_playlist.append(song)
            if not temp_playlist:

                temp_playlist = enabled_songs
        else:
            temp_playlist = enabled_songs

        counter = 0
        for song in temp_playlist:
            counter += song.playlist_chance
        chance = randint(1,counter)

        for song in temp_playlist:
            if song.playlist_chance >= chance:
                break
            chance -= song.playlist_chance
        
        if not song.path.exists():
            song.disable()
            self.disable_row(song)
            raise FileDeletedException()

        self.decrease_chance(song)
        self.increase_chance(song)
        self.amount_played += 1
        self.update_db_playlist()
        return song

    def increase_chance(self, played_song):
        """
        increase the chance in random mode
        """
        for song in self.playlist.values():
            if song != played_song:
                song.increase_chance(len(self.playlist))

    def decrease_chance(self, song):
        """
        decrease chance in random mode
        """
        song.decrease_chance(len(self.playlist))

    def playlist_add_paths(self, paths):
        for path in paths:
            self.playlist_add_path(path)

    def playlist_add_path(self, path):
        song = self.song_handler.songs.get(path)
        if not song:
            song = self.song_handler.create_song(path)

        self.playlist_add_song(song)

    def playlist_add_songs(self, songs):
        for song in songs:
            self.playlist_add_song(song)

    def playlist_add_song(self, song):
        """
        add song in playlist
        """
        if song.raw_path in self.playlist:
            return
        try:
            m, s = divmod(song.length, 60)
            orlength = ('%02d:%02d' % (m, s))

            if not song.title:
                qtitle = QTableWidgetItem(song.path.name)
            else:
                qtitle = QTableWidgetItem(song.title)
            qlength = QTableWidgetItem(orlength)
            qlength.setTextAlignment(Qt.AlignRight | Qt.AlignCenter)
            row = self.playlist_widget.rowCount()
            self.playlist_widget.insertRow(row)
            self.playlist_widget.setItem(row, 0, QTableWidgetItem(song.raw_path))
            self.playlist_widget.setItem(row, 1, qtitle)
            self.playlist_widget.setItem(row, 2, qlength)
            self.playlist[song.raw_path] = song
            # if sort:
            #     self.playlist_widget.sortItems(1)
        except (KeyError, UnboundLocalError):
            pass

    def create_tree(self):
        """
        create the tree for the playlists
        """
        self.model = PlaylistTreeModel((self.db.get_all_sections(),self.db.get_all_playlists()))
        self.widget_handler.GUI.playlistTreeView.setModel(self.model)
        self.widget_handler.GUI.playlistTreeView.hideColumn(1)
        self.widget_handler.GUI.playlistTreeView.hideColumn(3)
        self.widget_handler.GUI.playlistTreeView.setHeaderHidden(True)
        self.widget_handler.GUI.playlistTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget_handler.GUI.playlistTreeView.customContextMenuRequested.connect(self.playlist_tree_context_menu)

    def add_item_playlist_tree_view(self, object, section):
        self.model.add_item(object, section)

    def create_section(self):
        """
        create a new section for playlists
        """
        if self.widget_handler.GUI.playlistFolderLineEdit.text():
            section_name = self.widget_handler.GUI.playlistFolderLineEdit.text()
            section_id = self.db.create_playlist_section(section_name, self.selected_section_id)
            section = {"playlist_section_id": section_id, "section_name": section_name, "parent": self.selected_section_id}
            self.add_item_playlist_tree_view(section,True)
        else:
            show_error_box("Missing section name!", "Please enter a section name")

    def delete_selected_file(self):
        """
        delete a section or playlist in playlist tree
        """
        if self.widget_handler.GUI.playlistTreeView.selectedIndexes():
            index = self.widget_handler.GUI.playlistTreeView.selectedIndexes()[0]
            selected_id = self.model.get_id(index)
            if self.model.is_section(index):
                reply = show_confirmation_box("Are you sure?", "Are you sure to delete the section?\n All Playlists and Sections in it will be deleted as well.")
                if reply == QMessageBox.No:
                    return
                self.model.remove_child(index)
                self.db.delete_playlist_section(selected_id)
            else:
                reply = show_confirmation_box("Are you sure?", "Are you sure you want to delete the playlist?")
                if reply == QMessageBox.No:
                    return
                self.model.remove_child(index)
                self.db.delete_playlist(selected_id)
            self.db.commit()

    def remove_selected(self):
        if self.playlist_widget.selectedItems():
            rows = []
            for i in self.playlist_widget.selectedIndexes():
                rows.append(i.row())
            rows = list(set(rows))

            for row in reversed(rows):
                path = self.playlist_widget.item(row,0).text()
                del self.playlist[path]
                self.playlist_widget.removeRow(row)

    def search_playlist(self):
        """
        search a playlist or section
        """
        cursorposition = self.playlistSearchLineEdit.lineEdit().cursorPosition()
        matchlist = self.search_files(unicode(self.playlistSearchLineEdit.currentText()), self.model.index(self.model.rootPath()))
        if len(matchlist) == 1:
            idx = self.model.index(matchlist[0])
            self.playlistTreeView.setCurrentIndex(idx)
            self.playlistSearchLineEdit.clear()
        elif len(matchlist) > 1:
            tmp = self.playlistSearchLineEdit.currentText()
            self.playlistSearchLineEdit.clear()
            for name in matchlist:
                self.playlistSearchLineEdit.addItem(name)
            self.playlistSearchLineEdit.setEditText(tmp)
            self.playlistSearchLineEdit.showPopup()
            self.playlistSearchLineEdit.lineEdit().setFocus(Qt.PopupFocusReason)
            self.playlistSearchLineEdit.lineEdit().setCursorPosition(cursorposition)

    def search_files(self, name, parent):
        """
        search through all files and return matched
        """
        matchlist = []
        it = QDirIterator(parent.data().toString(), QDirIterator.Subdirectories)
        while it.hasNext():
            tmp = it.next()
            last = tmp.split("/")[-1]
            if name in last or name == tmp:
                matchlist.append(tmp)
        return matchlist

    def load_playlist_from_db(self, index):
        """
        load a playlist file to active playlist
        """
        if self.playlist and self.widget_handler.GUI.playlistLineEdit.text():
            reply = show_confirmation_box("Playlist overwrite", "Are you sure you want to overwrite the playlist?")
            if reply == QMessageBox.No:
                return
        self.playlist_widget.setRowCount(0)
        self.reset_all()

        self.playlist_id = self.model.get_id(index)
        self.playlist_name = self.model.get_name(index)
        self.section_id = self.model.get_parent(index)
        database_songs = self.db.get_all_songs_from_playlist(self.playlist_id)
        self.widget_handler.GUI.playlistLineEdit.setText(self.playlist_name)

        for song in database_songs:
            self.playlist_add_song(self.song_handler.get_or_create_song_from_playlist(song))
        self.widget_handler.GUI.playlistTab.setCurrentIndex(1)

    def create_playlist(self):
        """
        create a new playlist and save it
        """
        if not self.playlist_name:
            show_error_box("No Playlist Name", "Please insert a name for the before saving playlist!")
            return
        
        if self.playlist_widget.rowCount() == 0:
            show_error_box("No Songs Selected", "Please Drag and Drop some songs in the first Playlist!")
            return

        if self.section_id:
            section_id = self.section_id
        else:
            section_id = self.selected_section_id
        db_playlist = self.db.get_playlist_by_name(self.playlist_name, section_id)
        if db_playlist:
            reply = show_confirmation_box("Playlist overwrite", "Are you sure you want to overwrite the playlist?")
            if reply == QMessageBox.No:
                return
            self.db.update_playlist(self.playlist, self.playlist_id, self.playlist_name, self.amount_played)
            self.db.add_songs_to_playlist(self.playlist, self.playlist_id)
            self.db.remove_songs_from_playlist(self.playlist, self.playlist_id)
        else:
            playlist_id = self.db.create_playlist(self.playlist, self.playlist_name, self.amount_played, section_id)
            playlist = {"playlist_id": playlist_id, "playlist_name": self.playlist_name, "playlist_section_fk": section_id}
            self.add_item_playlist_tree_view(playlist, False)


    def table_to_playlist(self):
        """
        send edit table to playlist
        """
        if self.playlist and self.widget_handler.GUI.playlistLineEdit.text():
            reply = show_confirmation_box("Playlist overwrite", "Are you sure you want to overwrite the playlist?")
            if reply == QMessageBox.No:
                return
        self.playlist_widget.setRowCount(0)
        self.update_db_playlist()
        self.playlist = {}
        songs = self.song_handler.get_filtered_songs()

        self.playlist_add_songs(songs)
        for song in songs:
            self.playlist[song.raw_path] = song
        song = self.widget_handler.MAINTABLE.get_selected_song()
        item = self.get_playlist_item(song)
        self.playlist_widget.setCurrentItem(item)
        self.playlist_widget.setFocus()
        self.playlist_widget.setCurrentCell(self.playlist_widget.currentRow(), 1)

    def playlist_tree_context_menu(self, pos):
        """
        create context menu for playlist tree
        """
        index = self.playlistTreeView.indexAt(pos)
        if index.isValid():
            menu = QMenu(self)
            menu.addAction('loeschen', self.delete_selectedFile)
            if self.model.isDir(index):
                menu.addAction('Playlist erstellen', self.switchPlaylistTab)
            menu.exec_(self.playlistTreeView.mapToGlobal(pos))

    def tree_view_double_clicked(self, index):
        if self.model.is_section(index):
            self.widget_handler.GUI.playlistTab.setCurrentIndex(1)
            self.selected_section_id = self.model.get_id(index)
        else:
            self.load_playlist_from_db(index)

    def shuffle(self):
        if self.playlist:
            self.playlist_widget.setRowCount(0)
            songs = list(self.playlist.values())
            shuffle(songs)
            self.playlist = {}
            self.playlist_add_songs(songs)
            self.playlist_widget.setFocus()
            self.playlist_widget.setCurrentCell(0, 1)