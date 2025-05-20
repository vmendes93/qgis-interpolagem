import pytest
from interpoladores.krigagem import Krigagem
import numpy as np

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
    assert not np.any(np.isnan(zi))

@pytest.mark.parametrize("modelo", ["linear", "exponential", "gaussian", "spherical"])
def test_krigagem_varios_modelos(modelo):
    x = [0, 10, 20]
    y = [0, 10, 20]
    z = [1.0, 2.0, 3.0]
    gridx = np.linspace(0, 20, 5)
    gridy = np.linspace(0, 20, 5)

    krig = Krigagem(x, y, z, modelo_variograma=modelo)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))

def test_krigagem_grade_densa():
    x = [0, 10, 20]
    y = [0, 10, 20]
    z = [1.0, 2.0, 3.0]
    gridx = np.linspace(0, 20, 10)
    gridy = np.linspace(0, 20, 10)

    krig = Krigagem(x, y, z)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (10, 10)
    assert not np.any(np.isnan(zi))

def test_krigagem_pontos_colineares():
    x = [0, 5, 10]
    y = [0, 0, 0]  # linha reta
    z = [1.0, 2.0, 1.5]
    gridx = np.linspace(0, 10, 5)
    gridy = np.linspace(-5, 5, 5)

    krig = Krigagem(x, y, z)
    zi = krig.interpolar(gridx, gridy)

    assert zi.shape == (5, 5)
    assert not np.any(np.isnan(zi))

