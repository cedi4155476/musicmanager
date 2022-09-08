from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from random import randint

from utils import show_error_box, show_confirmation_box
from objects import PlaylistTreeItem, PlaylistTreeModel
from exceptions import FileDeletedException

class Playlist:
    def __init__(self, widget_handler, db):
        self.db = db
        self.playlist = {}
        self.playlist_tree = {}
        self.RANDOMNESS = False
        self.playlist_name = ""
        self.playlist_id = None
        self.section_name = None
        self.section_id = None
        self.amount_played = 0
        self.widget_handler = widget_handler

    def setup(self, song_handler):
        self.song_handler = song_handler

    def close(self):
        self.update_db_playlist()

    def reset_all(self):
        self.playlist = {}
        self.playlist_name = ""
        self.amount_played = 0
        self.RANDOMNESS = False

    def update_db_playlist(self):
        self.db.update_playlist(self.playlist, self.playlist_id, self.playlist_name, self.amount_played)

    def load_playlist(self, songs, playlist_name, amount_played):
        self.reset_all()
        for song in songs:
            self.playlist[song.raw_path] = song
        self.playlist_name = playlist_name
        self.amount_played = amount_played

    def get_playlist_item(self, song):
        """
        get the playlistwidgetitem with song
        """
        for i in range(self.widget_handler.GUI.playlistWidget.rowCount()):
            if song.raw_path == self.widget_handler.GUI.playlistWidget.item(i, 0).text():
                return self.widget_handler.GUI.playlistWidget.item(i, 0)

    def disable_row(self, song):
        row = self.widget_handler.PLAYLIST.get_playlist_item(song.raw_path).row()
        for c in range(self.widget_handler.GUI.playlistWidget.columnCount()):
            item = self.widget_handler.GUI.playlistWidget.item(row, c)
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
        path = self.widget_handler.GUI.playlistWidget.item(index,  0).text()
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
            row = self.widget_handler.GUI.playlistWidget.rowCount()
            self.widget_handler.GUI.playlistWidget.insertRow(row)
            self.widget_handler.GUI.playlistWidget.setItem(row, 0, QTableWidgetItem(song.raw_path))
            self.widget_handler.GUI.playlistWidget.setItem(row, 1, qtitle)
            self.widget_handler.GUI.playlistWidget.setItem(row, 2, qlength)
            self.playlist[song.raw_path] = song
            # if sort:
            #     self.widget_handler.GUI.playlistWidget.sortItems(1)
        except (KeyError, UnboundLocalError):
            pass

    def create_tree(self):
        """
        create the tree for the playlists
        """
        self.model = PlaylistTreeModel()
        self.widget_handler.GUI.playlistTreeView.setModel(self.model)
        self.widget_handler.GUI.playlistTreeView.hideColumn(1)
        self.widget_handler.GUI.playlistTreeView.hideColumn(2)
        self.widget_handler.GUI.playlistTreeView.hideColumn(3)
        self.widget_handler.GUI.playlistTreeView.setHeaderHidden(True)
        self.widget_handler.GUI.playlistTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.widget_handler.GUI.playlistTreeView.customContextMenuRequested.connect(self.widget_handler.GUI.playlistTreeContextMenu)

    def create_section(self):
        """
        create a new folder for playlists
        """
        if self.widget_handler.GUI.playlistFolderLineEdit.text():
            playlist_name = self.widget_handler.GUI.playlistFolderLineEdit.text()
            section = None
            if self.widget_handler.GUI.playlistTreeView.selectedIndexes():
                index = self.widget_handler.GUI.playlistTreeView.selectedIndexes()[0]
                section = self.get_section(index)
            self.db.create_playlist_section(playlist_name, section)
        else:
            show_error_box("Missing section name!", "Please enter a section name")

    def delete_selectedFile(self):
        """
        delete a folder or playlist in playlist tree
        """
        if self.playlistTreeView.selectedIndexes():
            index = self.playlistTreeView.selectedIndexes()[0]
            path = self.get_path(index)
            if self.model.isDir(index):
                reply = QMessageBox.question(self, "Are you sure?", "Are you sure to delete the directory?\n All files and directories in it will be deleted.", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return
                shutil.rmtree(path)
            else:
                path += unicode(index.data().toString())
                reply = QMessageBox.question(self, "Are you sure?", "Are you sure to delete the file?", QMessageBox.Yes|QMessageBox.No);
                if reply == QMessageBox.No:
                    return
                os.remove(path)

    def get_section(self, index):
        """
        get path of selected file or folder
        """
        print()
        print(self.model.internalPointer(index))
        print()
        # if self.model.internalPointer(index):
        #     repath.append(unicode(index.data().toString()))
        # while True:
        #     index = index.parent()
        #     repath.append(unicode(index.data().toString()))
        #     if index.data().toString() == "playlists":
        #         break

        # for rpath in reversed(repath):
        #     path += rpath + "/"
        # return path

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
        if self.playlist and self.playlistLineEdit.text():
            reply = QMessageBox.question(self, "Playlist overwrite", "Are you sure you want to overwrite the playlist?", QMessageBox.Yes|QMessageBox.No);
            if reply == QMessageBox.No:
                return
        self.playlistWidget.setRowCount(0)
        self.playlist = {}

        path = self.get_path(index)
        path += unicode(index.data().toString())
        playlistname, songs = self.load_playlist(path)
        paths = []
        self.playlistLineEdit.setText(playlistname['name'])
        for song in songs:
            paths.append(song['path'])
        self.playlistAdd(paths, False)
        self.playlistTab.setCurrentIndex(1)

    def load_playlist(self, path):
        """
        get data from playlist
        """
        tree = ET.parse(path)
        root = tree.getroot()
        songs = []
        for child in root:
            if child.tag == "name":
                playlistname = child.attrib
            elif child.tag == "song":
                songs.append(child.attrib)
        return playlistname, songs

    def create_playlist(self):
        """
        create a new playlist and save it
        """
        if self.widget_handler.GUI.playlistTreeView.selectedIndexes():
            section = self.get_section(self.widget_handler.GUI.playlistTreeView.selectedIndexes()[0])
        else:
            section = None
        playlist_name = self.widget_handler.GUI.playlistLineEdit.text()

        if not playlist_name:
            show_error_box("No Playlist Name", "Please insert a name for the before saving playlist!")
            return
        
        if self.widget_handler.GUI.playlistWidget.rowCount() == 0:
            show_error_box("No Songs Selected", "Please Drag and Drop some songs in the first Playlist!")
            return

        if self.db.get_playlist_by_name(section):
            reply = show_confirmation_box("Playlist overwrite", "Are you sure you want to overwrite the playlist?")
            if reply == QMessageBox.No:
                return
            self.db.create_playlist(self.playlist, self.playlist_name, self.amount_played, section)
        else:
            self.db.create_playlist(self.playlist, self.playlist_name, self.amount_played, section)

    def tableToPlaylist(self):
        """
        send edit table to playlist
        """
        if self.playlist and self.widget_handler.GUI.playlistLineEdit.text():
            reply = show_confirmation_box("Playlist overwrite", "Are you sure you want to overwrite the playlist?")
            if reply == QMessageBox.No:
                return
        self.widget_handler.GUI.playlistWidget.setRowCount(0)
        self.playlist = {}
        if self.filtersongs:
            songs = []
            for song in self.filtersongs:
                songs.append(song.get_path())

        else:
            songs = self.song_handler.songs

        for path in songs:
            paths.append(path)
        self.playlistAdd(paths, False)
        item = self.get_playlistItemWithPath(self.Spath)
        self.playlistWidget.setCurrentItem(item)
        self.playlistWidget.setFocus()
        self.playlistWidget.setCurrentCell(self.playlistWidget.currentRow(), 1)