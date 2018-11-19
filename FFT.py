import math
import numpy as np
from matplotlib.pyplot import *
import scipy.io.wavfile as wave
from numpy.fft import fft
from itertools import chain
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--corde", required=True,
                help="chemin du fichier son à étudier")
args = vars(ap.parse_args())                            # Crée la liste des arguments du programme

def Tracer_spectre(debut,duree,data,rate):              #Arguments : 1)date du début de l'enregistrement, 2)durée de l'enregistrement,
                                                                  #  3)variable data contenant les amplitudes (fonction wave.read()),

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

rate,data = wave.read("cordes\{}.wav".format(args["corde"]))    #Lit le son. Conserve les amplitudes dans la variable data
n = data.size
duree = 1.0*n/rate
a = chain(*data)
data2 = list(a)                                                 # Transforme un array en liste
# te = 1.0/rate
# t = np.zeros(n)
# for k in range(n):
#     t[k] = te*k
# figure(figsize=(12,4))
#
# xlabel("t (s)")
# ylabel("amplitude")
# axis([0,2,min(data2),max(data2)])
# plot(t,data2)
# grid()
# show()                                                          #Affiche le son
Tracer_spectre(0,.5,data2,rate)



