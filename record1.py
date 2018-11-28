from pynput import keyboard
import time
import pyaudio
import wave

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()
frames = []

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

class MyListener(keyboard.Listener):
    def __init__(self):
        super(MyListener, self).__init__(self.on_press, self.on_release)
        self.key_pressed = None

        self.stream = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK,
                             stream_callback = self.callback)
        print self.stream.is_active()

    def on_press(self, key):
        if key == keyboard.Key.cmd_l:
            self.key_pressed = True

    def on_release(self, key):
        if key == keyboard.Key.cmd_l:
            self.key_pressed = False

    def callback(self,in_data, frame_count, time_info, status):
        if self.key_pressed == True:
            return (in_data, pyaudio.paContinue)
        elif self.key_pressed == False:
            return (in_data, pyaudio.paComplete)
        else:
            return (in_data,pyaudio.paAbort)


listener = MyListener()
listener.start()
started = False

def record():
    if listener.key_pressed == True and started == False:
        started = True
        listener.stream.start_stream()
        print "start Stream"

    elif listener.key_pressed == False and started == True:
        print "Something coocked"
        listener.stream.stop_stream()
        listener.stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        started = False