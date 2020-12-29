# PYTHON AUDIO PLAYER

import os
import time
import datetime
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar

root = Tk()

# Set UI
root.geometry("780x500+200+50")
root.title("MP3 PLAYER")
#root.iconbitmap("icon.ico")
root.resizable(False, False)
root.configure(bg="lightskyblue")

# Global variable
audioTrack = StringVar()    # Get and set song
playList = []               # Add song to playlist
dir_opt = {}                # Directory

pauseStatus = 0             # Playing

currentVolVal = 1.0         # Volume control
muteStatus = 0              # Unmute status

totalSongLength = 0

# Volume lable
lblProgess = ''
lblVolumeProgess = ''
prgbVolume = ''

# Music lable
lblProgessMusic = ''
lblProgressMusicStartTime = ''
lblProgressMusicEndTime = ''
prgbMusic = ''
#############################################################

# FlyText funcion variable
cnt = 0
initText = ''
txtFly = "Mp3 Player - Copyright by duyluandt3"
lblFly = Label(root, background="lightskyblue",
               font=("arial", 10, "italic bold"))
lblFly.grid(row=6, column=0, padx=15, pady=10, columnspan=3)


# Title
# lblTitle = Label(root, background="lightskyblue", width=30,
#                  font=("arial", 12, "italic bold"), textvariable=audioTrack)
cntTitle = 0
initTitle = ''
selectTurn = 'Select songs..'

lblTitle = Label(root, background="lightskyblue", width=30,
                 font=("arial", 12, "italic bold"))
lblTitle.grid(row=3, column=0, padx=15, pady=10, columnspan=3)

#print(audioTrack.get())

# Status
lblStatus = Label(root, background="lightskyblue",
                  font=("arial", 12, "italic bold"), text="Waiting...")
lblStatus.grid(row=2, column=0, padx=15, pady=10, columnspan=3)


# Scroll bar for play list


# UI design
def CreateWidthes():
    # # Icon
    # global impPlay, impPause, impStop, impVolUp, impVolDown

    # impPlay = PhotoImage(file=r'D:\DATA\Electronic\Electronic Study\Python\Mp3_PJ\V2\play.png')
    # impPause = PhotoImage("/icon/pause.png").subsample(2,2 )
    # impStop = PhotoImage("/icon/stop.png").subsample(2,2 )
    # impVolUp = PhotoImage("/icon/volup.png").subsample(2,2 )
    # impVolDown = PhotoImage("/icon/voldown.png").subsample(2,2 )

    # impPlay = impPlay.subsample(30,30)

    # Label
    global playList, lblStatus
    global lblProgess, lblVolumeProgess, prgbVolume
    global lblProgessMusic, lblProgressMusicStartTime, lblProgressMusicEndTime, prgbMusic

    lblTrack = Label(root, text="Select audio: ",
                     background="lightskyblue", font=("arial", 12, "italic bold"))
    lblTrack.grid(row=0, column=0, padx=15, pady=10)

    entryTrack = Entry(root, font=("arial", 12, "italic bold"),
                       width=35, textvariable=audioTrack)
    entryTrack.grid(row=0, column=1, padx=15, pady=10)

    # Button
    btnBrowse = Button(root, text="Open", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=MusicCurl)
    btnBrowse.grid(row=0, column=2, padx=15, pady=10)

    btnPlay = Button(root, text="Play", bg="green2", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=PlayMusic)
    btnPlay.grid(row=1, column=0, padx=20, pady=10)

    root.btnPause = Button(root, text="Pause", bg="blue", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=PauseMusic)
    root.btnPause.grid(row=1, column=1, padx=10, pady=10)

    root.btnResume = Button(root, text="Resume", bg="blue", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=ResumeMusic)
    root.btnResume.grid(row=1, column=1, padx=10, pady=10)
    root.btnResume.grid_remove()

    root.btnMute = Button(root, text="Mute", width=12, bg="yellow", activebackground="purple4",
                          font=("arial", 13, "italic bold"), bd=2, compound=RIGHT, command=MuteMusic)
    root.btnMute.grid(row=3, column=2, padx=15, pady=5)

    root.btnUnMute = Button(root, text="UnMute", width=12, bg="yellow", activebackground="purple4",
                            font=("arial", 13, "italic bold"), bd=2, compound=RIGHT, command=UnMuteMusic)
    root.btnUnMute.grid(row=3, column=2, padx=15, pady=5)
    root.btnUnMute.grid_remove()

    btnVolUp = Button(root, text="Vol +", bg="gray", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=VolUp)
    btnVolUp.grid(row=1, column=2, padx=15, pady=10)

    btnVolDown = Button(root, text="Vol -", bg="gray", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=VolDown)
    btnVolDown.grid(row=2, column=2, padx=15, pady=5)

    btnStop = Button(root, text="Stop", bg="red", font=(
        "arial", 13, "italic bold"), width=12, bd=2, activebackground="purple4", command=StopMusic)
    btnStop.grid(row=2, column=0, padx=20, pady=10)


    sb = Scrollbar(root, width=15,  orient=VERTICAL)  
    sb.grid(row=5, column=2, padx=135, pady=5, columnspan=3)

    playList = Listbox(root, highlightcolor="blue",
                       width=100, selectmode=SINGLE,  yscrollcommand = sb.set)
    #print(type(playList))
    playList.grid(row=5, column=0, padx=15, pady=5, columnspan=3)

    sb.config(command = playList.yview)

    ########### Progess bar volume ###########
    lblProgess = Label(root, text='', bg="red", width=3)
    lblProgess.grid(row=0, column=3, rowspan=3, padx=10, pady=20)

    prgbVolume = Progressbar(lblProgess, orient=VERTICAL,
                             mode="determinate", value=0, length=150)
    prgbVolume.grid(row=0, column=0, ipadx=5)

    lblVolumeProgess = Label(lblProgess, text="0", bg="lightgray", width=3)
    lblVolumeProgess.grid(row=0, column=0)

    ########### Progess bar music ###########
    lblProgessMusic = Label(root, text="", bg="red")
    lblProgessMusic.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    lblProgressMusicStartTime = Label(lblProgessMusic, text="0:00:0", bg="red")
    lblProgressMusicStartTime.grid(row=0, column=0)

    lblProgressMusicEndTime = Label(lblProgessMusic, text="0:00:0", bg="red")
    lblProgressMusicEndTime.grid(row=0, column=2)

    prgbMusic = Progressbar(
        lblProgessMusic, orient=HORIZONTAL, mode="determinate", value=0)
    prgbMusic.grid(row=0, column=1, ipadx=213, ipady=3)


def FlyText():
    #global cnt, initText
    global cnt, initText
    if(cnt >= len(txtFly)):
        cnt = -1
        initText = ''
        lblFly.configure(text=initText)
    else:
        initText = initText + txtFly[cnt]
        lblFly.configure(text=initText)
    cnt += 1
    lblFly.after(200, FlyText)


def FlyTitle():
    #global cnt, initText
    global cntTitle, initTitle
    if(cntTitle >= len(selectTurn)):
        cntTitle = -1
        initTitle = ''
        lblTitle.configure(text=initTitle)
    else:
        initTitle = initTitle + selectTurn[cntTitle]
        lblTitle.configure(text=initTitle)
    cntTitle += 1
    lblTitle.after(200, FlyTitle)


def Init():
    #pygame.init()
    mixer.init()


def MusicCurl():
    # dd = filedialog.askopenfilename()
    # audioTrack.set(dd)
    try:
        dd = filedialog.askdirectory(title="Open", **dir_opt)
        audioTrack.set(dd)
        os.chdir(dd)
        songList = os.listdir()
        pos = 0
        for item in songList:
            playList.insert(pos, item)
            pos += 1
    except IOError:
        pass


def PlayMusic():
    # Lable change
    global lblStatus
    global selectTurn
    lblStatus.configure(text="Playing...")
    # Start
    try:
        selectTurn = playList.get(ACTIVE)
        mixer.music.load(selectTurn)
    except IndexError:
        pass
    audioTrack.set(playList.get(ACTIVE))
    mixer.music.set_volume(currentVolVal)
    mixer.music.play()

    song = MP3(selectTurn)
    totalSongLength = int(song.info.length)
    prgbMusic["maximum"] = totalSongLength
    lblProgressMusicEndTime.configure(text="{}".format(
        str(datetime.timedelta(seconds=totalSongLength))))
    #print(totalSongLength)
    #print(selectTurn)
    ProgessbarMusicTick()


def ProgessbarMusicTick():
    currentSongLength = mixer.music.get_pos()//1000
    prgbMusic["value"] = currentSongLength
    prgbMusic.after(2, ProgessbarMusicTick)
    lblProgressMusicStartTime.configure(text="{}".format(
        str(datetime.timedelta(seconds=currentSongLength))))
    #print(currentSongLength)


def PauseMusic():
    # Lable change
    global lblStatus
    lblStatus.configure(text="Pausing...")

    # Start
    mixer.music.pause()
    pauseStatus = 1
    if(pauseStatus == 1):
        root.btnPause.grid_remove()
        root.btnResume.grid()
        pauseStatus = 0
    else:
        ResumeMusic()


def ResumeMusic():
    # Lable change
    global lblStatus
    lblStatus.configure(text="Playing...")
    # Start

    root.btnResume.grid_remove()
    root.btnPause.grid()
    mixer.music.unpause()
    pauseStatus = 1


def StopMusic():
    # Lable change
    global lblStatus
    lblStatus.configure(text="Stopping...")
    # Start

    mixer.music.stop()


def VolUp():
    global lblVolumeProgess
    vol = mixer.music.get_volume()
    if(vol >= vol*100):
        mixer.music.set_volume(vol+0.01)
    else:
        mixer.music.set_volume(vol+0.05)
    lblVolumeProgess.configure(text='{}'.format(
        int(mixer.music.get_volume()*100)))
    prgbVolume['value'] = mixer.music.get_volume()*100
    #print(vol)


def CurrentVolume():
    global lblVolumeProgess
    vol = mixer.music.get_volume()
    lblVolumeProgess.configure(text='{}'.format(
        int(mixer.music.get_volume()*100)))
    prgbVolume['value'] = mixer.music.get_volume()*100


def VolDown():
    global lblVolumeProgess
    vol = mixer.music.get_volume()
    if(vol >= vol*100):
        mixer.music.set_volume(vol-0.01)
    else:
        mixer.music.set_volume(vol-0.05)
    lblVolumeProgess.configure(text="{}".format(
        int(mixer.music.get_volume()*100)))
    prgbVolume['value'] = mixer.music.get_volume()*100
    #print(vol)


def MuteMusic():
    # Lable change
    global lblStatus
    lblStatus.configure(text="Mute...")
    # Start

    global currentVolVal
    muteStatus = 1
    if(muteStatus == 1):
        root.btnMute.grid_remove()
        root.btnUnMute.grid()
        muteStatus = 0
    else:
        UnMuteMusic()

    currentVolVal = mixer.music.get_volume()
    mixer.music.set_volume(0)

    lblVolumeProgess.configure(text="0")
    prgbVolume['value'] = 0


def UnMuteMusic():
    # Lable change
    global lblStatus
    lblStatus.configure(text="Unmute...")
    time.sleep(0.1)
    lblStatus.configure(text="Playing...")

    # Start
    global currentVolVal
    root.btnUnMute.grid_remove()
    root.btnMute.grid()

    mixer.music.set_volume(currentVolVal)
    muteStatus = 1
    lblVolumeProgess.configure(text="{}".format(
        int(mixer.music.get_volume()*100)))
    prgbVolume['value'] = mixer.music.get_volume()*100


FlyText()
FlyTitle()
CreateWidthes()
Init()
CurrentVolume()
#MusicCurl()

root.mainloop()
