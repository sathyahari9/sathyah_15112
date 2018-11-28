# Name - Sathya Hari
# Section - I
# Term project 1 phase
# Project currently implements keys in the form of classes, plays audio files(once threaded) and recognizes fingers based on if they are colored green
import os
import cv2
import numpy as np
import copy
import pyaudio
import wave
from array import array
from struct import pack
import time
import _thread
import random
from pynput import keyboard
import gamify as gm
import play

current = set()
# from queue import Queue

# Display size

def displayBlocks(img,coordinates,keysCo,keys):
    colors = {
        (0,100):(0,0,255),
        (75,125):(0,255,0),
        (100,200):(255,0,0),
        (175,225):(122,122,122),
        (200,300):(150,240,255),
        (300,400):(100,240,255),
        (375,425):(120,200,255),
        (400,500):(200,140,200),
        (475,525):(190,200,100),
        (500,600):(250,200,100),
        (575,625):(130,0,170),
        (600,700):(100,170,255),
        (700,800):(60,255,0),
        (775,825):(100,255,0),
        (800,900):(255,0,255),
        (875,925):(70,255,180),
        (900,1000):(240,100,255),
        (1000,1100):(200,200,30)
    }
    count = 0
    for co in coordinates:
        count+=1
        color = colors[co]
        cv2.rectangle(img,(co[0],350),(co[1],400),color,thickness=cv2.FILLED)
        print(coordinates)
        print(count)
        if count%2 == 0:
            coordinates.pop(0)
    if len(coordinates) > 0:
        print(coordinates[-1])

# Basic Animation Framework

from tkinter import *

####################################
# customize these functions
####################################

def init(data):
    data.state = 0
    data.mouseInvert = False
    pass

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def redrawAll(canvas, data):
    if data.state == 0:
        canvas.create_rectangle(0,0,data.width,data.height,fill="black")
        canvas.create_text(data.width/2,data.height/2,text="PIANO HERO",fill="white")
        if data.mouseInvert:
            canvas.create_rectangle(data.width/2 - 40, data.height/2 + 100, data.width/2 + 40, data.height/2 + 140, outline = "white", fill= "white")
            canvas.create_text(data.width/2, data.height/2 + 120, text = "PLAY", fill = "black")
        else:
            canvas.create_rectangle(data.width/2 - 40, data.height/2 + 100, data.width/2 + 40, data.height/2 + 140, outline = "white", fill= "black")
            canvas.create_text(data.width/2, data.height/2 + 120, text = "PLAY", fill = "white")
    else:
        # canvas.create_rectangle(data.width,data.height,fill="black")
        # canvas.create_text(data.width/2,data.height/2,text="AIR PIANO",fill="white")
        # canvas.create_rectangle(data.width/2 - 40, data.height/2 + 100, data.width/2 + 40, data.height/2 + 140, outline = "white")
        # canvas.create_text(data.width/2, data.height/2 + 120, text = "PLAY", fill = "white")
        pass


####################################
# use the run function as-is
####################################
        

def video():
    lowerBound = np.array([33,80,40])
    higherBound = np.array([102,255,255])
    cam = cv2.VideoCapture(0)
    # Defining kernel sizes for smoothing the image
    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))
    timeMes = 0
    # font for text
    # font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
    keyPressed= []
    keysCo = {}
    coordinates = []
    while True:
        ret, img = cam.read()
        img = cv2.resize(img,(1100,600))
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
        cs = []
        cv2.drawContours(img,conts,-1,(255,0,0),2)
        for i in range(0,11):
            cv2.rectangle(img,(i * 100,400),(i * 100 + 100,600),(255,255,255),thickness=cv2.FILLED)
            cv2.rectangle(img, (i * 100, 400), (i * 100 + 100, 600), (0,0, 0), 1)
        #
        cv2.rectangle(img, (75,400),(125,550),(0,0,0),thickness=cv2.FILLED)
        cv2.rectangle(img, (175, 400), (225, 550), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (375, 400), (425, 550), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (475, 400), (525, 550), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (575, 400), (625, 550), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (775, 400), (825, 550), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (875, 400), (925, 550), (0, 0, 0), thickness=cv2.FILLED)
        #
        keys = {
        1:"C.wav",
        2:"C_s.wav",
        3:"D.wav",
        4:"D_s.wav",
        5:"E.wav",
        6:"F.wav",
        7:"F_s.wav",
        8:"G.wav",
        9:"G_s.wav",
        10:"A.wav",
        11:"Bb.wav",
        12:"B.wav",
        13:"C1.wav",
        14:"C_s1.wav",
        15:"D1.wav",
        16:"D_s1.wav",
        17:"E1.wav",
        18:"F1.wav"
        }
        keyID = 0
        displayBlocks(img,coordinates,keysCo,keys)
        for i in range(0,len(conts)):
            x1, y1, w1, h1 = cv2.boundingRect(conts[i])
            cx1 = int(x1 + w1 / 2)
            cy1 = int(y1 + h1 / 2)
            if 0 <= cx1 <= 75 and 400 <= cy1:
                keyID = 1
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(0, 400),(100, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([0,100]))
                
            elif 75 <= cx1 <= 125 and 400 <= cy1:
                keyID = 2
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(75, 400),(125, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([75,125]))
                

            elif 125 <= cx1 <= 175 and 400 <= cy1:
                keyID = 3
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(100, 400),(200, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([100,200]))
                

            elif 175 <= cx1 <= 225 and 400 <= cy1:
                keyID = 4
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(175, 400),(225, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([175,225]))
               

            elif 225 <= cx1 <= 300 and 400 <= cy1:
                keyID = 5
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(200, 400), (300, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([200,300]))
                

            elif 300 <= cx1 <= 375 and 400 <= cy1:
                keyID = 6
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(300, 400),(400, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([300,400]))
                

            elif 375 <= cx1 <= 425 and 400 <= cy1:
                keyID = 7
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(375, 400),(425, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([375,425]))
                

            elif 425 <= cx1 <= 475 and 400 <= cy1:
                keyID = 8
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(400, 400), (500, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([400,500]))
                

            elif 475 <= cx1 <= 525 and 400 <= cy1:
                keyID = 9
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(475, 400), (525, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([475,525]))

            elif 525 <= cx1 <= 575 and 400 <= cy1:
                keyID = 10
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(500, 400), (600, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([500, 600]))
               

            elif 575 <= cx1 <= 625 and 400 <= cy1:
                keyID = 11
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(575, 400), (625, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([575, 625]))
            elif 625 <= cx1 <= 700 and 400 <= cy1:
                keyID = 12
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(600, 400), (700, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([600, 700]))
                

            elif 700 <= cx1 <= 775 and 400 <= cy1:
                keyID = 13
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(700, 400), (800, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([700, 800]))
                

            elif 775 <= cx1 <= 825 and 400 <= cy1:
                keyID = 14
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(775, 400), (825, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([775, 825]))
                

            elif 825 <= cx1 <= 875 and 400 <= cy1:
                keyID = 15
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(800, 400), (900, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([800, 900]))
                

            elif 875 <= cx1 <= 925 and 400 <= cy1:
                keyID = 16
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(875, 400), (925, 550), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([875, 925]))
                

            elif 925 <= cx1 <= 1000 and 400 <= cy1:
                keyID = 17
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(900, 400), (1000, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([900, 1000]))
                

            elif 1000 <= cx1 <= 1100 and 400 <= cy1:
                keyID = 18
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1000, 400), (1100, 600), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1000, 1100]))
                
        cv2.imshow('Cam', img)
        cv2.waitKey(10)


def mousePressedWrapper(event, canvas, data):
    mousePressed(event, data)

def keyPressedWrapper(event, canvas, data):
    keyPressed(event, data)

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

def playOutput():
    curr_directory = os.getcwd()
    os.chdir(curr_directory)
    filename = askopenfilename()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()


if __name__ == "__main__":

    from tkinter import *
    from tkinter.filedialog import askopenfilename
    import pygame
    import os
    from PIL import Image, ImageFilter

    piano = Image.open("piano.jpg")
    piano.show()

    root = Tk()
    root.minsize(500,500)

    listofsongs = []

    index = 0
    path = "piano.jpg"
    # canvas = Canvas(root, width=500, height=500)
    # canvas.configure(bd=0, highlightthickness=0)
    # canvas.create_rectangle(0,0,500,500,fill="orange")
    # canvas.pack(side = TOP, anchor = NW, padx = 10, pady = 10)
    # canvas.pack()
    button1 = Button(root,text="Play Game",command=gm.playGame)
    button1.configure(width = 10, activebackground = "#33B5E5",
                                                            relief = FLAT)
    button1.pack(side = TOP)
    button2 = Button(root,text="Play Output",command=playOutput)
    button2.configure(width = 10, activebackground = "#33B5E5")
    button2.pack(side = TOP)
    button3 = Button(root,text="Play Solo",command=video)
    button3.pack(side = TOP)
    # set up events
    # root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, data))
    # root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, data))
    # redrawAll(canvas, data)
    # and launch the app
    root.mainloop()
    print("bye!")   