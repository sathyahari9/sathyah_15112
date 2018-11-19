import tkinter
import cv2
import numpy as np
import copy
from pynput.mouse import Button, Controller
import wx


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.mainloop()
        pass
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")

# Display size

lowerBound = np.array([33,80,40])
higherBound = np.array([102,255,255])

cam = cv2.VideoCapture(0)
# Defining kernel sizes for smoothing the image
kernelOpen = np.ones((5,5))
kernelClose = np.ones((20,20))

# font for text
# font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)

while True:
    ret, img = cam.read()
    # converting color from Red, Blue, Green to Hue, Saturation and Value
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # finding mask using given image and color parameters
    mask = cv2.inRange(imgHSV,lowerBound,higherBound)
    # smoothing image
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    # final mask after, smoothing, refilling
    maskFinal = maskClose
    conts, heirarchy = cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1:3]
    cv2.drawContours(img,conts,-1,(255,0,0),2)
    if len(conts) == 2:
        # mouse.release(Button.left)
        x1,y1,w1,h1 = cv2.boundingRect(conts[0])
        x2,y2,w2,h2 = cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        cx1 = int(x1 + w1 / 2)
        cy1 = int(y1 + h1 / 2)
        cx2 = int(x2 + w2 / 2)
        cy2 = int(y2 + h2 / 2)
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,0),2)
        cx = int((cx1 + cx2) / 2)
        cy = int((cy1 + cy2) / 2)
        cv2.circle(img,(cx,cy),2,(0,255,0),2)
        # mouse.position = (sx - (cx1 * sx/camx),sy - (cy1 * sy/camy))
        # while mouse.position != (sx - (cx1 * sx/camx),sy - (cy1 * sy/camy)):
        #     pass

    elif len(conts) == 1:
        x1,y1,w1,h1 = cv2.boundingRect(conts[0])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,0,255),2)
        cx1 = int(x1 + w1 / 2)
        cy1 = int(y1 + h1 / 2)
        cv2.circle(img,(cx1,cy1),int(w1/4),(0,255,0),2)
        # mouse.position = (sx - (cx1 * sx/camx),sy - (cy1 * sy/camy))
        # while mouse.position != (sx - (cx1 * sx/camx),sy - (cy1 * sy/camy)):
        #     pass
        # mouse.press(Button.left)
    cv2.imshow('MaskFinal',maskFinal)
    cv2.waitKey(10)
#work left in open cv-
# Basic Animation Framework for project


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