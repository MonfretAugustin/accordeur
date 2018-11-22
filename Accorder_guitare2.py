import Note_fondamentale_uniquement_3 as Nfu
import math
import time
from aiy.leds import (Leds, Pattern, PrivacyLed, RgbLeds, Color)
from aiy.voice import tts           ## à voir si ça s'importe de la sorte

Liste_frequences=[(1,329.6),(2,246.9),(3,196),(4,146.8),(5,110),(6,82.4)]  # Liste telle que [(numéro de la corde, fréquence associée en Hz)]  numéro 1 = plus fine, 6 plus grosse

def trouve_freq_souhaitee(frequence):     # trouve la fréquence à obtenir (la plus proche de celle jouée)
    k=0
    while k < 6 and frequence < Liste_frequences[k][1] :   # Parcourt liste afin de trouver la fréquence la plus proche
        k+=1
    if k==0:
        print("la corde choisie est: ",Liste_frequences[0][0])
        return Liste_frequences[0]
    elif k==6:
        print("la corde choisie est : ",Liste_frequences[5][0])
        return Liste_frequences[5]
    else:
        ecart_prec = Liste_frequences[k-1][1] - frequence
        ecart_suiv = frequence - Liste_frequences[k][1]
        if ecart_prec < ecart_suiv :
            print("la corde choisie est: ",Liste_frequences[k-1][0])
            return Liste_frequences[k-1]
        else:
            print("la corde choisie est : ",Liste_frequences[k][0])
            return Liste_frequences[k]

def ecart_avec_objectif(f_fond,f_ref):    # renvoie l'écart sous la forme (valeur de l'écart, -1 ou 1)  -1 pour diminuer, 1 pour augmenter
    ecart = f_fond - f_ref
    if ecart == abs(ecart):
        action = -1
    else :
        action = 1
    return (abs(ecart),action)

def reponse_bouton(est_juste,ecart,action):
    with Leds() as leds :
        if est_juste :
            leds.update(Leds.rgb_on(Color.GREEN))           # Vert fixe pendant 3 secondes si fréquence atteinte
            time.sleep(3)
            print ('Corde accordée')
            tts.say('Corde accordée',lang='fr-FR')          ####### Dire la phrase en plus #######
        else :
            period = 10*ecart
            leds.pattern=Pattern.blink(period)          # donne fréquence de pulsation
            print('Tourner la cheville')
            tts.say('Tourner la cheville', lang='fr-FR')       ####### Dire la phrase #######
            if action == 1 :
                leds.update(Leds.rgb_pattern(Color.BLUE))       #Clignotement bleu pour augmenter pendant 5 secondes
                time.sleep(5)
            else :
                leds.update(Leds.rgb_pattern(Color.RED))        #Clignotement rouge pour diminuer pendant 5 secondes
                time.sleep(5)


def accord_de_la_corde () :
    est_juste=False
    while est_juste==False:
        f_fond = Nfu.determine_note_fondamentale()
        f_ref=trouve_freq_souhaitee(f_fond)[1]
        (ecart,action) = ecart_avec_objectif(f_fond,f_ref)
        print("L'ecart est de : ", ecart)
        est_juste=test_justesse(ecart,f_ref)
        reponse_bouton(est_juste,ecart,action)


def test_justesse(ecart,f_ref):
        rapport=(f_ref+ecart)/f_ref
        return (rapport<1.02)
    
def accord_de_la_guitare():
    for k in range (6):
        print ('Accorder la corde suivante')
        tts.say('Accorder la corde suivante', lang='fr-FR')####### De même, phrase à dire #######
        accord_de_la_corde()
    print('Guitare accordée')
    tts.say('Guitare accordée',lang='fr-FR')                ####### Idem #######
if __name__=="__main__":
    accord_de_la_corde()
