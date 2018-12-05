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
    play("raw/" + filename)

def playWrapper():
    listofsongs = []
    wind = Toplevel()
    wind.minsize(500,500)
    for song in os.listdir("recordings/"):
        listofsongs.append(song)

    listbox = Listbox(wind)
    for song in listofsongs:
        listbox.insert(0,song)
    listbox.pack(side = "bottom",anchor = S)
    print(listbox.get(ACTIVE))
    button3 = Button(wind,text="Play",command=lambda: play("recordings/"+str(listbox.get(ACTIVE))))
    button3.pack()