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

##### Une seule fonction dans ce module qui a pour objectif d'analyser le son émis suite à l'appui sur le bouton et de renvoyer sa fréquence fondamentale #####

def freq_max(data,rate):
            start = int(0*rate)
            stop = int((0+1)*rate)
            spectre = abs(fft(data[start:stop]))               # Réalise le spectre
            spectre = spectre/spectre.max()                    # Normalise le spectre par rapport à la fondamentale
            spectre2 = list(chain(spectre))                    # Transforme l'array en liste
            freq = []
            n=len(spectre2)
            spectre2 = spectre2[0:20000]		                # On coupe les fréquences supérieurs à 20000
            for _ in range(3):

                maxi = spectre2.index(max(spectre2))           # Trouve l'indice de la fréquence max (fondamentale)
                freq.append(1.0/n*rate*maxi)
                for j in range(maxi-60,maxi+60):
                    spectre2[j]=0

            print(freq)
            return(2*freq[0])

def determine_note_fondamentale():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', default='recording.wav')
    args = parser.parse_args()

    with Board() as board:
        print('Press button to start recording.')


        board.led.state = Led.ON            ### allumer la led pour indiquer qu'il faut appuyer sur le bouton
        board.button.wait_for_press()       ### attendre que l'utilisateur appuie sur le bouton
        done = threading.Event()
        board.button.when_pressed = done.set
        board.led.state = Led.OFF           ### eteindre lorsque bouton appuyé
        fs = 60000
        duration = 1       # seconds
        myrecording = sounddevice.rec(int(duration * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        print("done recording")
        myrecording2 = list(chain(*myrecording))*10        # On augmente de façon virtuelle la durée du signal pour augmenter la précision de la fft

        data = myrecording2
        rate = fs

        return freq_max(data,rate)
           

if __name__=='__main__':
    determine_note_fondamentale()

