import pyaudio
import wave
from pynput import keyboard
import threading

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) 
frames = []

recordingEvent = threading.Event()    # set to activate recording
exitEvent = threading.Event()         # set to stop recording thread


def on_press(key):
    if key == keyboard.Key.ctrl:
        print('- Started recording -'.format(key))
        recordingEvent.set()
    else:
        print('incorrect character {0}, press cmd_l'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.ctrl:
        print('{0} stop'.format(key))
        recordingEvent.clear()
        keyboard.Listener.stop
        return False


def do_recording():
    while (not exitEvent.is_set()):
        if (recordingEvent.wait(0.1)):
            try:
                data = stream.read(CHUNK)
                # print len(data)
                frames.append(data)
            except IOError: 
                print('warning: dropped frame') # can replace with 'pass' if no message desired 


class myRecorder(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        do_recording()


# start recorder thread
recordingThread = myRecorder()
recordingThread.start()

# monitor keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# stop recorder thread
exitEvent.set()    
recordingThread.join()

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()