import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from interpoladores.krigagem import Krigagem

def test_krigagem_simples():
    # Pontos amostrados
    x = [0, 10, 20]
    y = [0, 10, 20]
    z = [1.0, 2.0, 3.0]

    # Grade de teste
    gridx = np.linspace(0, 20, 5)
    gridy = np.linspace(0, 20, 5)

    krig = Krigagem(x, y, z, modelo_variograma='linear')
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert np.all(np.isfinite(zi))
    assert np.min(zi) >= 1.0
    assert np.max(zi) <= 3.0

