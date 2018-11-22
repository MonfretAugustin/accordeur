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

def minimum(tableau):
        min_=tableau[0]
        k_min=0
        for k in range(len(tableau)):
            if x<=min_:
                min_=tableau[k]
                k_min=k
        return min_,k_min

def ecart_avec_objectif(f_fond,f_ref):    # renvoie l'écart sous la forme (valeur de l'écart, -1 ou 1)  -1 pour diminuer, 1 pour augmenter
    ecart1_2=f_fond - f_ref*2
    ecart_1=f_fond - f_ref
    ecart_2=f_fond - f_ref/2
    ecart_3=f_fond - f_ref/3
    tableau_ecart_abs=[abs(ecart1_2),abs(ecart_1),abs(ecart_2),abs(ecart_3)]
    tableau_ecart=[ecart1_2,ecart_1,ecart_2,ecart_3]
    min_,k_min=minimum(tableau)
    return tableau_ecart[k_min]

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
            print('Tourner la cheville')
            tts.say('Tourner la cheville', lang='fr-FR')       ####### Dire la phrase #######
            if ecart>0 :
                leds.update(Leds.rgb_pattern(Color.BLUE))       #Clignotement bleu pour augmenter pendant 5 secondes
                time.sleep(5)
            else :
                leds.update(Leds.rgb_pattern(Color.RED))        #Clignotement rouge pour diminuer pendant 5 secondes
                time.sleep(5)


def accord_de_la_corde (k) :
    est_juste=False
    while est_juste==False:
        f_fond = Nfu.determine_note_fondamentale()
        f_ref=Liste_frequences[k][1]
        ecart= ecart_avec_objectif(f_fond,f_ref)
        print("L'ecart est de : ", abs(ecart))
        est_juste=test_justesse(ecart,f_ref)
        reponse_bouton(est_juste,ecart)


def test_justesse(ecart,f_ref):
        rapport=(f_ref+abs(ecart))/f_ref
        return (rapport<1.02)
    
def accord_de_la_guitare():
    for k in range (6):
        print ('Accorder la corde suivante')
        tts.say('Accorder la corde suivante', lang='fr-FR')####### De même, phrase à dire #######
        accord_de_la_corde(k)
    print('Guitare accordée')
    tts.say('Guitare accordée',lang='fr-FR')                ####### Idem #######
if __name__=="__main__":
    accord_de_la_corde()
