# Name - Sathya Hari
# Section - I
# Term project 1 phase
# Project currently implements keys in the form of classes, plays audio files and recognizes fingers

import cv2
import numpy as np
import copy
import pyaudio
import wave
from array import array
from struct import pack
import time
import threading
from queue import Queue
q = Queue

# Display size
conts = []

def play_audio():
    global conts
    while True:
        play_audio_helper()

def play_audio_helper():
    for i in range(0, len(conts)):
        x1, y1, w1, h1 = cv2.boundingRect(conts[i])
        cx1 = int(x1 + w1 / 2)
        cy1 = int(y1 + h1 / 2)
        if 40 <= cx1 <= 80 and 400 <= cy1 <= 600:
            play("c-maj.wav")
        elif 100 <= cx1 <= 140 and 400 <= cy1 <= 600:
            play("c-maj.wav")

def play(file):
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

def video():
    global conts
    lowerBound = np.array([33,80,40])
    higherBound = np.array([102,255,255])

    cam = cv2.VideoCapture(0)
    # Defining kernel sizes for smoothing the image
    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))

    # font for text
    # font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
    play_thread = threading.Thread(target=play_audio)
    play_thread.start()
    while True:
        ret, img = cam.read()
        img = cv2.resize(img,(1250,700))
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

        for i in range(0,22):
            cv2.rectangle(img,(i * 60,400),(i * 60 + 60,700),(255,255,255),thickness=cv2.FILLED)
            cv2.rectangle(img, (i * 60, 400), (i * 60 + 60, 700), (0,0, 0), 1)
        #
        cv2.rectangle(img, (40,400),(80,600),(0,0,0),thickness=cv2.FILLED)
        cv2.rectangle(img, (100, 400), (140, 600), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (220, 400), (260, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (280, 400), (320, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (340, 400), (380, 600), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (460, 400), (500, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (520, 400), (560, 600), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (640, 400), (680, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (700, 400), (740, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (760, 400), (800, 600), (0, 0, 0), thickness=cv2.FILLED)
        #
        cv2.rectangle(img, (880, 400), (920, 600), (0, 0, 0), thickness=cv2.FILLED)
        cv2.rectangle(img, (940, 400), (980, 600), (0, 0, 0), thickness=cv2.FILLED)

        cv2.imshow('MaskFinal', maskFinal)
        cv2.imshow('Cam', img)
        cv2.waitKey(10)

video()