import pyaudio
import wave
from array import array
from struct import pack

# on_press and on release functions taken from stackoverflow.com, modified to work in my context
def on_press(key):
    if key == keyboard.Key.ctrl:
        print('Recording'.format(key))
        record()
    else:
        print('Wrong key {0}, press ctrl'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.ctrl:
        print('{0} stop'.format(key))
        recordingEvent.clear()
        keyboard.Listener.stop
        return False

# reworking record function.
def record(sounds,recKeys):
    sound = []
    if len(recKeys) == 0:
        pass
    else:
        for rec in recKeys:
            sound.append("raw/" + str(sounds[rec]))
        concatenate(sound)

def concatenate(sound):
    infiles = sound
    outfile = "sounds.wav"

    data= []
    for infile in infiles:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    output.writeframes(data[0][1])
    output.writeframes(data[1][1])
    output.close()