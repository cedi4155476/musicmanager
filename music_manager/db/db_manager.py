import sqlite3, os
from utils import HOME
from widgets import genre

class DBManager:

    def __init__(self):
        """
        connect to the db and if it did not exist make the db and it's tables
        """
        self.conn = sqlite3.connect(HOME +'music.db')
        self.conn.row_factory = self.dict_factory
        self.c = self.conn.cursor()
        try:
            self.c.execute('SELECT path FROM song')
        except sqlite3.OperationalError:
            for line in open("db/"+'dbcreate.sql'):
                try:
                    self.c.execute(line)
                except sqlite3.OperationalError as e:
                    break
    
    def __del__(self):
        self.conn.commit()
        self.c.close()
        self.conn.close()

    def dict_factory(self, cursor, row):
        """
        make it easier to read from db
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def commit(self):
        self.conn.commit()

    def get_all_genres(self):
        """
        Get all Genres from all Songs
        """
        self.c.execute('SELECT genre_name as genre FROM genre')
        return self.c.fetchall()

    def get_all_genres_of_song(self, path):
        """
        get all genres of editing song
        """
        self.c.execute('''SELECT genre.genre_name as genre, genre.genre_id as id FROM genre 
                                                JOIN song_genre 
                                                    ON genre.genre_id = song_genre.genre_id 
                                                    WHERE song_genre.song_path = ?''', (path, ))
        return self.c.fetchall()

    def is_genre_needed(self, genre):
        """
        checks if genre is needed anymore
        """
        self.c.execute('SELECT * FROM genre JOIN song_genre ON song_genre.genre_id = genre.genre_id WHERE genre.genre_name = ?', (genre, ))
        if self.c.fetchone():
            return True
        else:
            return False
    
    def remove_genre(self, genre_text):
        """
        Remove a genre from a song and completely if none are left
        """
        self.c.execute('SELECT genre_id FROM genre WHERE genre_name = ?',  (genre_text, ))
        delgenreid = self.c.fetchone()['genre_id']
        delete = (self.path, delgenreid)
        self.c.execute('DELETE FROM song_genre WHERE song_path = ? AND genre_id = ?',  delete)
        genre_needed = self.is_genre_needed(genre_text)
        if not genre_needed:
            self.c.execute('DELETE FROM genre WHERE genre_name = ?', (genre_text, ))
        return genre_needed

    def give_empty_genre(self, path):
        """
        If there are no genres left, it need an empty genre
        """
        self.c.execute('''SELECT genre_id from genre WHERE genre_name = "empty" ''')
        genre_id = self.c.fetchone()['genre_id']
        inserts = (path, genre_id)
        self.c.execute('INSERT INTO song_genre VALUES(?,?)', inserts)

    def get_song(self, path):
        """
        get all infos from database for defined path
        """
        self.c.execute('''SELECT song.title as title, song.album as album, song.comment as comment,  genre.genre_name as genre, interpreter.interpreter_name as interpreter,
                                                song.length as length, song.times_played as times_played, song.rating as rating, song.bpm as bpm, song.year as year,
                                                song.track as track, composer.composer_name as composer, song.cd as cd
                                    FROM song
                                    LEFT OUTER JOIN song_genre
                                        ON song.path = song_genre.song_path
                                    LEFT OUTER JOIN genre
                                        ON song_genre.genre_id = genre.genre_id
                                    LEFT OUTER JOIN interpreter
                                        ON song.interpreter_fk = interpreter.interpreter_id
                                    LEFT OUTER JOIN composer
                                        ON song.composer_fk = composer.composer_id
                                        WHERE song.path = ?''',  (path, ))
        datas = self.c.fetchall()
        if not datas:
            return {}
        i = 0
        genre = []
        for d in datas:
            if i == 0:
                data = d
                genre.append(d['genre'])
            else:
                genre.append(d['genre'])
            i +=1
        data["genres"] = genre
        return data
    
    def add_song(self, song):
        """
        add song to db
        """
        interpreter_id = self.get_or_create_interpreter_composer('interpreter', song.interpreter)["id"]
        composer_id = self.get_or_create_interpreter_composer('composer', song.composer)["id"]
        inserts = (song.raw_path, song.title, song.album, song.comment, song.length, song.times_played, song.rating, song.year, composer_id, interpreter_id, song.bpm, song.track, song.cd)
        self.c.execute('INSERT INTO song VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', inserts)
        self.add_genres(song.raw_path, song.genres)
    
    def update_song(self, song):
        interpreter_id = self.get_or_create_interpreter_composer('interpreter', song.interpreter)["id"]
        composer_id = self.get_or_create_interpreter_composer('composer', song.composer)["id"]
        inserts = (song.title, song.album, interpreter_id, composer_id, song.raw_path)
        self.c.execute('UPDATE song SET title=?, album=?, interpreter_fk=?, composer_fk=? WHERE path=?', inserts)

    def get_or_create_interpreter_composer(self, type, value):
        '''
        add AIC to db
        '''
        select_statement = f"{type}_id as id, {type}_name as name"
        name = type + "_name"
        self.c.execute('SELECT {select} FROM {table_name} WHERE {name}=?'.format(select=select_statement, table_name=type, name=name), (value, ))
        result = self.c.fetchone()
        if result:
            return result
        ex = (None, value)
        self.c.execute('INSERT INTO {tb} VALUES(?,?)'.format(tb=type), ex)
        return {"id": self.c.lastrowid, "name": value}

    def get_interpreter_composer_with_id(self, type, value):
        '''
        get information of interpreter or composer
        '''
        select_statement = f"{type}_id as id, {type}_name as name"
        name = type + "_id"
        self.c.execute('SELECT {select} FROM {table_name} WHERE {name}=?'.format(select=select_statement, table_name=type, name=name), (value, ))
        return self.c.fetchone()

    def add_genres(self, path, genres):
        """
        go through all genres in a file and add them to the db
        """
        for genre in genres:
            self.add_genre_to_song(path, genre)

    def add_genre_to_song(self, path, genre_name):
        """
        make the connections between song and genre or if it does not exist add the genre to the db and then make connection
        """
        genre_id = self.get_or_create_genre(genre_name)["genre_id"]

        self.get_or_create_genre_song_connection(path, genre_id)

    def get_or_create_genre_song_connection(self, path, genre_id):
        """
        return genre_song connection or create if not exists
        """
        tests = [path, genre_id]
        self.c.execute('SELECT song_path, genre_id FROM song_genre WHERE song_path=? AND genre_id=?', tests)
        result = self.c.fetchone()
        if result:
            return result
        
        insert = (path, genre_id)
        self.c.execute("INSERT INTO song_genre VALUES (?,?)", insert)
        return {"song_path": path, "genre_id": genre_id}

    def get_or_create_genre(self, genre_name):
        """
        return genre from name and create if not exists
        """
        self.c.execute("SELECT genre_id, genre_name FROM genre WHERE genre_name = ?", (genre_name, ))
        result = self.c.fetchone()
        if result:
            return result
        gen = (None, genre_name)
        self.c.execute("INSERT INTO genre VALUES (?,?)", gen)
        return {"genre_id": self.c.lastrowid, "genre_name": genre_name}