from math import sqrt
class Song(object):
    def __init__(self, path, title=None, album=None, interpreter=None, comment=None, cs=0, genres={}, length=None, chance=500, timesplayed=0,  rating=10):
        self.path = path
        self.title = title
        self.album = album
        self.interpreter = interpreter
        self.comment = comment
        self.cs = cs
        self.genres = genres
        self.length = length
        self.chance = chance
        self.timesplayed = timesplayed
        self.rating = rating
        
    def update(self, title, album, interpreter, comment,  cs, rating):
        self.title = title
        self.album = album
        self.interpreter = interpreter
        self.comment = comment
        self.cs = cs
        self.rating = rating
        
    def set_rating(self, rating):
        self.rating = rating
        
    def increasechance(self, count):
        count = float(count)
        count = float(count)
        self.chance += sqrt(self.chance) / count * (self.rating / 10.0)
        if self.chance >= 1:
            self.chance = 1
        
    def decreasechance(self, count):
        count = float(count)
        self.chance -= self.chance * self.chance * count
        if self.chance <= 0:
            self.chance = 0.000000001
        
    def update_timesplayed(self):
        self.timesplayed += 1
        
    def get_chance(self):
        return self.chance
        
    def get_title(self):
        return self.title
        
    def get_album(self):
        return self.album
        
    def get_interpreter(self):
        return self.interpreter
        
    def get_genres(self):
        return self.genres
        
    def get_path(self):
        return self.path
    
    def get_cs(self):
        return self.cs
    
    def genres_add(self, genre):
        self.genres.add(genre)
        
    def genres_del(self,  genre):
        self.genres.remove(genre)
        
    def get_all(self):
        return {'path': self.path, 'title': self.title, 'album': self.album, 'interpreter': self.interpreter, 'comment' : self.comment, 'cs': self.cs, 'genre': self.genres, 'length' : self.length, 'chance' : self.chance, 'timesplayed' : self.timesplayed, 'rating' : self.rating}
