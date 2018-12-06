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
import playGame as gm
import play
import example
import threading
import subprocess

from time import gmtime, strftime
date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
outfile = date + ".wav"

# function to display blocks
def displayBlocks(img,coordinates,keysCo,keys):
    global a
    colors = {
        (0,60):(0,0,255),
        (45,75):(0,255,0),
        (60,120):(255,0,0),
        (105,135):(122,122,122),
        (120,180):(150,240,255),
        (180,240):(100,240,255),
        (225,255):(120,200,255),
        (240,300):(200,140,200),
        (285,315):(190,200,100),
        (300,360):(250,200,100),
        (345,375):(130,0,170),
        (360,420):(100,170,255),
        (420,480):(60,255,0),
        (465,495):(100,255,0),
        (480,540):(255,0,255),
        (525,555):(70,255,180),
        (540,600):(240,100,255),
        (600,660):(200,200,30),
        (645,675):(200,0,30),
        (660,720):(180,200,130),
        (705,735):(100,20,130),
        (720,780):(200,200,30),
        (765,795):(200,200,30),
        (780,840):(200,200,30),
        (840,900):(200,200,30),
        (885,915):(200,200,30),
        (900,960):(200,200,30),
        (945,975):(200,200,30),
        (960,1020):(200,200,30),
        (1020,1080):(200,200,30),
        (1065,1095):(200,200,30),
        (1080,1140):(200,200,30),
        (1125,1155):(200,200,30),
        (1140,1200):(200,200,30),
        (1185,1215):(200,200,30),
        (1200,1260):(200,200,30)
    }
    count = 0
    for co in coordinates:
        count+=1
        color = colors[co]
        cv2.rectangle(img,(co[0],450),(co[1],500),color,thickness=cv2.FILLED)
        print(coordinates)
        print(count)
        if count%2 == 0:
            coordinates.pop(0)
    if len(coordinates) > 0:
        print(coordinates[-1])

# Basic Animation Framework

from tkinter import *
from PIL import Image, ImageFilter, ImageTk

#############################################################################
# FUNCTION BASE TAKEN FROM 15-112 WEBSITE, CODE MODIFIED FOR CURRENT PROGRAM
#############################################################################

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

def init(data):
    data.state = 0
    data.mouseInvert = False
    pass

def mousePressed(event, data):
    if event.x >= data.width/2 - 40 and event.x <= data.width/2 + 40 and event.y >= data.height/2 + 100 and event.y <= data.height/2 + 140:
        data.mouseInvert = True
    pass

def keyPressed(event, data):
    pass

def redrawAll(canvas, data):
    tk_img = ImageTk.PhotoImage(file = "piano.png")
    canvas.create_image(400, 200, image=tk_img)
    canvas.image = tk_img
    if data.state == 0:
        if data.mouseInvert:
            canvas.create_rectangle(data.width/2 - 40, data.height/2 + 100, data.width/2 + 40, data.height/2 + 140, outline = "white", fill= "white")
            canvas.create_text(data.width/2, data.height/2 + 120, text = "PLAY", fill = "black")
            data.mouseInvert = False
            popUp()
        else:
            canvas.create_rectangle(data.width/2 - 40, data.height/2 + 100, data.width/2 + 40, data.height/2 + 140, outline = "white", fill= "black")
            canvas.create_text(data.width/2, data.height/2 + 120, text = "PLAY", fill = "white")

coordinates = []

def video():
    global coordinates
    coordinates = []
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
    recKeys = []
    while True:
        ret, img = cam.read()
        cv2.flip(img,1)
        img = cv2.resize(img,(1260,700))
        img = cv2.flip( img, 1 )
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
        for i in range(0,21):
            cv2.rectangle(img,(i * 60,500),(i * 60 + 60,700),(255,255,255),thickness=cv2.FILLED)
            cv2.rectangle(img, (i * 60, 500), (i * 60 + 60, 700), (0,0, 0), 1)
        #
        cv2.rectangle(img, (45,500),(75,650),(0,0,0),thickness=cv2.FILLED)
        cv2.rectangle(img, (105, 500), (135, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (225, 500), (255, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (285, 500), (315, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (345, 500), (375, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (465, 500), (495, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (525, 500), (555, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (645, 500), (675, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (705, 500), (735, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (765, 500), (795, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (885, 500), (915, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (945, 500), (975, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (1065, 500), (1095, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (1125, 500), (1155, 650), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (1185, 500), (1215, 650), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (20,20),(60,45),(0,0,0), thickness=cv2.FILLED)
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
        11:"A_s.wav",
        12:"B.wav",
        13:"C1.wav",
        14:"C_s1.wav",
        15:"D1.wav",
        16:"D_s1.wav",
        17:"E1.wav",
        18:"F1.wav",
        19:"F_s1.wav",
        20:"G.wav",
        21:"G_s.wav",
        22:"A1.wav",
        23:"A_s1.wav",
        24:"B.wav",
        25:"C2.wav",
        26:"C_s2.wav",
        27:"D2.wav",
        28:"D_s2.wav",
        29:"E2.wav",
        30:"F2.wav",
        31:"F_s2.wav",
        32:"G2.wav",
        33:"G_s2.wav",
        34:"A2.wav",
        35:"A_s2.wav",
        36:"B2.wav"
        }
        keyID = 0
        displayBlocks(img,coordinates,keysCo,keys)
        for i in range(0,len(conts)):
            x1, y1, w1, h1 = cv2.boundingRect(conts[i])
            cx1 = int(x1 + w1 / 2)
            cy1 = int(y1 + h1 / 2)
            if 20<= cx1 <= 60 and 20 <= cy1 <= 40:
                print("ligma")
                example.start_audio_recording()
            if 0 <= cx1 <= 45 and 500 <= cy1:
                keyID = 1
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(0, 500),(60, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([0,60]))
                recKeys.append(keyID)

            elif 45 <= cx1 <= 75 and 500 <= cy1:
                keyID = 2
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(45, 500),(75, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([45,75]))
                recKeys.append(keyID)

            elif 75 <= cx1 <= 105 and 500 <= cy1:
                keyID = 3
                _thread.start_new_thread(play.play_audio,(keyID,keys,))
                cv2.rectangle(img,(60, 500),(120, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([60,120]))
                recKeys.append(keyID)

            elif 105 <= cx1 <= 135 and 500 <= cy1:
                keyID = 4
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(105, 500),(135, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([105,135]))
                recKeys.append(keyID)

            elif 135 <= cx1 <= 180 and 500 <= cy1:
                keyID = 5
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(120, 500), (180, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([120,180]))
                recKeys.append(keyID)

            elif 180 <= cx1 <= 225 and 500 <= cy1:
                keyID = 6
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(180, 500),(240, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([180,240]))
                recKeys.append(keyID)

            elif 225 <= cx1 <= 255 and 500 <= cy1:
                keyID = 7
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(225, 500),(255, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([225,255]))
                recKeys.append(keyID)

            elif 255 <= cx1 <= 285 and 500 <= cy1:
                keyID = 8
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(240, 500), (300, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([240,300]))
                recKeys.append(keyID)

            elif 285 <= cx1 <= 315 and 500 <= cy1:
                keyID = 9
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(285, 500), (315, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([285,315]))
                recKeys.append(keyID)

            elif 315 <= cx1 <= 345 and 500 <= cy1:
                keyID = 10
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(300, 500), (360, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([300, 360]))
                recKeys.append(keyID)

            elif 345 <= cx1 <= 375 and 500 <= cy1:
                keyID = 11
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(345, 500), (375, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([345, 375]))
                recKeys.append(keyID)

            elif 375 <= cx1 <= 420 and 500 <= cy1:
                keyID = 12
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(360, 500), (420, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([360, 420]))
                recKeys.append(keyID)

            elif 420 <= cx1 <= 465 and 500 <= cy1:
                keyID = 13
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(420, 500), (480, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([420, 480]))
                recKeys.append(keyID)

            elif 465 <= cx1 <= 495 and 500 <= cy1:
                keyID = 14
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(465, 500), (495, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([465, 495]))
                recKeys.append(keyID)

            elif 495 <= cx1 <= 525 and 500 <= cy1:
                keyID = 15
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(480, 500), (540, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([480, 540]))
                recKeys.append(keyID)

            elif 525 <= cx1 <= 555 and 500 <= cy1:
                keyID = 16
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(525, 500), (555, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([525, 555]))
                recKeys.append(keyID)

            elif 555 <= cx1 <= 600 and 500 <= cy1:
                keyID = 17
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(540, 500), (600, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([540, 600]))
                recKeys.append(keyID)

            elif 600 <= cx1 <= 645 and 500 <= cy1:
                keyID = 18
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(600, 500), (660, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([600, 660]))
                recKeys.append(keyID)

            elif 645 <= cx1 <= 675 and 500 <= cy1:
                keyID = 19
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(645, 500), (675, 650), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([645, 675]))
                recKeys.append(keyID)
            
            elif 675 <= cx1 <= 705 and 500 <= cy1:
                keyID = 20
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(660, 500), (720, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([660, 720]))
                recKeys.append(keyID)

            elif 705 <= cx1 <= 735 and 500 <= cy1:
                keyID = 21
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(705, 500), (735, 645), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([705, 735]))
                recKeys.append(keyID)

            elif 735 <= cx1 <= 765 and 500 <= cy1:
                keyID = 22
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(720, 500), (780, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([720, 780]))
                recKeys.append(keyID)

            elif 765 <= cx1 <= 795 and 500 <= cy1:
                keyID = 23
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(765, 500), (795, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([765, 795]))
                recKeys.append(keyID)

            elif 795 <= cx1 <= 840 and 500 <= cy1:
                keyID = 24
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(780, 500), (840, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([780, 840]))
                recKeys.append(keyID)
                
            elif 840 <= cx1 <= 885 and 500 <= cy1:
                keyID = 25
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(840, 500), (900, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([840, 900]))
                recKeys.append(keyID)

            elif 885 <= cx1 <= 915 and 500 <= cy1:
                keyID = 26
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(885, 500), (915, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([885, 915]))
                recKeys.append(keyID)

            elif 915 <= cx1 <= 945 and 500 <= cy1:
                keyID = 27
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(900, 500), (960, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([900, 960]))
                recKeys.append(keyID)
            
            elif 945 <= cx1 <= 975 and 500 <= cy1:
                keyID = 28
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(945, 500), (975, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([945, 975]))
                recKeys.append(keyID)

            elif 975 <= cx1 <= 1020 and 500 <= cy1:
                keyID = 29
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(960, 500), (1020, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([960, 1020]))
                recKeys.append(keyID)
            
            elif 1020 <= cx1 <= 1065 and 500 <= cy1:
                keyID = 30
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1020, 500), (1080, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1020, 1080]))
                recKeys.append(keyID)

            elif 1065 <= cx1 <= 1095 and 500 <= cy1:
                keyID = 31
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1065, 500), (1095, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1065, 1095]))
                recKeys.append(keyID)
            
            elif 1095 <= cx1 <= 1125 and 500 <= cy1:
                keyID = 32
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1080, 500), (1140, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1080, 1140]))
                recKeys.append(keyID)
            
            elif 1125 <= cx1 <= 1155 and 500 <= cy1:
                keyID = 33
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1125, 500), (1155, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1125, 1155]))
                recKeys.append(keyID)

            elif 1155 <= cx1 <= 1185 and 500 <= cy1:
                keyID = 34
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1140, 500), (1200, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1140, 1200]))
                recKeys.append(keyID)

            elif 1185 <= cx1 <= 1215 and 500 <= cy1:
                keyID = 35
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1185, 500), (1215, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1185, 1215]))
                recKeys.append(keyID)

            elif 1215 <= cx1 <= 1260 and 500 <= cy1:
                keyID = 36
                _thread.start_new_thread(play.play_audio,(keyID,keys))
                cv2.rectangle(img,(1200, 500), (1260, 700), (0, 0, 255), 2)
                keyPressed.append(keyID)
                keysCo[keyID] = keysCo.get(keyID,1) + 1
                coordinates.append(tuple([1200, 1260]))
                recKeys.append(keyID)

        cv2.imshow('Cam', img)
        if cv2.getWindowProperty('Cam',cv2.WND_PROP_VISIBLE) < 1:        
            break
        cv2.waitKey(10)
    cv2.destroyAllWindows()

def playOutput():
    curr_directory = os.getcwd()
    os.chdir(curr_directory)
    filename = askopenfilename()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def popUp():
    try:
        root = Toplevel()
        root.minsize(500,500)
        root.title("Air piano")
        listofsongs = []
        index = 0
        # path = "piano.jpg"
        # img = Image.open(path)
        # img=img.resize((250,250),Image.ANTIALIAS)
        # img2 = ImageTk.PhotoImage(img)
        # panel = Label(root, image = img2)
        # panel.pack(side = "bottom", fill = "both", expand = "no")
        img4 = PhotoImage(file="game.png")
        button1 = Button(root,text="",image=img4,compound=CENTER,command=gm.playGame)
        button1.image = img4
        button1.pack(side = TOP)
        img3 = PhotoImage(file="play.png")
        button2 = Button(root,text="",image=img3,compound=CENTER,command=play.playWrapper)
        button2.image = img3        
        button2.pack(side = TOP)
        img2 = PhotoImage(file="solo.png")
        button3 = Button(root,text="",image=img2,compound=CENTER,command=video)
        button3.image = img2        
        button3.pack(side = TOP)
        img1 = PhotoImage(file="start.png")
        button4 = Button(root,text="",image=img1,compound=CENTER,command= lambda:example.start_audio_recording())
        button4.image = img1        
        button4.pack(side = TOP)
        img = PhotoImage(file="stop.png")
        button5 = Button(root,text="",image=img,compound=CENTER,command= lambda:example.stop_AVrecording())
        button5.image = img  
        button5.pack(side = TOP)
    except Exception as e:
        print(e)
        
        
if __name__ == "__main__":

    try:
        from tkinter import *
        from tkinter.filedialog import askopenfilename
        import pygame
        import os
        from PIL import Image, ImageFilter, ImageTk
        # run(300,600)
        from tkinter import messagebox
        run(800,400)
        _thread.exit()
    except (SystemExit):
        cv2.destroyAllWindows()
        pygame.quit()