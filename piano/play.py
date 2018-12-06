import pyaudio
import wave
from array import array
from struct import pack
from tkinter import *
import os

def play(file):
    CHUNK = 1024
    wf = wave.open(file, 'rb')
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    audio.terminate()

def play_audio(keyID,keys):
    filename = keys[keyID]
    play("raw3/" + filename)

def playWrapper():
    listofsongs = []
    wind = Toplevel()
    wind.minsize(450,250)
    wind.configure(background="#6ef442")
    for song in os.listdir("recordings/"):
        listofsongs.append(song)

    listbox = Listbox(wind)
    for song in listofsongs:
        listbox.insert(0,song)
    listbox.configure(relief="flat",background="#EEEEEE",bd=2,height=10)
    listbox.pack(side = "top",anchor = S)
    print(listbox.get(ACTIVE))
    button3 = Button(wind,text="Play Recording",command=lambda: play("recordings/"+str(listbox.get(ACTIVE))))
    button3.configure(relief="groove", foreground= "black",padx = 10, pady =10)
    button3.pack()