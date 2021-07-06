
import os
from tkinter import *
from pygame import mixer
import tkinter.messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import threading
import time
from tkinter import ttk
from ttkthemes import themed_tk as tk

mixer.init()
root = tk.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.title("Media Player")
root.geometry("700x400")
root.iconbitmap(r'images/headphone.ico')
# Root - Leftframe,rigthframe and statusbar is there
statusbar = ttk.Label(root, text="welcome to melody Player", relief=SUNKEN, anchor=W,font='Times 10 bold')
statusbar.pack(side=BOTTOM, fill=X)
# status bar iscoded at top to ensure it occupies the maximum span of the window
# menubar 1 :-
menubar = Menu(root)
root.config(menu=menubar)
submenu = Menu(menubar, tearoff=0)

leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=10)
rightframe = Frame(root)
rightframe.pack(pady=30,padx=10)
topframe = Frame(rightframe)
topframe.pack()
lenlabel = ttk.Label(topframe, text="Length : -- --")
lenlabel.pack()
listbox = Listbox(leftframe)
listbox.pack()

def browse_file():
    global filepath_name

    filepath_name = filedialog.askopenfilename()
    add_to_playlist(filepath_name)

index = 0
playlist = []
def add_to_playlist(f):
    global index
    filename = os.path.basename(f)
    listbox.insert(index, filename)
    playlist.insert(index, f)
    index = index + 1

def del_file():
    try:
        song_select = listbox.curselection()
        song_select = int(song_select[0])
        listbox.delete(song_select)
        playlist.pop()
    except:
         tkinter.messagebox.showerror("Selection error","Please select a file before deleting")

add_btn = ttk.Button(leftframe, text="add+",command=browse_file)
add_btn.pack(side=LEFT)
del_btn = ttk.Button(leftframe, text="del-",command=del_file)
del_btn.pack(side=LEFT)

menubar.add_cascade(label='file', menu=submenu)
submenu.add_command(label='Open', command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


# menubar 2 :-
def about_us():
    tkinter.messagebox.showinfo('About us', 'This is a music player developed by A Sampath Abhishek')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=submenu)
submenu.add_command(label='About us', command=about_us)
photo = PhotoImage(file='images/play-button.png')
photo2 = PhotoImage(file='images/stop.png')
photo3 = PhotoImage(file='images/pause.png')
photo4 = PhotoImage(file='images/rewind.png')
photo5 = PhotoImage(file='images/mute.png')
photo6 = PhotoImage(file='images/speaker.png')
'''labe = Label(root, image=photo)
labe.pack()'''
middleframe = Frame(rightframe)
middleframe.pack(padx=30, pady=30)

bottomframe = Frame(rightframe)
bottomframe.pack(pady=20)

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = listbox.curselection()
            select_song = int(selected_song[0])
            play_it = playlist[select_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def show_details(play_song):
    file_name = os.path.basename(play_song)
    name = file_name.endswith(".mp3")
    if name:
        audio = MP3(play_song) #loads mp3 file into the variable audio
        total_length = audio.info.length
        min,secs = divmod(total_length,60)
        mins = round(min)
        sec = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins,sec)
        lenlabel['text'] = 'length : '+ timeformat
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length() # loads audio in seconds
        min, secs = divmod(total_length, 60)
        mins = round(min)
        sec = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, sec)
        lenlabel['text'] = 'length : ' + timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

but = ttk.Button(middleframe, image=photo, command=play_music)
but.grid(row=0, column=0, padx=10)

currenttimelabel = ttk.Label(topframe, relief=GROOVE, text="Current time : ----")
currenttimelabel.pack(pady=10)

def start_count(t):
    while t and mixer.music.get_busy():
        global paused
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            min = round(mins)
            sec = round(secs)
            timeformat = '{:02d}:{:02d}'.format(min,sec)
            currenttimelabel['text'] = 'Current time :'+ timeformat
            time.sleep(1)
            t = t-1
def stop_music():
    global paused
    paused = FALSE
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'


stop_but = ttk.Button(middleframe, image=photo2, command=stop_music)
stop_but.grid(row=0, column=2, padx=10)

paused = FALSE


def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = 'Music paused'


pause_but = ttk.Button(middleframe, image=photo3, command=pause_music)
pause_but.grid(row=0, column=1, padx=10)


def rewind_music():
    play_music()


rewind_but = ttk.Button(bottomframe, image=photo4, command=rewind_music)
rewind_but.grid(row=1, column=0, padx=10)

muted = FALSE


def mute_music():
    global muted
    if muted:
        speaker_but.configure(image=photo6)
        mixer.music.set_volume(0.7)
        scale.set(70)
        muted = FALSE
    else:
        speaker_but.configure(image=photo5)
        mixer.music.set_volume(0)
        scale.set(0)
        muted = TRUE


speaker_but = ttk.Button(bottomframe, image=photo6, command=mute_music)
speaker_but.grid(row=1, column=1, padx=10)


def set_vol(var):
    volume = float(var) / 100
    mixer.music.set_volume(volume)

def close_window():
    stop_music()
    root.destroy()

scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(12)
mixer.music.set_volume(0.12)
scale.grid(row=1, column=2, padx=10)
print(scale.get())

root.protocol('WM_DELETE_WINDOW',close_window)
root.mainloop()
