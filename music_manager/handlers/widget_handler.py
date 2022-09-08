import widgets

class WidgetHandler:

    def __init__(self, music_manager, config, db):
        self.MUSICMANAGER = music_manager
        self.FILTER = widgets.Filter()
        self.INFO = widgets.Info()
        self.MAINTABLE = widgets.MainTable()
        self.MYTREEVIEW = widgets.MyTreeView()
        self.PLAYLIST = widgets.Playlist(self, db)
        self.MYLISTVIEW = widgets.MyListView()
        self.GUI = widgets.GUI(self)
        self.MUSICPLAYER = widgets.MusicPlayer(self, config)
        self.SHORTEDIT = widgets.ShortEdit(self, db)

    def set_search_dialog(self, config, parent):
        self.SEARCH = widgets.SearchDialog(config, parent)
        return self.SEARCH
    
    def get_edit(self, db, path, song, parent = None):
        self.EDIT = widgets.Edit(self, db, path, song)
        return self.EDIT

    def get_genre(self, db, path, parent = None):
        return widgets.Genre(db, path, parent)
    
    def get_loading(self, max):
        return widgets.Loading(max)

    def reload_musicplayer(self):
        self.MUSICPLAYER = widgets.MusicPlayer(self)
