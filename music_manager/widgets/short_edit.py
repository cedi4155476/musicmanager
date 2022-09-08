

class ShortEdit:
    def __init__(self, widget_handler, db):
        self.widget_handler = widget_handler
        self.db = db
    
    def set_info(self, song):
        """
        Create the infos on the left
        """
        self.widget_handler.GUI.lineEditTitle.setText(song.title)
        self.widget_handler.GUI.lineEditArtist.setText(song.artist)
        self.widget_handler.GUI.lineEditAlbum.setText(song.album)
        self.widget_handler.GUI.lineEditComment.setText(song.comment)
        self.widget_handler.GUI.spinBoxRating.setValue(int(song.rating))
