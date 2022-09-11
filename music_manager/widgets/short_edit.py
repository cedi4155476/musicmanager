

class ShortEdit:
    def __init__(self, widget_handler, db):
        self.widget_handler = widget_handler
        self.db = db
        self.song = None
    
    def setup(self, song_handler):
        self.song_handler = song_handler

    def set_info(self, song):
        """
        Create the infos on the left
        """
        self.widget_handler.GUI.lineEditTitle.setText(song.title)
        self.widget_handler.GUI.lineEditArtist.setText(song.artist)
        self.widget_handler.GUI.lineEditAlbum.setText(song.album)
        self.widget_handler.GUI.lineEditComment.setText(song.comment)
        self.widget_handler.GUI.spinBoxRating.setValue(int(song.rating))
        self.song = song

    def save(self):
        if not self.song:
            return
        title = self.widget_handler.GUI.lineEditTitle.text()
        artist = self.widget_handler.GUI.lineEditArtist.text()
        album = self.widget_handler.GUI.lineEditAlbum.text()
        comment = self.widget_handler.GUI.lineEditComment.text()
        rating = self.widget_handler.GUI.spinBoxRating.value()

        self.song.update(title, album, artist, comment, rating)
        self.db.update_song(self.song)
        self.widget_handler.FILTER.get_all_checkboxes()
        self.song_handler.update_file(self.song)
        self.widget_handler.MAINTABLE.fill_table()

    def genre_button_clicked(self):
        if not self.song:
            return
        self.db.commit()
        genre_dialog = self.widget_handler.get_genre_dialog(self.db, self.song)
        genre_dialog.exec()
        self.db.commit()
        self.song.update_genres(self.db.get_all_genres_of_song(self.song))
        self.song_handler.update_file(self.song)
        self.widget_handler.FILTER.get_all_checkboxes()
        self.widget_handler.MAINTABLE.fill_table()