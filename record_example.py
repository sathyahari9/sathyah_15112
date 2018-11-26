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
        print("callback")
        if self.key_pressed == True:
            #stream_queue.put(in_data)
            print("record")
            frames.append(in_data)
            return (in_data, pyaudio.paContinue)

        elif self.key_pressed == False:
            #stream_queue.put(in_data)
            frames.append(in_data)
            return (in_data, pyaudio.paComplete)

        else:
            print("not record")
            return (in_data,pyaudio.paContinue)


listener = MyListener()
listener.start()
started = False

def record():
    time.sleep(0.1)
    if listener.key_pressed == True and started == False:
        started = True
        listener.stream.start_stream()
        print "*RECORDING"

    elif listener.key_pressed == False and started == True:
        print "*DONE RECRODING"
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

while True:
    time.sleep(0.1)
    record()