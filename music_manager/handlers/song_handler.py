from distutils.log import error
import mutagen
from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3NoHeaderError

from PyQt5.QtWidgets import QMessageBox

from utils import show_error_box
from logger import Logger
from objects.song import Song

class SongHandler:
    def __init__(self, db, widget_handler):
        self.db = db
        self.widget_handler = widget_handler
        self.songs = {}

    def load_raw_songs(self, paths):
        """
        add all songs in db and check for errors
        """
        load_errors = []
        logger = Logger()
        loading_dialog = self.widget_handler.get_loading(len(paths))
        loading_dialog.show()
        i = 0

        for path in paths:
            if path.suffix == ".jpg":
                continue
            if path.exists():
                try:
                    song_file = self.read_file_info(path)
                    raw_database_song_info = self.db.get_song(str(path.resolve()))
                    if raw_database_song_info:
                        song_database = Song(path, raw_database_song_info)
                        if not song_file == song_database:
                            self.db.update_song(song_file)
                            song_file.update_from_database(song_database)
                        else:
                            song_file = song_database
                    else:
                        self.db.add_song(song_file)
                    self.songs[str(path.resolve())] = song_file
                except ValueError as e:
                    logger.warning(f"failed to load: {path}\tError Message: {e}")
                    load_errors.append(path)
                # try:
                #     data, genre = self.get_dbData(path)
                #     self.create_object(path, data, genre, playlist)
                # except:
                #     pass
                i+=1
                loading_dialog.progressBar.setValue(i)
            else:
                logger.warning(f"File deleted: {path}")
                load_errors.append(path)
                i+= 1
        if i >= len(paths):
            loading_dialog.close()
        self.db.commit()

        if len(load_errors) > 0:
            show_error_box("loading Error", f"{str(len(load_errors))} file(s) failed to load \n Maybe the file(s) do not exist anymore.\n More infos about the files in tmp/error.log file")
            load_errors = []

    def get_or_create_song_from_playlist(self, song):
        for s in self.songs.values():
            if s.song_id == song["song_id"]:
                s.playlist_played = song["times_played"]
                s.playlist_chance = song["chance"]
                return s
            
        raw_database_song_info = self.db.get_song_with_id(song["song_id"])
        return Song(raw_database_song_info["song_path"], raw_database_song_info)

    def read_file_info(self, path):
        """
        get the fileinfos
        """
        try:
            info = MP3(path)
            info_dict = {}
            info_dict["length"] = int(info.info.length)
            audio = mutagen.easyid3.EasyID3(path)
            try:
                info_dict["title"] = audio["title"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["title"] = ""

            try:
                info_dict["album"] = audio["album"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["album"] = ""

            try:
                if audio["genre"]:
                    info_dict["genres"] = audio["genre"]
                else:
                    info_dict["genres"] = ["empty"]
            except (ID3NoHeaderError, KeyError):
                info_dict["genres"] = ["empty", ]

            try:
                info_dict["artist"] = audio["artist"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["artist"] = ""

            try:
                info_dict["comment"] = audio["album"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["comment"] = ""

            try:
                info_dict["bpm"] = audio["bpm"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["bpm"] = ""

            try:
                info_dict["composer"] = audio["composer"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["composer"] = ""

            try:
                info_dict["cd"] = audio["discnumber"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["cd"] = ""

            try:
                info_dict["track"] = audio["tracknumber"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["track"] = ""

            try:
                info_dict["year"] = audio["date"][0]
            except (ID3NoHeaderError, KeyError):
                info_dict["year"] = ""

        except (ID3NoHeaderError):
            info_dict["title"] = ""
            info_dict["album"] = ""
            info_dict["artist"] = ""
            info_dict["comment"] = ""
            info_dict["genres"] = ["empty", ]
            info_dict["bpm"] = ""
            info_dict["composer"] = ""
            info_dict["cd"] = ""
            info_dict["track"] = ""
            info_dict["year"] = ""

        except HeaderNotFoundError:
            raise ValueError("Could not read File. Are you sure it is a music File?")

        return Song(path, info_dict)

    def update_file(self, song):
        """
        save changes in file
        """
        try:
            audio = mutagen.easyid3.EasyID3(song.raw_path)
        except ID3NoHeaderError:
            audio = mutagen.File(song.raw_path, easy=True)
            audio.add_tags()
        genres = []

        for genre in song.genre:
            genres.append(genre)

        audio["title"] = song.title
        audio["album"] = song.album
        audio["artist"] = song.artist
        audio["genre"] = genres
        audio["discnumber"] = song.cd
        audio["composer"] = song.composer
        audio["tracknumber"] = song.track
        audio["bpm"] = song.bpm
        audio["date"] = song.year
        audio.save()
