import argparse
import time
import threading
import math
import numpy as np
from matplotlib.pyplot import *
import scipy.io.wavfile as wave
from numpy.fft import fft
from itertools import chain
import argparse

from aiy.board import Board
from aiy.voice.audio import AudioFormat, play_wav, record_file, Recorder

def main():
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
        
        def Tracer_spectre(debut,duree,data,rate):
            start = int(0*rate)
            stop = int((0+1)*rate)
            spectre = np.absolute(fft(data[start:stop]))       #Réalise le spectre
            spectre = spectre/spectre.max()                    #Normalise le spectre par rapport à la fondamentale
            spectre2 = list(chain(spectre))                    #Transforme l'array en liste
            maxi = spectre2.index(max(spectre))                #Trouve l'indice de la fréquence max (fondamentale)

            n = spectre.size
            freq = np.zeros(n)
            for k in range(n):
                freq[k] = 1.0/n*rate*k
            vlines(freq,[0],spectre,'r')
            print("La fréquence fondamentale de ce son est : {} Hz".format(freq[maxi]))
            xlabel('f (Hz)')
            ylabel('A')
            axis([0,0.5*rate,0,1])
            grid()
            show()                                              #Trace le sprectre du son (optionnel)

        rate,data = wave.read("recoding.wav")    #Lit le son. Conserve les amplitudes dans la variable data
        n = data.size
        duree = 1.0*n/rate
        a = chain(*data)
        data2 = list(a)
        Tracer_spectre(0,.5,data2,rate)


if __name__ == '__main__':
    main()



