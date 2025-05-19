import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from interpoladores.idw import IDW

def test_idw_interpola_ponto_unico():
    x = [0]
    y = [0]
    z = [5.0]
    gridx = [0]
    gridy = [0]

    idw = IDW(x, y, z)
    zi = idw.interpolar(gridx, gridy)

    assert zi.shape == (1, 1)
    assert zi[0, 0] == 5.0

def test_idw_interpola_entre_pontos():
    x = [0, 10]
    y = [0, 10]
    z = [0.0, 10.0]
    gridx = [5]
    gridy = [5]

    idw = IDW(x, y, z, power=2)
    zi = idw.interpolar(gridx, gridy)

    assert zi.shape == (1, 1)
    assert 4.0 < zi[0, 0] < 6.0  # valor deve estar entre os dois
