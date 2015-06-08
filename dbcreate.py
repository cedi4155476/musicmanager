import sqlite3
conn = sqlite3.connect('music.db') 

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS music (path text, title text, album text, interpret_FK Integer)''')

c.execute('''CREATE TABLE IF NOT EXISTS interpret (interpret_ID Integer, name text)''')

c.execute('''CREATE TABLE IF NOT EXISTS genre(id Integer, genre text)''')

c.execute('''CREATE TABLE IF NOT EXISTS music_genre(path_music text, id_genre Integer)''')


c.execute('''INSERT INTO genre VALUES (1, "Rock")''')

c.execute('''INSERT INTO music_genre VALUES ("/home/cch/Documents/python/music manager/files/My soul Your Beat's", 1)''')

conn.commit()

conn.close()