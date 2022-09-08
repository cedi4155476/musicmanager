from PyQt5.QtWidgets import QSpacerItem, QCheckBox, QSizePolicy
from PyQt5.QtCore import Qt

class Filter:
    def __init__(self):
        self.checkboxes = []
        self.widget_handler = None
        self.song_handler = None
    
    def setup(self, song_handler, widget_handler):
        self.widget_handler = widget_handler
        self.song_handler = song_handler

    def reset(self):
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def get_allBoxes(self):
        """
        removes then creates all boxes for filtering
        """
        for checkbox in self.checkboxes:
            self.widget_handler.GUI.genreLayout.removeWidget(checkbox)
            self.widget_handler.GUI.albumLayout.removeWidget(checkbox)
            self.widget_handler.GUI.artistLayout.removeWidget(checkbox)
            checkbox.hide()

        if hasattr(self.widget_handler.GUI, "aspacerItem"):
            self.widget_handler.GUI.albumLayout.removeItem(self.widget_handler.GUI.aspacerItem)
        if hasattr(self.widget_handler.GUI, "gspacerItem"):
            self.widget_handler.GUI.genreLayout.removeItem(self.widget_handler.GUI.gspacerItem)
        if hasattr(self.widget_handler.GUI, "ispacerItem"):
            self.widget_handler.GUI.artistLayout.removeItem(self.widget_handler.GUI.ispacerItem)

        self.checkboxes = []

        self.get_file_informations()

        self.create_all_checkboxes()

    def get_file_informations(self):
        """
        get all the folder filters
        """
        folder_genres = set(['empty'])
        folder_artists = set()
        folder_albums = set()
        for song in self.song_handler.songs.values():
                folder_genres.update(song.genres)
                folder_artists.add(song.artist)
                folder_albums.add(song.album)
        self.folder_genres = list(folder_genres)
        self.folder_artists = list(folder_artists)
        self.folder_albums = list(folder_albums)

    def create_checkbox(self, text, widget, layout):
        """
        create a checkbox for filtering
        """
        checkBox = QCheckBox(widget)
        checkBox.setLayoutDirection(Qt.LeftToRight)
        checkBox.setObjectName(text)
        layout.addWidget(checkBox)
        checkBox.setText(text)
        checkBox.stateChanged.connect(self.checkCheckboxes)
        self.checkboxes.append(checkBox)

    def create_all_checkboxes(self):
        """
        creates all checkboxes for filtering
        """
        for genre in self.folder_genres:
            self.create_checkbox(genre, self.widget_handler.GUI.genreWidget, self.widget_handler.GUI.genreLayout)

        if len(self.folder_genres) < 20:
            self.widget_handler.GUI.gspacerItem = QSpacerItem(70, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.widget_handler.GUI.genreLayout.addSpacerItem(self.widget_handler.GUI.gspacerItem)

        i = 0
        for artist in self.folder_artists:
            if artist:
                self.create_checkbox(artist, self.widget_handler.GUI.artistWidget, self.widget_handler.GUI.artistLayout)
                i += 1

        if i < 20:
            self.widget_handler.GUI.ispacerItem = QSpacerItem(70, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.widget_handler.GUI.artistLayout.addSpacerItem(self.widget_handler.GUI.ispacerItem)

        i = 0
        for album in self.folder_albums:
            if album:
                self.create_checkbox(album, self.widget_handler.GUI.albumWidget, self.widget_handler.GUI.albumLayout)
                i += 1

        if i < 20:
            self.widget_handler.GUI.aspacerItem = QSpacerItem(70, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.widget_handler.GUI.albumLayout.addSpacerItem(self.widget_handler.GUI.aspacerItem)

    def checkCheckboxes(self):
        """
        checks all checkboxes and shows the filtered ones
        """
        activated_checkboxes = self.checkBoxTypes()
        self.song_handler.filtersongs = []
        if not activated_checkboxes:
            self.widget_handler.MAINTABLE.fill_table()

        for song in self.song_handler.songs.values():
            if self.filter_song(song, activated_checkboxes):
                self.song_handler.filtersongs.append(song)
        self.widget_handler.MAINTABLE.reload_table()

    def checkBoxTypes(self):
        """
        checks how many checkboxes are active and which types
        """
        activated_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.isChecked():
                if checkbox.parentWidget().accessibleName() == "genre filter widget":
                    activated_checkboxes.append(("genres", checkbox.text()))

                if checkbox.parentWidget().accessibleName() == "album filter widget":
                    activated_checkboxes.append(("album", checkbox.text()))

                if  checkbox.parentWidget().accessibleName() == "artist filter widget":
                    activated_checkboxes.append(("artist", checkbox.text()))
        return activated_checkboxes

    def filter_song(self, song, activated_checkboxes):
        for checkbox in activated_checkboxes:
            song_dict = song.__dict__
            if checkbox[0] == "genres":
                if not checkbox[1] in song_dict[checkbox[0]]:
                    return False
            else:
                if not song_dict[checkbox[0]] == checkbox[1]:
                    return False
        return True
    
    def remove_all_checkboxes(self):
        for checkbox in self.checkboxes:
            self.widget_handler.GUI.genreLayout.removeWidget(checkbox)
            self.widget_handler.GUI.albumLayout.removeWidget(checkbox)
            self.widget_handler.GUI.artistLayout.removeWidget(checkbox)
            checkbox.hide()
        self.checkboxes = []
