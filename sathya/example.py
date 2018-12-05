import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os

from time import gmtime, strftime

# code from stackoverflow modified

class AudioRecorder():
    # Audio class based on pyAudio and Wave
    def __init__(self):

        self.open = True
        self.rate = 4800
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        timePrint = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.audio_filename = "recordings/" + timePrint + ".wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer = self.frames_per_buffer)
        self.audio_frames = []


    # Audio starts being recorded
    def record(self):
        self.stream.start_stream()
        while(self.open == True):
            data = self.stream.read(self.frames_per_buffer) 
            self.audio_frames.append(data)
            if self.open==False:
                break


    # Finishes the audio recording therefore the thread too    
    def stop(self):

        if self.open==True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

        pass

    # Launches the audio recording function using a thread
    def start(self):
        audio_thread = threading.Thread(target=self.record)
        audio_thread.start()

def start_audio_recording():
    print("start")
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()

def stop_AVrecording():

    audio_thread.stop() 
    print("stop")
    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)
