BEGIN TRANSACTION;
CREATE TABLE genre (genre_ID INTEGER PRIMARY KEY, genre_name TEXT);
INSERT INTO genre VALUES(1,'empty');
CREATE TABLE interpreter (interpreter_ID INTEGER PRIMARY KEY, interpreter_name TEXT);
CREATE TABLE music (path TEXT, title TEXT, album TEXT, interpreter_FK NUMERIC, comment TEXT, cs NUMERIC, length NUMERIC, chance NUMERIC, times_played NUMERIC, rating NUMERIC);
CREATE TABLE music_genre (music_path TEXT, genre_ID NUMERIC);
CREATE TABLE volume (volume_ID INTEGER PRIMARY KEY, volume NUMERIC);
INSERT INTO volume VALUES(1,1);
COMMIT;
