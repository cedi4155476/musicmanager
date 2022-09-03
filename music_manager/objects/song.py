from math import sqrt
class Song(object):
    """
    holds all song object for the programm
    """    
    mapping = {
        1:10,
        2:11,
        3:13,
        4:16,
        5:20,
        6:25,
        7:31,
        8:38,
        9:46,
        10:55,
        11:65,
        12:76,
        13:88,
        14:101,
        15:115,
        16:130,
        17:146,
        18:200,
        19:240,
        20:350,
    }

    def __init__(self, path, info):
        self.path = path
        self.raw_path = str(path.resolve())
        self.title = info.get("title")
        self.album = info.get("album")
        self.interpreter = info.get("interpreter")
        self.comment = info.get("comment")
        self.genres = info.get("genres", [])
        self.length = info.get("length")
        self.chance = info.get("chance", 0)
        self.times_played = info.get("times_played", 0)
        self.rating = info.get("rating", 20)
        self.cd = info.get("cd")
        self.track = info.get("track")
        self.bpm = info.get("bpm")
        self.composer = info.get("composer")
        self.year = info.get("year")
        
    def __eq__(self, other):
        return_value = True 
        if not isinstance(other, Song):
            return False
        return_value = self.path == other.path and return_value
        return_value = self.title == other.title and return_value
        return_value = self.album == other.album and return_value
        return_value = self.interpreter == other.interpreter and return_value
        return_value = self.comment == other.comment and return_value
        return_value = self.genres == other.genres and return_value
        return_value = self.length == other.length and return_value
        return_value = self.cd == other.cd and return_value
        return_value = self.track == other.track and return_value
        return_value = self.bpm == other.bpm and return_value
        return_value = self.composer == other.composer and return_value
        return_value = self.year == other.year and return_value

        return return_value

    def update_from_database(self, info):
        self.genres = info.genres
        self.chance = info.chance
        self.times_played = info.times_played
        self.rating = info.rating

    def update(self, title, album, interpreter, comment, rating):
        self.title = title
        self.album = album
        self.interpreter = interpreter
        self.comment = comment
        self.rating = rating

    def updateInfos(self, track, cd, bpm, title, interpreter, composer, album, year, comment):
        self.title = title
        self.album = album
        self.interpreter = interpreter
        self.comment = comment
        self.cd = cd
        self.track = track
        self.bpm = bpm
        self.composer = composer
        self.year = year

    def set_rating(self, rating):
        self.rating = rating

    def increasechance(self, amount_songs):
        self.chance += int(pow(self.mapping[self.rating],2)) + amount_songs

    def decreasechance(self, count):
        self.chance = 0

    def update_times_played(self):
        self.times_played += 1

    def get_chance(self):
        return self.chance

    def get_title(self):
        return self.title

    def get_album(self):
        return self.album

    def get_interpreter(self):
        return self.interpreter

    def get_composer(self):
        return self.composer

    def get_genres(self):
        return self.genres

    def get_path(self):
        return self.path

    def add_genre(self, genre):
        self.genres.append(genre)

    def remove_genre(self,  genre):
        self.genres.remove(genre)

    def get_all(self):
        return {'path': self.path, 'title': self.title, 'album': self.album, 'interpreter': self.interpreter, 
                'comment' : self.comment, 'genre': self.genres, 'length' : self.length, 'chance' : self.chance,
                'times_played' : self.times_played, 'rating' : self.rating, 'track' : self.track, 'cd' : self.cd,
                'bpm' : self.bpm, 'composer' : self.composer, 'year' : self.year}
