import sqlite3
conn = sqlite3.connect('music.db') 

c = conn.cursor()

for line in open('dbcreate.sql'):
    try:
        c.execute(line)
    except sqlite3.OperationalError:
        break

conn.close()
