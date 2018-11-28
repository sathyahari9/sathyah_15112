import pyaudio
import wave
from pynput import keyboard

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
print(stream.is_active())       
frames = []

def on_press(key):
    if key == keyboard.Key.cmd_l:
        print('- Started recording -'.format(key))
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except IOError: 
            print('warning: dropped frame')# can replace        with 'pass' if no message desired 
    else:
        print('incorrect character {0}, press     cmd_l'.format(key))


def on_release(key):
    print('{0} released'.format(
    key))
    if key == keyboard.Key.cmd_l:
        print('{0} stop'.format(key))
        keyboard.Listener.stop
        return False

print("* recording")


with keyboard.Listener(on_press=on_press,     on_release=on_release) as listener:
    listener.join()

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