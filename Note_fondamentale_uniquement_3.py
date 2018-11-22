import argparse
import time
import wave,struct
import threading
import math
from numpy.fft import fft
import argparse
import sounddevice
from itertools import chain
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.board import Board, Led
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def determine_note_fondamentale():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')
        board.led.state = Led.ON
        board.button.wait_for_press()
        done = threading.Event()
        board.button.when_pressed = done.set
        board.led.state = Led.OFF
        fs = 60000
        duration = 2 # seconds
        myrecording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        print("done recording")
        myrecording2 = list(chain(*myrecording)) #On augmente de façon virtuel la durée du signal pour augmenter la précision de la fft
        

        """def readwave(filename):
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

        recording_name = '../AIY-projects-python/src/examples/voice/recording.wav'"""
        data = myrecording2

        rate = fs


        start = int(0*rate)
        stop = int((0+1)*rate)
        spectre = abs(fft(data[start:stop]))       #Réalise le spectre
        spectre = spectre/spectre.max()                    #Normalise le spectre par rapport à la fondamentale
        spectre2 = list(chain(spectre))                    #Transforme l'array en liste
        freq = []
        n=len(spectre2)
        spectre2 = spectre2[0:20000]		#On coupe les fréquences supérieurs à 20000
        for _ in range(3):

            maxi = spectre2.index(max(spectre2))                #Trouve l'indice de la fréquence max (fondamentale)
            freq.append(1.0/n*rate*maxi)
            for j in range(maxi-60,maxi+60):
                spectre2[j]=0

        print(freq)
        return(2*freq[0])

if __name__=='__main__':
    determine_note_fondamentale()

