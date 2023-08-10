from __future__ import unicode_literals
import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import json
import pygame
from pygame import mixer
from pygame.locals import *
import threading
import random, copy
from subprocess import Popen
from io import StringIO

print("-- Musik Console Player --")
print("Welcome to Musik!")
print("Working v3.1")

# TODO: 4.0- mac and windows executables, GUI, file conversion to mp3

paused = False
volume = 100
clock = pygame.time.Clock()
queue = []
playlist = []
history = []
discord = False
current = None
loop = False
loopq = False
quit = False
length = 0
prev_length = 0
lengthProc = None
home_path = os.path.expanduser("~")
artists_path = os.path.join(home_path, "Musik", "artists.json")
albums_path = os.path.join(home_path, "Musik", "albums.json")
song_path = os.path.join(home_path, "Musik", "Songs")
length_path = os.path.join(home_path, "Musik", "length.txt")
mlength = """import pygame, sys, time
t = time.time()
pygame.mixer.init()
length = pygame.mixer.Sound(sys.argv[1]).get_length()
file = open(sys.argv[2], "r")
lines = file.read()
if len(lines) == 0 or float(lines.split("/")[0]) < t:
    file.close()
    file = open(sys.argv[2], "w")
    file.write(str(t)+"/"+str(length))
file.close()
pygame.mixer.quit()"""


try:
    file = open(artists_path, "r")
    artists = json.load(file)
    file.close()
    file = open(albums_path, "r")
    albums = json.load(file)
    file.close()
except FileNotFoundError:
    os.mkdir(os.path.join(home_path, "Musik"))
    os.mkdir(song_path)
    file = open(artists_path, "w")
    file.write("{}")
    file.close()
    artists = {}
    file = open(albums_path, "w")
    file.write("{}")
    file.close()
    albums = {}
    file = open(length_path, "w")
    file.close()

try:
    file = open(os.path.join(home_path, "Musik", "mlength.py"), "r")
    file.close()
except FileNotFoundError:
    file = open(os.path.join(home_path, "Musik", "mlength.py"), "w")
    file.write(mlength)
    file.close()


class InputThread(threading.Thread):

    def __init__(self, input_func=None, name='musik-input'):
        self.input_func = input_func
        super(InputThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            self.input_func(input("> "))  # waits to get input + Return


def commandParser(command):
    global current, paused, volume, queue, quit, playlist, history, loop, instance, discord, loopq, prev_length
    history.append(command)
    commandlower = command.lower()
    commandlowerf = commandlower.split(" ")[0]
    if commandlowerf in ["quit", "exit", "esc"]:
        pygame.mixer.music.stop()
        quit = True
        file = open(artists_path, "w")
        json.dump(artists, file)
        file.close()
        file = open(albums_path, "w")
        json.dump(albums, file)
        file.close()
        exit(0)
    elif commandlowerf == "stop":
        pygame.mixer.music.stop()
        current = None
        queue = []
        print("Stopped music")
    elif commandlowerf == "pause" or commandlowerf == "":
        if not paused:
            pygame.mixer.music.pause()
            paused = True
            print("Paused")
        else:
            pygame.mixer.music.unpause()
            paused = False
            print("Unpaused")
    elif commandlowerf in ["resume", "continue", "unpause"] and paused:
        pygame.mixer.music.unpause()
        paused = False
        print("Unpaused")
    elif "volume" == commandlowerf or "v" == commandlowerf:
        if " " in commandlower:
            volume = int(commandlower.split(" ")[-1])
            mixer.music.set_volume(volume / 100.0)
            print(f"Volume set to {volume}")
        else:
            print(f"Volume is {volume}")
    elif "p" == commandlowerf or "play" == commandlowerf:
        if " " in commandlower:
            musicWords = commandlower.split(" ")[1:]
            music = ""
            for i in musicWords:
                music += i
                music += " "
            mixer.music.unload()
            music = music[:-1]
            if music in playlist:
                print(f"Playing {music}")
                openMusic(music)
                paused = False
            else:
                songs = []
                for i in artists:
                    if music in artists[i].lower():
                        songs.append(i)
                if len(songs) == 0:
                    print(f"Track or Artist {music} not found. Searching Albums...")
                    commandParser(f"_pa {music}")
                else:
                    name = songs[0]
                    queue = songs[1:] + queue
                    openMusic(name)
                    print(f"Playing artist {wordCapitalize(music)}")
        else:
            print(f"Currently playing: {current}")
    elif "_p" == commandlowerf:
        if " " in commandlower:
            musicWords = commandlower.split(" ")[1:]
            music = ""
            for i in musicWords:
                music += i
                music += " "
            mixer.music.unload()
            music = music[:-1]
            openMusic(music)
            print(f"Playing {music}")
            paused = False
    elif commandlowerf in ["artist", "current"]:
        if current is not None:
            try:
                print("Playing \"" + wordCapitalize(current) + "\" by " + artists[current])
            except:
                print("Playing \"" + wordCapitalize(current) + '"')
                print("This song has no registered artist.")
                a = input("Please enter the artist: ")
                artists[current] = a
    elif "q" == commandlowerf or "queue" == commandlowerf:
        if " " in commandlower:
            musicWords = commandlower.split(" ")[1:]
            music = ""
            for i in musicWords:
                music += i
                music += " "
            music = music[:-1]
            if music in playlist:
                queue.append(music)
                print(f"Added {music} to queue")
            else:
                songs = []
                for i in artists:
                    if music in artists[i].lower():
                        songs.append(i)
                if len(songs) == 0:
                    print(f"Track or Artist {music} is not available. Searching Albums...")
                    commandParser(f"_qa {music}")
                else:
                    queue = queue + songs
                    print(f"Queued artist {wordCapitalize(music)}")
        else:
            print("Your queue\n    ", end="")
            print(*queue, sep="\n    ")
    elif "_q" == commandlowerf:
        if " " in commandlower:
            musicWords = commandlower.split(" ")[1:]
            music = ""
            for i in musicWords:
                music += i
                music += " "
            music = music[:-1]
            queue.append(music)
            print(f"Added {music} to queue")
    elif commandlowerf in ["list", "l", "_lc", "library"]:
        for i, j, files in os.walk(os.path.join(song_path, "")):
            for i in files:
                if i[0] != ".":
                    if i.split(".")[0] not in playlist:
                        playlist.append(i.split(".")[0])
        if commandlowerf != "_lc":
            print("Your Musik library:")
            for i in range(0, len(playlist)):
                print(f"    [{i}] {playlist[i]}")
    elif "playlist" == commandlowerf or "pl" == commandlowerf or "plq" == commandlowerf or "playlistq" == commandlowerf:
        if len(playlist) != 0:
            if " " in commandlower:
                index = int(commandlower.split(" ")[-1])
                if len(playlist) > index >= 0:
                    if "q" in commandlower.split(" ")[0]:
                        queue.append(playlist[index])
                        print(f"Added {playlist[index]} to queue")
                    else:
                        openMusic(playlist[index])
                        print(f"Playing {playlist[index]}")
                else:
                    print("Enter a valid library index")
            else:
                if "q" in commandlowerf:
                    queue = queue + playlist
                    print(f"Adding library to queue")
                else:
                    openMusic(playlist[0])
                    queue = copy.deepcopy(playlist[1:])
                    print(f"Playing {playlist[0]} and adding library to queue")
    elif commandlowerf == "refresh":
        commandParser("_lc")
    elif commandlowerf in ["skip", "next", "n"]:
        if len(queue) > 0:
            mixer.music.stop()
    elif commandlowerf in ["loop", "repeat", "r"]:
        if "q" in commandlower:
            loopq = not loopq
            print(f"Loop Queue: {loopq}")
        else:
            loop = not loop
            print(f"Loop: {loop}")
    elif commandlowerf in ["random", "shuffle", "s"]:
        random.shuffle(queue)
        print("Shuffled queue")
    elif commandlowerf in ["clear", "c"]:
        queue = []
        print("Cleared queue")
    elif commandlowerf in ["calbum", "ca", "create album"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            songs = []
            while True:
                songName = input("Enter song to add to new album (--q to finish): ").lower()
                if songName == "--q":
                    break
                songs.append(songName)
            albums[albumName] = songs
            print(f"Created album \"{albumName}\" with {len(songs)} songs")
    elif commandlowerf in ["dalbum", "da", "delete album"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            try:
                del albums[albumName]
                print(f"Deleted album \"{albumName}\"")
            except:
                print(f"Album \"{albumName}\" does not exist")
    elif commandlowerf in ["pa", "palbum", "play album", "_pa"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            try:
                songs = albums[albumName]
                queue = copy.deepcopy(songs)
                current = None
                print(f"Playing album \"{albumName}\"")
            except:
                if "_" in commandlowerf:
                    print(f"Album \"{albumName}\" not found. Searching library...")
                    pass
                else:
                    print(f"Album \"{albumName}\" does not exist")
    elif commandlowerf in ["a", "albums", "album"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            try:
                songs = albums[albumName]
                print(f"Album \"{albumName}\":")
                for song in songs:
                    print(f"\t{song}")
            except:
                print(f"Album \"{albumName}\" does not exist")
        else:
            print("Albums:")
            for album in albums:
                print(f"\t{album}")
    elif commandlowerf in ["qa", "qalbum", "queue album", "_qa"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            try:
                songs = albums[albumName]
                for song in songs:
                    queue.append(song)
                print(f"Queued album \"{albumName}\"")
            except:
                if "_" in commandlowerf:
                    print(f"Album \"{albumName}\" not found. Searching library...")
                    pass
                else:
                    print(f"Album \"{albumName}\" does not exist")
    elif commandlowerf in ["ea", "ealbum", "edit album"]:
        if " " in commandlower:
            albumNames = commandlower.split()[1:]
            albumName = ' '.join(albumNames)
            try:
                songs = albums[albumName]
                print(f"Songs in {albumName}: {songs}")
                while True:
                    songName = input("Enter song to add to album (--q to finish): ").lower()
                    if songName == "--q":
                        break
                    songs.append(songName)
                while True:
                    songName = input("Enter song to remove from album (--q to finish): ").lower()
                    if songName == "--q":
                        break
                    try:
                        del songs[songs.index(songName)]
                    except:
                        print("No such song exists in the album")
                albums[albumName] = songs
                print(f"Edited album \"{albumName}\"")
            except:
                print(f"Album \"{albumName}\" does not exist")
    elif commandlowerf in ["t", "time", "length"]:
        if " " in commandlower and current is not None:
            seconds = 0
            if ":" in commandlower or "," in commandlower or "." in commandlower or "/" in commandlower or "\\" in commandlower or ";" in commandlower:
                tp = commandlower.split(' ')[1:]
                t = ""
                for i in range(0, len(tp)):
                    t += tp[i]
                t.strip(' ')
                brk = t[-3]
                if brk.isdigit():
                    brk = t[-2]
                segments = t.split(brk)
                if len(segments) == 2:
                    seconds = (int(segments[0])*60)+int(segments[1])
                elif len(segments) == 3:
                    seconds = (int(segments[0])*3600)+(int(segments[1])*60)+int(segments[2])
            else:
                seconds = int(commandlower.split(' ')[1])
            prev_length = int(pygame.mixer.music.get_pos() / 1000) - seconds
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(seconds)
            print(f"Jumped to {seconds} seconds.")
        elif current is not None:
            seconds = int(pygame.mixer.music.get_pos() / 1000)
            seconds -= prev_length
            minutes = int(seconds // 60)
            hours = int(seconds // 3600)
            minutes -= hours * 60
            seconds = int(seconds % 60)
            tminutes = int(length // 60)
            thours = int(length // 3600)
            tminutes -= thours * 60
            tseconds = int(length % 60)
            print(f"{hours}:{minutes}:{seconds}/{thours}:{tminutes}:{tseconds}")
    elif commandlowerf in ["help", "h"]:
        print(f"""-- Musik Help --
Commands:
    quit, exit, esc - Quits Musik
    p, play + name of song - Play specified song if in library or play all songs of specified artist or search albums
    pause, press enter - Pause current music
    unpause, press enter, resume, continue - Unpause current music
    stop - Stop all music and clear queue
    q, queue + name of song - Add specified song or artist to queue if in library or search albums
    v, volume + volume - Change volume to specified number (between 0-100)
    l, list, library - View all songs in your library by number
    playlist, pl + number - Play a song from your library by number or play the first song and add the entire library to the queue if not specified
    playlistq, plq + number - Queue a song from your library by number or queue the entire library if not specified
    n, next, skip - Move to the next song in queue, if any
    refresh - Refresh your library to check for new arrivals
    loop, repeat, r - Loop/Unloop the current song
    loop queue, loopq, loop q - Loop/Unloop the current song and queue
    random, shuffle, s - Shuffle the queue
    c, clear - Clear the queue
    t, time, length - Get the current position in the song and total length of the song
    t, time, length + (value in seconds) - Jump to the point in the song given by the specified value
    t, time, length + (hours:minutes:seconds) - Jump to the specified time, (seperated by commas, periods, colons, semi-colons or back or forward slashes)
    artist, current - View information about the current song
    ca, calbum, create album + name - Create a new album with the specified name
    da, dalbum, delete album + name - Delete specified album
    pa, palbum, play album + name - Play specified album
    qa, qalbum, queue album + name - Queue specified album
    a, albums, album + name - View contents of specified album or view all albums if not specified
    ea, ealubm, edit album + name - Add and remove songs from specified album
    h, help - Open Musik Help
            
Adding songs:
    Songs are not provided and you will have to download them yourself (the song needs to be in the MP3, WAV or OGG formats)
    Once you have the file, simply move or copy the song into {song_path} then ensure the name is in lower case and you're good to go!
            
Musik is made by Blueish""")


mixer.init(buffer=1024)
extensions = [".mp3", ".wav", ".WAV", ".ogg"]


def openMusic(name):
    global current, discord, queue, length, prev_length, lengthProc
    for extension in extensions:
        try:
            file_path = os.path.join(song_path, name+extension)
            prev_length = 0
            mixer.music.load(file_path)
            mixer.music.play()
            current = name
            length = 0
            try:
                lengthProc = Popen(["python3", os.path.join(home_path, "Musik", "mlength.py"), file_path, length_path])
            except:
                try:
                    lengthProc = Popen(["python", os.path.join(home_path, "Musik", "mlength.py"), file_path, length_path])
                except:
                    pass
            name = ""
            for i in current.split(" "):
                name += i.capitalize() + " "
            name = name[:-1]
            break
        except:
            continue


# start the input thread
commandParser("_lc")
inputThread = InputThread(commandParser)


def wordCapitalize(words):
    name = ""
    for i in words.split(" "):
        name += i.capitalize() + " "
    name = name[:-1]
    return name


while True:
    if not mixer.music.get_busy():
        if loop and not quit and not paused and current is not None:
            openMusic(current)
        elif len(queue) != 0 and not quit and not paused:
            if loopq:
                queue.append(current)
            openMusic(queue[0])
            print(f"\nPlaying {queue[0]}\n> ", end="")
            del queue[0]
        elif quit:
            break
        elif not paused:
            current = None
            length = 0
            prev_length = 0
            if discord:
                try:
                    RPC.update(state="Idle")
                except:
                    discord = False
                    print("RPC disabled")
    if lengthProc is not None:
        if lengthProc.poll() is not None:
            file = open(length_path, "r")
            length = float(file.read().split('/')[1])
            file.close()
            lengthProc = None
    clock.tick(30)

inputThread.join()
mixer.music.unload()
mixer.quit()
pygame.quit()
