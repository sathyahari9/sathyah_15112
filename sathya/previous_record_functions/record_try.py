import wave
import pygame
import pyaudio
import sys
import time
import random
from pynput.keyboard import Key, Listener

# conversion code taken from stack overflow
from time import gmtime, strftime
timePrint = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "recordings/" + timePrint + ".wav"

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)  
                
print(stream.is_active())       
frames = []

def on_press(key):
    if key == keyboard.Key.ctrl:
        stream.stop_stream()
        stream.close()
        p.terminate()
        

def start_record():
    record = True
    while(record == True):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
        with Listener(
        on_press=on_press) as listener:
            listener.join()