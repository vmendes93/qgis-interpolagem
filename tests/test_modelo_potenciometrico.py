import numpy as np
import sys
import os

# Adiciona o diretório pai ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interpoladores.modelo_potenciometrico import calcular_gradiente_superficie



def test_fluxo_gradiente_linear():
    """
    Testa se os vetores de fluxo apontam corretamente para baixo
    numa superfície inclinada linearmente no eixo x.
    """
    # Gera uma grade regular
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 10, 5)
    grid_x, grid_y = np.meshgrid(x, y)

    # Superfície inclinada no eixo x
    z = grid_x.copy()

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    flow_x, flow_y = modelo.calcular_fluxo()

    # Espera-se que o fluxo aponte para -1 na direção x e 0 na direção y
    assert np.allclose(flow_x, -1.0)
    assert np.allclose(flow_y, 0.0)

def test_gradiente_superficie_plano_inclinado():
    # Geração de grade regular
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 10, 5)
    grid_x, grid_y = np.meshgrid(x, y)

    # Superfície Z plana crescente em x (gradiente constante)
    z = grid_x.copy()
    fx, fy = calcular_gradiente_superficie(grid_x, grid_y, z)

    # Espera-se: fx ≈ 1, fy ≈ 0
    np.testing.assert_allclose(fx, 1.0, atol=1e-6)
    np.testing.assert_allclose(fy, 0.0, atol=1e-6)

def test_gradiente_superficie_plano_y():
    # Plano crescente apenas em y
    x = np.linspace(0, 5, 6)
    y = np.linspace(0, 10, 6)
    grid_x, grid_y = np.meshgrid(x, y)

    z = grid_y.copy()

    fx, fy = calcular_gradiente_superficie(grid_x, grid_y, z)

    # Espera-se: fx ≈ 0, fy ≈ 1
    np.testing.assert_allclose(fx, 0.0, atol=1e-6)
    np.testing.assert_allclose(fy, 1.0, atol=1e-6)
