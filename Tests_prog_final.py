from Note_fondamentale_uniquement_3 import *
from Accorder_guitare3 import *

### Pour Note_fondamentale_3 on ne teste que la fonction freq_max, le reste étant uniquement une écoute du respaberry
def test_freq_max():
    rate = 60000
    assert freq_max('Data/Re.mp3',rate)>=146 and freq_max('Data/Re.mp3',rate)<= 147.5
    assert freq_max('Data/Sol.mp3',rate)>=195 and freq_max('Data/Sol.mp3',rate) <= 197
    assert freq_max('Data/Si.mp3',rate)>=245 and freq_max('Data/Si.mp3',rate) <= 249
    assert freq_max('Data/Mi aigu.mp3',rate)>=327 and freq_max('Data/Mi aigu.mp3',rate)<=331

def test_trouve_freq_souhaitee():
    assert trouve_freq_souhaitee(429.7)==(1,329.6,"mi aigu")
    assert trouve_freq_souhaitee(329.6)==(1,329.6,"mi aigu")
    assert trouve_freq_souhaitee(280.0)==(2,246.9,"si")
    assert trouve_freq_souhaitee(246.9)==(2,246.9,"si")
    assert trouve_freq_souhaitee(190)==(3,196,"sol")
    assert trouve_freq_souhaitee(73.0)==(6,82.4,"mi grave")

test_trouve_freq_souhaitee()

def test_minimum ():
    assert minimum([2,5,6,7,5,3,1])==1,6
    assert minimum([2,5,6,7,5,3])==2,0
    assert minimum([4,5,4,3,6,4,6])==4,5

test_minimum()

def test_ecart_obj():
    assert ecart_avec_objectif(329.6,324.0)>=5.5 and ecart_avec_objectif(329.6,324.0)<=5.7
    assert ecart_avec_objectif(246.9,250)>=-3.2 and ecart_avec_objectif(246.9,250)<= -3.0
    assert ecart_avec_objectif(185.4,196)>=-11.7 and ecart_avec_objectif(185.4,196)<=-11.5
    

test_ecart_obj()

### reponse_bouton peut-on faire un test ? ###

### accord de la corde pareil ###

def test_test_justesse():
    assert test_justesse(0.2,329.6)==True
    assert test_justesse(10,329.6)==False
    assert ...                              ### à compléter

test_test_justesse()

###accord de la guitare idem ###
