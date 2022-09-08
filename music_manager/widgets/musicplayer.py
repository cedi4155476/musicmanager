import pyglet, time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from random import randint

from exceptions import FileDeletedException
from views.Ui_musicplayer import Ui_music

class MusicPlayer(QDialog, Ui_music):
    """
    music player dialog for listening to the songs
    """

    def __init__(self, widget_handler, config, parent=None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.titlei = -12
        self.albumi = -12
        self.artisti = -12

        self.spinBoxRating.setReadOnly(True)
        self.spinBoxRating.setReadOnly(False)

        self.setFixedSize(self.size())

        self.progress.release_play.connect(self.release_play)
        self.progress.progress_movement.connect(self.progress_movement)

        self.titlescroll = QTimer(parent)
        self.titlescroll.timeout.connect(self.title_timeout)
        self.titlescroll.start(350)

        self.albumscroll = QTimer(parent)
        self.albumscroll.timeout.connect(self.album_timeout)
        self.albumscroll.start(350)

        self.artistscroll = QTimer(parent)
        self.artistscroll.timeout.connect(self.artist_timeout)
        self.artistscroll.start(350)

        self.widget_handler = widget_handler
        self.config = config

        self.songlist = []
        self.index = 0
        self.RANDOMNESS = False
        # Pyglet doesnt like to start at 0 TODO: TEST
        self.START = 0.000001
        self.loop = QTimer()
        self.loop.timeout.connect(self.update_time)
        self.player= pyglet.media.Player()
        self.volume = self.config.get_volume()
        self.musicplayersetslots()

    def save_volume(self):
        """
        Save the used volume
        """
        self.config.save_volume(self.volume)

    def change_volume(self, volume):
        self.volume = volume
        self.player.volume = volume

    def title_timeout(self):
        """
        scrolling for long titles
        """
        if self.scrolltitle.horizontalScrollBar().value() < self.scrolltitle.horizontalScrollBar().maximum() and self.titlei >= 0:
            self.scrolltitle.horizontalScrollBar().setValue(self.scrolltitle.horizontalScrollBar().value()+10)
        elif self.titlei >= 4:
            self.scrolltitle.horizontalScrollBar().setValue(0)
            self.titlei = -8
        else:
            self.titlei += 1

    def album_timeout(self):
        """
        scrolling for long albums
        """
        if self.scrollalbum.horizontalScrollBar().value() < self.scrollalbum.horizontalScrollBar().maximum() and self.albumi >= 0:
            self.scrollalbum.horizontalScrollBar().setValue(self.scrollalbum.horizontalScrollBar().value()+10)
        elif self.albumi >= 4:
            self.scrollalbum.horizontalScrollBar().setValue(0)
            self.albumi = -8
        else:
            self.albumi += 1

    def artist_timeout(self):
        """
        scrolling for long artists
        """
        if self.scrollartist.horizontalScrollBar().value() < self.scrollartist.horizontalScrollBar().maximum() and self.artisti >= 0:
            self.scrollartist.horizontalScrollBar().setValue(self.scrollartist.horizontalScrollBar().value()+10)
        elif self.artisti >= 4:
            self.scrollartist.horizontalScrollBar().setValue(0)
            self.artisti = -8
        else:
            self.artisti += 1

    def set_song_info(self):
        """
        set song info
        """
        m, s = divmod(self.current_song.length, 60)
        length = "/ %02d:%02d" % (m, s)
        range = self.current_song.length*50
        self.title.setText(self.current_song.title)
        self.album.setText(self.current_song.album)
        self.artist.setText(self.current_song.artist)
        self.spinBoxRating.setValue(self.current_song.rating)
        self.progress.setRange(0, range)
        self.length.setText(length)

    def set_volume(self, volume):
        """
        change volume
        """
        self.soundSlider.setValue(volume)

    def update_progress(self, time):
        """
        set progress
        """
        self.progress.setValue(time*50)
        self.widget_handler.GUI.timebar.setValue(int(time*50))
        m, s = divmod(time, 60)
        self.time.setText("%02d:%02d" % (m, s))
        self.widget_handler.GUI.time.setText("%02d:%02d" % (m, s))

    def closeEvent(self, e):
        """
        close window
        """
        e.ignore()
        self.hide()
        self.playerhidden.emit(0)

    def close(self):
        self.pause()
        self.save_volume()

    def player_closed(self, int):
        """
        show dockwidget if music player is hidden and close player if music player is closed
        """
        self.musicdock.setVisible(True)
        self.musicdock.setFloating(False)
        if int == 0:
            self.close_music()

    def close_music(self):
        """
        close music and set it to start position
        """
        if self.player.playing:
            self.pause()
        self.widget_handler.GUI.musicframe.setVisible(False)
        self.current_song = None
        self.player= pyglet.media.Player()
        self.widget_handler.GUI.tray_icon.setIcon(QIcon('resources/trayicon.png'))
        self.widget_handler.PLAYLIST.update_db_playlist()

    @pyqtSlot("bool")
    def on_musicdock_topLevelChanged(self, topLevel):
        """
        hide dockwidget and show music player in dialog
        """
        if topLevel:
            self.musicdock.setVisible(False)
            self.set_volume(self.volume)
            self.showNormal()

    @pyqtSlot()
    def on_dockbutton_clicked(self):
        """
        hide window and show dockwidget as music player
        """
        self.hide()
        self.playerhidden.emit(1)

    @pyqtSlot()
    def on_playbutton_clicked(self):
        """
        send click signal
        """
        self.play()

    @pyqtSlot()
    def on_pausebutton_clicked(self):
        """
        send click signal
        """
        self.pause()

    @pyqtSlot()
    def on_previousbutton_clicked(self):
        """
        send click signal
        """
        self.load_last()

    @pyqtSlot()
    def on_nextbutton_clicked(self):
        """
        send click signal
        """
        self.load_next()

    @pyqtSlot("int")
    def on_spinBoxRating_valueChanged(self, p0):
        """
        send signal when rating is changed
        """
        self.current_song.rating = p0

    @pyqtSlot("int")
    def on_soundSlider_valueChanged(self, value):
        """
        send signal when volume is changed
        """
        self.soundsliderchanged.emit(value)

    def musicplayersetslots(self):
        """
        connect the slots with the musicplayer class
        """
        self.widget_handler.GUI.timebar.release_play.connect(self.release_play)

    def play_clicked(self):
        """
        get clicked signal of dialog
        """
        self.on_playbutton_2_clicked()

    def previous_clicked(self):
        """
        get clicked signal of dialog
        """
        self.on_previousbutton_clicked()

    def sound_slider_changed(self, value):
        """
        get sound changed
        """
        self.on_soundSlider_valueChanged(value)

    def rating_changed(self, rating):
        """
        get rating changed
        """
        self.playlist[self.Ppath].set_rating(rating)

    def time_changed(self, percent):
        """
        send time changed information
        """
        self.progress_movement(percent)
        self.update_progress(int(self.player.time))

    def release_play(self):
        """
        release mouse after changing time in time bar
        """
        if not self.player.playing:
            self.play()

    def progress_movement(self, percent):
        """
        change time bar position
        """
        if self.player.playing:
            self.pause()
        if not percent:
            percent = 0.00001
        self.player.seek(percent * self.current_song.length)
        self.update_progress(self.player.time)

    def play(self):
        """
        change the tray icon and start playing
        """
        self.widget_handler.GUI.tray_icon.setIcon(QIcon('resources/trayiconplay.png'))
        self.player.play()

    def pause(self):
        """
        change the tray icon and pause the player
        """
        self.widget_handler.GUI.tray_icon.setIcon(QIcon('resources/trayiconpause.png'))
        self.player.pause()

    def play_pause_button_clicked(self):
        if self.player.playing:
            self.pause()
            self.widget_handler.GUI.playpausebutton.setIcon(QIcon('resources/play.png'))
        else:
            self.play()
            self.widget_handler.GUI.playpausebutton.setIcon(QIcon('resources/pause.png'))

    def play_next_song(self):
        """
        wait for loading and then start next song
        """
        time.sleep(0.2)
        self.player.next_source()

    def play_selected_song(self):
        """
        play selected song in normal mode
        """
        if self.RANDOMNESS:
            self.widget_handler.GUI.musicframe.setVisible(False)
            self.player = pyglet.media.Player()
            self.RANDOMNESS = False
        if not self.widget_handler.PLAYLIST.playlist:
            return
        # self.playlistTab.setCurrentIndex(1)
        try:
            if not self.widget_handler.GUI.musicframe.isVisible():
                self.widget_handler.GUI.musicframe.setVisible(True)
                self.start_loop()
            self.index = self.widget_handler.GUI.playlistWidget.currentRow()
            self.current_song = self.widget_handler.PLAYLIST.get_song_with_index(self.index)
            source = pyglet.media.load(self.current_song.raw_path)
            self.player.queue(source)
            self.get_infos()
            if self.player.playing:
                self.play_next_song()
            else:
                self.play()
            self.widget_handler.GUI.playpausebutton.setIcon(QIcon('resources/pause.png'))
        except FileDeletedException:
            self.widget_handler.GUI.musicframe.setVisible(False)
            return

    def load_next(self):
        try:
            if self.RANDOMNESS:
                if self.index >= len(self.songlist) -1:
                    self.load_next_random_song()
                else:
                    self.get_next_songlist_song()
            else:
                self.load_next_normal_song()
        except FileDeletedException:
            self.load_next()
            return
        self.play_next_song()

    def get_next_songlist_song(self):
        """
        get the next song in random mode after it went back so it will have a structur
        """
        self.index += 1
        self.current_song = self.songlist[self.index]
        if not self.current_song.path.exists():
            self.current_song.disable()
            self.widget_handler.PLAYLIST.disable_row(self.current_song)
            raise FileDeletedException
        source = pyglet.media.load(self.current_song.raw_path)
        self.player.queue(source)
        self.get_infos()

    def load_next_normal_song(self):
        """
        get next song in normal mode
        """
        if self.index == len(self.widget_handler.PLAYLIST.playlist) -1:
            self.index = 0
        else:
            self.index += 1
        self.current_song = self.widget_handler.PLAYLIST.get_song_with_index(self.index)
        self.widget_handler.GUI.playlistWidget.setCurrentCell(self.index, 1)
        source = pyglet.media.load(self.current_song.raw_path)
        self.player.queue(source)
        self.get_infos()

    def load_next_random_song(self):
        song = self.widget_handler.PLAYLIST.get_next_random_song()
        self.index = len(self.songlist)
        self.songlist.append(song)
        source= pyglet.media.load(song.raw_path)
        self.player.queue(source)

    def load_last(self):
        """
        play last song
        """
        if self.player.time > 3:
            self.player.seek(self.START)
            return

        try:
            if self.RANDOMNESS:
                if self.index <= 0: #  Its not possible to go back before the first song
                    self.player.seek(self.START)
                elif self.index > 0:
                    self.load_last_random_song()
            else:
                self.load_last_normal_song()
        except FileDeletedException:
            self.load_last()
            return
        self.play_next_song()

    def load_last_normal_song(self):
        """
        get last song in normal mode
        """
        if self.index <= 0:
            self.index = self.widget_handler.GUI.playlistWidget.rowCount()-1
        else:
            self.index -= 1
        self.current_song = self.widget_handler.PLAYLIST.get_song_with_index(self.index)
        self.widget_handler.GUI.playlistWidget.setCurrentCell(self.index, 1)
        source = pyglet.media.load(self.current_song.raw_path)
        self.player.queue(source)
        self.get_infos()

    def load_last_random_song(self):
        """
        get the last song played in random mode
        """
        self.index -= 1
        self.current_song = self.songlist[self.index]

        if not self.current_song.path.exists():
            self.current_song.disable()
            self.widget_handler.PLAYLIST.disable_row(self.current_song)
            raise FileDeletedException
        source = pyglet.media.load(self.current_song.raw_path)
        self.player.queue(source)
        self.get_infos()

    def start_random_play(self):
        """
        start playing in random mode
        """
        if not self.playlist:
            return
        if not self.widget_handler.GUI.musicframe.isVisible():
            self.widget_handler.GUI.musicframe.setVisible(True)
        self.RANDOMNESS = True
        self.songlist = []
        self.index = 0
        self.start_loop()
        self.load_next_random_song()

        self.get_infos()
        if self.player.source:
            self.play_next_song()
        self.play()
        self.player.volume = self.volume
        self.soundSlider.setValue(self.volume)
        self.soundSlider.setSliderPosition(self.volume)

    def get_infos(self):
        """
        get song information and set them in the player
        """
        item = self.widget_handler.PLAYLIST.get_playlist_item(self.current_song)
        scroll = self.widget_handler.GUI.playlistWidget.item(item.row(), 1)
        self.widget_handler.GUI.playlistWidget.setCurrentItem(item)
        self.widget_handler.GUI.playlistWidget.scrollToItem(scroll)
        self.widget_handler.GUI.playlistWidget.update()
        self.widget_handler.GUI.timebar.setRange(0, self.current_song.length*50)

        m, s = divmod(self.current_song.length, 60)
        self.widget_handler.GUI.length.setText("/ %02d:%02d" % (m, s))

        self.widget_handler.GUI.timebar.setValue(0)
        self.widget_handler.GUI.time.setText("%02d:%02d" % (0, 0))
        self.set_song_info()
        self.player.seek(self.START)

    def stop_loop(self):
        self.loop.stop()

    def start_loop(self):
        self.loop.start(100)

    def update_time(self):
        """
        update the time in the progress bar
        """
        if self.player.playing:
            self.update_progress(self.player.time)
            if int(self.player.time) >= self.current_song.length:
                self.playlist[self.Ppath].update_timesplayed()
                self.player.seek(self.START)
                self.on_nextbutton_clicked()
