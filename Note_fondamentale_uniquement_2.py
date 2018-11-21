import argparse
import time
import wave,struct
import threading
import math
# from matplotlib.pyplot import *
# import scipy.io.wavfile as wave
from numpy.fft import fft
from itertools import chain
import argparse

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def determine_note_fondamentale():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.button.wait_for_press()
        done = threading.Event()
        board.button.when_pressed = done.set

        def wait():
            start = time.monotonic()
            while not done.is_set():
                duration = time.monotonic() - start
                print('Recording: %.02f seconds [Press button to stop]' % duration)
                time.sleep(0.5)
        record_file(AudioFormat.CD, filename=args.filename, wait=wait, filetype='wav')

        def readwave(filename):
            wav = wave.open(filename)
            nchannels = wav.getnchannels()
            nframes = wav.getnframes()
            sampwidth = wav.getsampwidth()
            framerate = wav.getframerate()
            frames = wav.readframes(nframes)

            if sampwidth == 1:
                # 8 bit : unsigned char
                data = struct.unpack('%sB' % (nframes * nchannels), frames)

            elif sampwidth == 2:
                # 16 bits : signed short
	            data = struct.unpack('%sh' % (nframes * nchannels), frames)
            return (data,framerate)
	
	recording_name = "~/AIY-projects-python/src/examples/voice/recording.wav"
        data = list(readwave(recording_name)[0])

        rate = readwave(recording_name)[1]


        start = int(0*rate)
        stop = int((0+1)*rate)
        spectre = math.abs(fft(data[start:stop]))       #Réalise le spectre
        spectre = spectre/spectre.max()                    #Normalise le spectre par rapport à la fondamentale
        spectre2 = list(chain(spectre))                    #Transforme l'array en liste
        maxi = spectre2.index(max(spectre))                #Trouve l'indice de la fréquence max (fondamentale)

        n = spectre.size
        freq = []
        for k in range(n):
            freq.append(1.0/n*rate*k)

        return freq[maxi]

if __name__=='__main__':
    determine_note_fondamentale()

