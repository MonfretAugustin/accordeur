import Note_fondamentale_uniquement_3 as Nfu
import math
import time
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.voice import tts           ## à voir si ça s'importe de la sorte
from aiy.pins import PIN_D
from gpiozero import Button
from aiy.board import Board, Led
import sys


Liste_frequences=[(1,329.6,"mi aigu"),(2,246.9,"si"),(3,196,"sol"),(4,146.8,"ré"),(5,110,"la"),(6,82.4,"mi grave")]  # Liste telle que [(numéro de la corde, fréquence associée en Hz)]  numéro 1 = plus fine, 6 plus grosse

def trouve_freq_souhaitee(frequence):     # trouve la fréquence à obtenir (la plus proche de celle jouée)
    k=0
    while k < 6 and frequence < Liste_frequences[k][1] :   # Parcourt liste afin de trouver la fréquence la plus proche
        k+=1
    if k==0:
        tts.say('La corde détectée est {}'.format(Liste_frequences[0][2]), lang='fr-FR')
        print("la corde choisie est: ",Liste_frequences[0][0])
        return Liste_frequences[0]
    elif k==6:
        tts.say('La corde détectée est {}'.format(Liste_frequences[5][2]), lang='fr-FR')
        print("la corde choisie est : ",Liste_frequences[5][0])
        return Liste_frequences[5]
    else:
        ecart_prec = Liste_frequences[k-1][1] - frequence
        ecart_suiv = frequence - Liste_frequences[k][1]
        if ecart_prec < ecart_suiv :
            tts.say('La corde détectée est {}'.format(Liste_frequences[k-1][2]), lang='fr-FR')
            print("la corde choisie est: ",Liste_frequences[k-1][0])
            return Liste_frequences[k-1]
        else:
            tts.say('La corde détectée est {}'.format(Liste_frequences[k][2]), lang='fr-FR')
            print("la corde choisie est : ",Liste_frequences[k][0])
            return Liste_frequences[k]

def minimum(tableau):
        min_=tableau[0]
        k_min=0
        for k in range(len(tableau)):
            if tableau[k]<=min_:
                min_=tableau[k]
                k_min=k
        return min_,k_min

def ecart_avec_objectif(f_fond,f_ref):    # renvoie l'écart sous la forme (valeur de l'écart, -1 ou 1)  -1 pour diminuer, 1 pour augmenter
    ecart = f_fond - f_ref
    return ecart

def reponse_bouton(est_juste,ecart):
    with Leds() as leds :
        if est_juste :
            leds.update(Leds.rgb_on(Color.GREEN))           # Vert fixe pendant 3 secondes si fréquence atteinte
            time.sleep(3)
            print ('Corde accordée')
            tts.say('Corde accordée',lang='fr-FR')          ####### Dire la phrase en plus #######
        else :
            period = 10*abs(ecart)
            leds.pattern=Pattern.blink(period)          # donne fréquence de pulsation
            print("TOURNER LA CHEVILLE")
                 ####### Dire la phrase #######
            if ecart>0 :
                tts.say('Tendre la corde', lang='fr-FR')
                leds.update(Leds.rgb_pattern(Color.BLUE))       #Clignotement bleu pour augmenter pendant 5 secondes
                time.sleep(5)

            else :
                tts.say('Détendre la corde', lang='fr-FR')
                leds.update(Leds.rgb_pattern(Color.RED))        #Clignotement rouge pour diminuer pendant 5 secondes
                time.sleep(5)


def accord_de_la_corde () :
    est_juste=False
    while est_juste==False:
        f_fond = Nfu.determine_note_fondamentale()
        f_liste = trouve_freq_souhaitee(f_fond)
        f_ref=f_liste[1]
        ecart = ecart_avec_objectif(f_fond,f_ref)
        print("L'ecart est de : ", abs(ecart))
        est_juste=test_justesse(ecart,f_ref)
        reponse_bouton(est_juste,ecart)


def test_justesse(ecart,f_ref):
        rapport=(f_ref+abs(ecart))/f_ref
        return (rapport<1.02)
    
def accord_de_la_guitare():
    with Board() as board:
        tts.say("commencer à accorder la guitare", lang='fr-FR')
        print("commencer à accorder la guitare")
        button = Button(PIN_D)
        while True:
            accord_de_la_corde()
            
            tts.say("appuyer sur le bouton", lang='fr-FR')
            button.when_released = continuer
            time.sleep(3)
            tts.say("appuyer sur le bouton pour arrêter sinon le programme continue", lang='fr-FR')
            
            board.led.state = Led.ON
            button.when_pressed = arret
                
            
            time.sleep(3)
            board.led.state = Led.OFF
            

        
            tts.say('Accorder la corde suivante', lang='fr-FR')####### De même, phrase à dire #######
            print ('Accorder la corde suivante')

def arret():
    sys.exit(1)
    
def continuer():
    return None

if __name__=="__main__":
    accord_de_la_guitare()
