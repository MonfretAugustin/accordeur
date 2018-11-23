from Note_fondamentale_uniquement_3 import *
from Accorder_guitare3 import *

### Pour Note_fondamentale_3 on ne teste que la fonction freq_max, le reste étant uniquement une écoute du respaberry
def test_freq_max():
    assert

def test_trouve_freq_souhaitee():
    assert trouve_freq_souhaitee(429.7)==(1,329.6)
    assert trouve_freq_souhaitee(329.6)==(1,329.6)
    assert trouve_freq_souhaitee(280.0)==(2,246.9)
    assert trouve_freq_souhaitee(246.9)==(2,246.9)
    assert trouve_freq_souhaitee(190)==(3,196)
    assert trouve_freq_souhaitee(73.0)==(6,82.4)

test_trouve_freq_souhaitee()

def test_minimum ():
    assert minimum([2,5,6,7,5,3,1])==1,6
    assert minimum([2,5,6,7,5,3])==2,0
    assert minimum([4,5,4,3,6,4,6])==4,5

test_minimum()

def test_ecart_obj():
    assert ecart_avec_objectif(329.6,324.0)>=5.5 and ecart_avec_objectif(329.6,324.0)<=5.7
    assert ecart_avec_objectif(246.9,250)>=-3.2 and ecart_avec_objectif(246.9,250)<= -3.0
    assert ecart_avec_objectif(185.4,196)>=

test_ecart_obj()

### reponse_bouton peut-on faire un test ? ###

### accord de la corde pareil ###

def test_test_justesse():
    assert test_justesse(0.2,329.6)==True
    assert test_justesse(10,329.6)==False
    assert ...                              ### à compléter

test_test_justesse()

###accord de la guitare idem ###
