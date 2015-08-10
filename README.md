# Music Manager
## Introduction

This programm is for people who likes to hear music in a random loop so that one song will not appear after it has already been played but maybe will show up again before the whole list is finished. It is simply random.
## Note

This programm is not finished, so there will be some errors and it needs a lot more testing before it works like it should.
Some Files are crashing the programm it is still unclear why this is happening but it should be fixed in the future.
## Install with apt-get

You'll need to install avbin to listen to music so just do:
<pre>
sudo apt-get install libavbin-dev
</pre>

First you need my launchpad Repository for downloading this package.
<pre>
sudo add-apt-repository ppa:cedric-christen/musicmanager
</pre>
Then update your apt-get
<pre>
sudo apt-get update
</pre>
Finally install the package.
<pre>
sudo apt-get install python-music-manager
</pre>

Use the program with.
<pre>
music_manager
</pre>
There will be a music_manager directory in your home/documents folder with the playlists, database and error.log file.

## Bug reports

Please use the "issues" tool of GitHub to report bugs and errors.
## Main Goal

My main goal is that everyone can hear music edit the metadata of the songs in one programm and also save the playlists position and chance rate so you will not have the same song again if you restart the programm or computer.
