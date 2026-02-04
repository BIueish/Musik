<h1>Musik</h1>
A simple command line music player for Windows, Mac and Linux.

<h3>Features</h3>
- Play MP3, WAV or OGG music files
- Quickly access songs if needed by an index rather than name
- Create and edit custom albums
- Superfast song loading and playing
- And other standard features...

<h3>Running</h3>
As of now, Musik is only available as source code, and you'll need Python 3 to run it.

The only dependency is pygame.

Simply download `musik.py` and then install the pygame library using `python3
-m pip install pygame-ce` or just `pip3 install pygame-ce`

Musik can then be run by Python normally.

<h3>Commands</h3>
All commands and extensive help can be viewed inside Musik by entering 

`h` or `help`.

- `quit`, `exit`, `esc` - Quits Musik
- `p`, `play` + name of song - Play specified song if in library or play all songs of specified artist or search albums
- `pause`, press ENTER - Pause current music
- `unpause`, press ENTER, `resume`, `continue` - Unpause current music
- `stop` - Stop all music and clear queue 
- `q`, `queue` + name of song - Add specified song or artist to queue if in library or search albums 
- `v`, `volume` + volume - Change volume to specified number (between 0-100) 
- `l`, `list`, `library` - View all songs in your library by number 
- `playlist`, `pl` + number - Play a song from your library by number or play the first song and add the entire library to the queue if not specified 
- `playlistq`, `plq` + number - Queue a song from your library by number or queue the entire library if not specified 
- `n`, `next`, `skip` - Move to the next song in queue, if any 
- `refresh` - Refresh your library to check for new arrivals 
- `loop`, `repeat`, `r` - Loop/Unloop the current song 
- `loop queue`, `loopq`, `loop q` - Loop/Unloop the current song and queue 
- `random`, `shuffle`, `s` - Shuffle the queue 
- `c`, `clear` - Clear the queue 
- `t`, `time`, `length` - Get the current position in the song and total length of the song 
- `t`, `time`, `length` + (value in seconds) - Jump to the point in the song given by the specified value 
- `t`, `time`, `length` + (hours:minutes:seconds) - Jump to the specified time, (seperated by commas, periods, colons, semi-colons or back or forward slashes) 
- `artist`, `current` - View information about the current song 
- `ca`, `calbum`, `create album` + name - Create a new album with the specified name
- `da`, `dalbum`, `delete album` + name - Delete specified album 
- `pa`, `palbum`, `play album` + name - Play specified album 
- `qa`, `qalbum`, `queue album` + name - Queue specified album 
- `a`, `albums`, `album` + name - View contents of specified album or view all albums if not specified 
- `ea`, `ealubm`, `edit album` + name - Add and remove songs from specified album 
- `h`, `help` - Open Musik Help
            
<h3>Adding songs</h3>
    Songs are not provided and you will have to download them yourself (the song needs to be in the MP3, WAV or OGG formats)
    Once you have the file, simply move or copy the song into the Musik Songs folder then ensure the name is in lower case, and you're good to go!
(The help inside the Musik app gives the exact path of the Songs folder)

<h3>Bugs/Errors</h3>
    Please open an issue or contact me if you can for any bugs or errors you encounter.
    

<h3>Sample Usage</h3>
Here is a sample of what using Musik looks like

```
-- Musik Console Player --
Welcome to Musik!
Working v3.1
> v 60
Volume set to 60
> p the sound of the shire
Playing the sound of the shire
> plq
Adding library to queue
> shuffle
Shuffled queue
> n
Playing clair de lune
> 
Paused
> 
Unpaused
> stop
Stopped music
> pa minecraft
Playing album "minecraft"
>
Playing sweden
> q
Your queue
    clark
    aria math
    minecraft
    wet hands
    biome fest
> quit
```

Musik is made by Blueish
