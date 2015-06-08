import sqlite3
conn = sqlite3.connect('music.db') 

c = conn.cursor()

for line in open('dbcreate.sql'):
    c.execute(line)

conn.close()
