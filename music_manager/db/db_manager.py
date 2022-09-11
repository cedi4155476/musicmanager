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
            self.c.execute('SELECT song_id FROM song')
        except sqlite3.OperationalError:
            for line in open("db/"+'dbcreate.sql'):
                try:
                    self.c.execute(line)
                except sqlite3.OperationalError as e:
                    break
    
    def __del__(self):
        self.commit()
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

    def get_song(self, path):
        """
        get all infos from database for defined path
        """
        self.c.execute('''SELECT song.song_id as song_id, song.title as title, song.album as album, song.comment as comment,  genre.genre_name as genre, artist.artist_name as artist,
                                                song.length as length, song.times_played as times_played, song.rating as rating, song.bpm as bpm, song.year as year,
                                                song.track as track, composer.composer_name as composer, song.cd as cd
                                    FROM song
                                    LEFT OUTER JOIN song_genre
                                        ON song.song_id = song_genre.song_id
                                    LEFT OUTER JOIN genre
                                        ON song_genre.genre_id = genre.genre_id
                                    LEFT OUTER JOIN artist
                                        ON song.artist_fk = artist.artist_id
                                    LEFT OUTER JOIN composer
                                        ON song.composer_fk = composer.composer_id
                                        WHERE song.song_path = ?''',  (path, ))
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
        artist_id = self.get_or_create_artist_composer('artist', song.artist)["id"]
        composer_id = self.get_or_create_artist_composer('composer', song.composer)["id"]
        inserts = (song.raw_path, song.title, song.album, song.comment, song.length, song.times_played, song.rating, song.year, composer_id, artist_id, song.bpm, song.track, song.cd)
        self.c.execute('INSERT INTO song VALUES(Null,?,?,?,?,?,?,?,?,?,?,?,?,?)', inserts)
        song.song_id = self.c.lastrowid
        self.add_genres(song, song.genres)
    
    def update_song(self, song):
        artist_id = self.get_or_create_artist_composer('artist', song.artist)["id"]
        composer_id = self.get_or_create_artist_composer('composer', song.composer)["id"]
        inserts = (song.title, song.album, artist_id, composer_id, song.comment, song.times_played, song.rating, song.song_id)
        self.c.execute('UPDATE song SET title=?, album=?, artist_fk=?, composer_fk=?, comment=?, times_played=?, rating=? WHERE song_id=?', inserts)

    def update_songs(self, song_dict):
        """
        save all changes of a dict of songs
        """
        for song in song_dict.values():
            self.update_song(song)
        self.commit()

    def update_playlist(self, playlist, playlist_id, playlist_name, amount_played):
        """
        save all playlist changes in db
        """
        for song in playlist.values():
            self.update_song(song)
            self.c.execute("UPDATE song_playlist SET times_played=?, chance=? WHERE song_id=? AND playlist_id=?",(song.playlist_played, song.playlist_chance, song.song_id, playlist_id))
        
        self.c.execute("UPDATE playlist SET amount_played=?, playlist_name=? WHERE playlist_id=?",(amount_played, playlist_name, playlist_id))
        self.commit()

    def create_playlist(self, playlist, playlist_name, amount_played, playlist_section):
        self.c.execute("INSERT INTO playlist VALUES(NULL,?,?,?)",(playlist_name, amount_played, playlist_section))
        playlist_id = self.c.lastrowid
        for song in playlist.values():
            self.c.execute("INSERT INTO song_playlist VALUES(?,?,?,?)",(song.song_id, playlist_id, song.playlist_played, song.playlist_chance))
        self.commit()

    def delete_playlist(self, playlist_id):
        self.c.execute("DELETE FROM song_playlist where playlist_id=?",(playlist_id,))
        self.c.execute("DELETE FROM playlist where playlist_id=?",(playlist_id, ))

    def create_playlist_section(self, section_name, parent):
        self.c.execute("INSERT INTO playlist_section VALUES (NULL,?,?)", (section_name, parent))
        self.commit()
        return self.c.lastrowid

    def delete_playlist_section(self, section_id):
        child_sections = self.get_all_section_in_section(section_id)
        for section in child_sections:
            self.delete_playlist_section(section["playlist_section_id"])
        playlists = self.get_all_playlists_in_section(section_id)
        for playlist in playlists:
            self.delete_playlist(playlist["playlist_id"])
        self.c.execute("DELETE FROM playlist_section where playlist_section_id=?",(section_id,))

    def get_all_sections(self):
        self.c.execute("SELECT playlist_section_id, section_name, parent from playlist_section ORDER BY playlist_section_id asc")
        return self.c.fetchall()

    def get_all_section_in_section(self, section_id):
        self.c.execute("SELECT playlist_section_id, section_name, parent from playlist_section where parent=?", (section_id,))
        return self.c.fetchall()

    def get_all_playlists(self):
        self.c.execute("SELECT playlist_id, playlist_name, playlist_section_fk from playlist")
        return self.c.fetchall()

    def get_all_playlists_in_section(self, section_id):
        self.c.execute("SELECT playlist_id, playlist_name, playlist_section_fk from playlist where playlist_section_fk=?", (section_id, ))
        return self.c.fetchall()

    def get_playlist_by_name(self, name, section):
        self.c.execute("SELECT playlist_id, playlist_name, playlist_section_fk from playlist where playlist_name=? and playlist_section_fk=?",(name, section))
        return self.c.fetchone()

    def get_all_songs_from_playlist(self, playlist_id):
        self.c.execute("SELECT song_id, times_played, chance from song_playlist where playlist_id=?",(playlist_id, ))
        return self.c.fetchall()

    def get_or_create_artist_composer(self, type, value):
        '''
        get artist or composer or create it if not exists
        '''
        select_statement = f"{type}_id as id, {type}_name as name"
        name = type + "_name"
        self.c.execute('SELECT {select} FROM {table_name} WHERE {name}=?'.format(select=select_statement, table_name=type, name=name), (value, ))
        result = self.c.fetchone()
        if result:
            return result
        self.c.execute('INSERT INTO {tb} VALUES(?,?)'.format(tb=type), (None, value))
        return {"id": self.c.lastrowid, "name": value}

    def get_artist_composer_with_id(self, type, value):
        '''
        get information of artist or composer
        '''
        select_statement = f"{type}_id as id, {type}_name as name"
        name = type + "_id"
        self.c.execute('SELECT {select} FROM {table_name} WHERE {name}=?'.format(select=select_statement, table_name=type, name=name), (value, ))
        return self.c.fetchone()

    def get_all_genres(self):
        """
        Get all Genres from all Songs
        """
        self.c.execute('SELECT genre_name as genre FROM genre')
        return self.c.fetchall()

    def get_all_genres_of_song(self, song):
        """
        get all genres of editing song
        """
        self.c.execute('''SELECT genre.genre_id as id, genre.genre_name as genre FROM genre 
                                                JOIN song_genre 
                                                    ON genre.genre_id = song_genre.genre_id 
                                                    WHERE song_genre.song_id = ?''', (song.song_id, ))
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
    
    def remove_genre(self, genre_text, song):
        """
        Remove a genre from a song and completely if none are left
        """
        self.c.execute('SELECT genre_id FROM genre WHERE genre_name = ?',  (genre_text, ))
        self.c.execute('DELETE FROM song_genre WHERE song_id = ? AND genre_id = ?', (song.song_id, self.c.fetchone()['genre_id']))
        if genre_text == "empty":
            return True
        genre_needed = self.is_genre_needed(genre_text)
        if not genre_needed:
            self.c.execute('DELETE FROM genre WHERE genre_name = ?', (genre_text, ))
        return genre_needed

    def add_genres(self, song, genres):
        """
        go through all genres in a file and add them to the db
        """
        for genre in genres:
            self.add_genre_to_song(song, genre)

    def add_genre_to_song(self, song, genre_name):
        """
        make the connections between song and genre or if it does not exist add the genre to the db and then make connection
        """
        genre_id = self.get_or_create_genre(genre_name)["genre_id"]

        self.get_or_create_genre_song_connection(song, genre_id)

    def get_or_create_genre_song_connection(self, song, genre_id):
        """
        return genre_song connection or create if not exists
        """
        self.c.execute('SELECT song_id, genre_id FROM song_genre WHERE song_id=? AND genre_id=?', (song.song_id, genre_id))
        result = self.c.fetchone()
        if result:
            return result

        self.c.execute("INSERT INTO song_genre VALUES (?,?)", (song.song_id, genre_id))
        return {"song_id": song.song_id, "genre_id": genre_id}

    def get_or_create_genre(self, genre_name):
        """
        return genre from name and create if not exists
        """
        self.c.execute("SELECT genre_id, genre_name FROM genre WHERE genre_name = ?", (genre_name, ))
        result = self.c.fetchone()
        if result:
            return result
        self.c.execute("INSERT INTO genre VALUES (?,?)", (None, genre_name))
        return {"genre_id": self.c.lastrowid, "genre_name": genre_name}
