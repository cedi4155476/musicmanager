CREATE TABLE albuminterpreter (albuminterpreter_ID INTEGER PRIMARY KEY, albuminterpreter_name TEXT);
CREATE TABLE composer (composer_ID INTEGER PRIMARY KEY, composer_name TEXT);
CREATE TABLE genre (genre_ID INTEGER PRIMARY KEY, genre_name TEXT);
INSERT INTO genre VALUES(1,'empty');
CREATE TABLE interpreter (interpreter_ID INTEGER PRIMARY KEY, interpreter_name TEXT);
CREATE TABLE music (path TEXT, title TEXT, album TEXT, interpreter_FK NUMERIC, comment TEXT, cs NUMERIC, length NUMERIC, chance NUMERIC, times_played NUMERIC, rating NUMERIC, year TEXT, albuminterpreter_FK NUMERIC, composer_FK NUMERIC, bpm NUMERIC, track TEXT, cd TEXT);
CREATE TABLE music_genre (music_path TEXT, genre_ID NUMERIC);
