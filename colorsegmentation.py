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
def play_audio():
    global conts
    while True:
        for i in range(0,len(conts)):
            x1, y1, w1, h1 = cv2.boundingRect(conts[i])
            cx1 = int(x1 + w1 / 2)
            cy1 = int(y1 + h1 / 2)
            if 0 <= cx1 <= 75 and 400 <= cy1:
                play("piano.wav")
            elif 75 <= cx1 <= 125 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 125 <= cx1 <= 175 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 175 <= cx1 <= 225 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 225 <= cx1 <= 275 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 275 <= cx1 <= 325 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 325 <= cx1 <= 375 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 375 <= cx1 <= 425 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 425 <= cx1 <= 475 and 400 <= cy1:
                play("raw/pianoc1.wav")
            elif 475 <= cx1 <= 525 and 400 <= cy1:
                cv2.rectangle(img,(475, 400), (525, 550), (0, 0, 255), 2)
            elif 525 <= cx1 <= 575 and 400 <= cy1:
                cv2.rectangle(img,(500, 400), (600, 600), (0, 0, 255), 2)
            elif 575 <= cx1 <= 625 and 400 <= cy1:
                cv2.rectangle(img,(575, 400), (625, 550), (0, 0, 255), 2)
            elif 625 <= cx1 <= 675 and 400 <= cy1:
                cv2.rectangle(img,(600, 400), (700, 600), (0, 0, 255), 2)
            elif 675 <= cx1 <= 725 and 400 <= cy1:
                cv2.rectangle(img,(675, 400), (725, 550), (0, 0, 255), 2)
            elif 725 <= cx1 <= 775 and 400 <= cy1:
                cv2.rectangle(img,(700, 400), (800, 600), (0, 0, 255), 2)
            elif 775 <= cx1 <= 825 and 400 <= cy1:
                cv2.rectangle(img,(775, 400), (825, 550), (0, 0, 255), 2)
            elif 825 <= cx1 <= 875 and 400 <= cy1:
                cv2.rectangle(img,(825, 400), (875, 600), (0, 0, 255), 2)
            elif 875 <= cx1 <= 925 and 400 <= cy1:
                cv2.rectangle(img,(825, 400), (925, 550), (0, 0, 255), 2)
            elif 925 <= cx1 <= 1000 and 400 <= cy1:
                cv2.rectangle(img,(925, 400), (1000, 550), (0, 0, 255), 2)
    
    
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

if __name__ == "__main__":
    t1 = threading.Thread(target=play_audio)
    t1.start()
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
        img = cv2.resize(img,(1000,600))
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
        for i in range(0,10):
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
        for i in range(0,len(conts)):
            x1, y1, w1, h1 = cv2.boundingRect(conts[i])
            cx1 = int(x1 + w1 / 2)
            cy1 = int(y1 + h1 / 2)
            if 0 <= cx1 <= 75 and 400 <= cy1:
                cv2.rectangle(img,(0, 400), (100, 600), (0, 0, 255), 2)
            elif 75 <= cx1 <= 125 and 400 <= cy1:
                cv2.rectangle(img,(75, 400), (125, 550), (0, 0, 255), 2)
            elif 125 <= cx1 <= 175 and 400 <= cy1:
                cv2.rectangle(img,(100, 400),(200, 600), (0, 0, 255), 2)
            elif 175 <= cx1 <= 225 and 400 <= cy1:
                cv2.rectangle(img,(175, 400),(225, 550), (0, 0, 255), 2)
            elif 225 <= cx1 <= 275 and 400 <= cy1:
                cv2.rectangle(img,(200, 400), (300, 600), (0, 0, 255), 2)
            elif 275 <= cx1 <= 325 and 400 <= cy1:
                cv2.rectangle(img,(275, 400),(325, 550), (0, 0, 255), 2)
            elif 325 <= cx1 <= 375 and 400 <= cy1:
                cv2.rectangle(img,(300, 400),(400, 600), (0, 0, 255), 2)
            elif 375 <= cx1 <= 425 and 400 <= cy1:
                cv2.rectangle(img,(375, 400), (425, 550), (0, 0, 255), 2)
            elif 425 <= cx1 <= 475 and 400 <= cy1:
                cv2.rectangle(img,(400, 400), (500, 600), (0, 0, 255), 2)
            elif 475 <= cx1 <= 525 and 400 <= cy1:
                cv2.rectangle(img,(475, 400), (525, 550), (0, 0, 255), 2)
            elif 525 <= cx1 <= 575 and 400 <= cy1:
                cv2.rectangle(img,(500, 400), (600, 600), (0, 0, 255), 2)
            elif 575 <= cx1 <= 625 and 400 <= cy1:
                cv2.rectangle(img,(575, 400), (625, 550), (0, 0, 255), 2)
            elif 625 <= cx1 <= 675 and 400 <= cy1:
                cv2.rectangle(img,(600, 400), (700, 600), (0, 0, 255), 2)
            elif 675 <= cx1 <= 725 and 400 <= cy1:
                cv2.rectangle(img,(675, 400), (725, 550), (0, 0, 255), 2)
            elif 725 <= cx1 <= 775 and 400 <= cy1:
                cv2.rectangle(img,(700, 400), (800, 600), (0, 0, 255), 2)
            elif 775 <= cx1 <= 825 and 400 <= cy1:
                cv2.rectangle(img,(775, 400), (825, 550), (0, 0, 255), 2)
            elif 825 <= cx1 <= 875 and 400 <= cy1:
                cv2.rectangle(img,(825, 400), (875, 600), (0, 0, 255), 2)
            elif 875 <= cx1 <= 925 and 400 <= cy1:
                cv2.rectangle(img,(825, 400), (925, 550), (0, 0, 255), 2)
            elif 925 <= cx1 <= 1000 and 400 <= cy1:
                cv2.rectangle(img,(925, 400), (1000, 550), (0, 0, 255), 2)
        cv2.imshow('Cam', img)
        cv2.waitKey(10)
    t1.join()