import module_manager
import pyaudio
import wave
from array import array
from struct import pack
from tkinter import *

class PianoKeyWhite():
    def __init__(self,x,note,audioFile):
        self.note = note 
        self.audioFile = audioFile
        self.keySizeX = 50
        self.keySizeY = 240
        self.x = x
    def play(self,file):
        CHUNK = 1024 #measured in bytes

        wf = wave.open(file, 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()

    def draw(self,canvas):
        canvas.create_rectangle(self.x,0,self.x + self.keySizeX, self.keySizeY, fill = "white", outline = "black")

class PianoKeyBlack():
    def __init__(self,x,note,audioFile):
        self.note = note
        self.audioFile = audioFile
        self.keySizeX = 25
        self.keySizeY = 120
        self.x = x

    def draw(self,canvas):
        canvas.create_rectangle(self.x,0,self.x + self.keySizeX, self.keySizeY, fill = "black")

def draw(canvas, width, height):
    keysWhite = []
    keysBlack = []
    for i in range(0,25):
        keysWhite.append(PianoKeyWhite(i * 50,"A","tone" + str(i) +".wav"))
        keysWhite[i].draw(canvas)

    for i in range(0,24):
        keysBlack.append(PianoKeyBlack(i * 50 + 37.5, "A", "subtone" + str(i) + ".wav"))
        keysBlack[i].draw(canvas)

def runDrawing(width=300, height=300):
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    canvas = Canvas(root, width=width, height=height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    draw(canvas, width, height)
    root.mainloop()
    print("bye!")

runDrawing(1250,240)