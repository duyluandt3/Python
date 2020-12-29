# PYTHON AUDIO PLAYER

import pygame
import tkinter as tkr
import os

# Create window
player = tkr.Tk()

# Edit window
player.title("Audio Player")
player.geometry("205x340")

# Get playlist
os.chdir("D:/DATA/Entertainment/Music")
songlist = os.listdir()

# Volume control
volumControl = tkr.Scale(player, from_=0.0, to_=1.0, orient=tkr.HORIZONTAL, resolution=0.1)

# Play list
playlist = tkr.Listbox(player, highlightcolor="blue", selectmode=tkr.SINGLE)
print(playlist)

pos = 0
for item in songlist:
    playlist.insert(pos, item)
    pos += 1


# Init
pygame.init()
pygame.mixer.init()


# Action Event
def Play():
    pygame.mixer.music.load(playlist.get(tkr.ACTIVE))
    var.set(playlist.get(tkr.ACTIVE))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volumControl.get())
    print(pygame.mixer.music.get_volume())
    print(volumControl.get())



def ExitPlayer():
    pygame.mixer.music.stop()


def Pause():
    pygame.mixer.music.pause()


def UnPause():
    pygame.mixer.music.unpause()




# Register button
btnPlay = tkr.Button(player, width=5, height=3, text="PLAY", command=Play)
btnStop = tkr.Button(player, width=5, height=3,
                     text="STOP", command=ExitPlayer)
btnPause = tkr.Button(player, width=5, height=3,
                      text="PAUSE", command=Pause)
btnUnPause = tkr.Button(player, width=5, height=3,
                        text="UNPAUSE", command=UnPause)


# Get song
#file = "Song.mp3"
var = tkr.StringVar()
songtitle = tkr.Label(player, textvariable=var)


# Place Widgets
songtitle.pack()
btnPlay.pack(fill="x")
btnStop.pack(fill="x")
btnPause.pack(fill="x")
btnUnPause.pack(fill="x")
volumControl.pack(fill="x")
playlist.pack(fill="both", expand="yes")

# Main
player.mainloop()
