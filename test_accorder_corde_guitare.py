from Accorder_guitare import *

def test_trouve_freq_souhaitee():
    assert trouve_freq_souhaitee(429.7)==(1,329.6)
    assert trouve_freq_souhaitee(329.6)==(1,329.6)
    assert trouve_freq_souhaitee(280.0)==(2,246.9)
    assert trouve_freq_souhaitee(246.9)==(2,246.9)
    assert trouve_freq_souhaitee(190)==(3,196)
    assert trouve_freq_souhaitee(73.0)==(6,82.4)

test_trouve_freq_souhaitee()

def test_ecart_objectif():
    assert ecart_avec_objectif(429.7)==(100.1,-1)
    assert ecart_avec_objectif(329.6)==(0.0,-1)
    assert ecart_avec_objectif(280.0)==(33.1,-1)
    assert ecart_avec_objectif(246.9)==(0.0,-1)
    assert ecart_avec_objectif(190)==(6.0,1)
    assert ecart_avec_objectif(73.0)==(9.4,1)

test_ecart_objectif()
