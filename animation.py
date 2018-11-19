# Basic Animation Framework

from tkinter import *

####################################
# customize these functions
####################################
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


def init(data):
    data.keysWhite = []
    data.keysBlack = []
    for i in range(0,25):
        data.keysWhite.append(PianoKeyWhite(i * 50,"A","tone" + str(i) +".wav"))

    for i in range(0,24):
        data.keysBlack.append(PianoKeyBlack(i * 50 + 37.5, "A", "subtone" + str(i) + ".wav"))

    pass

def mousePressed(event, data):

    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    for i in range(0,25):
        data.keysWhite[i].draw(canvas)
    for i in range(0,24):
        data.keysBlack[i].draw(canvas)
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1250, 220)