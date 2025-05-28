import numpy as np
from interpoladores.modelo_potenciometrico import (
    ModeloPotenciometrico,
    calcular_gradiente_superficie,
    plotar_vetores_fluxo,
)


def test_fluxo_gradiente_linear_x():
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 10, 5)
    grid_x, grid_y = np.meshgrid(x, y)

    z = grid_x.copy()

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    flow_x, flow_y = modelo.calcular_fluxo()

    np.testing.assert_allclose(flow_x, -1.0, atol=1e-6)
    np.testing.assert_allclose(flow_y, 0.0, atol=1e-6)


def test_fluxo_gradiente_linear_y():
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 10, 5)
    grid_x, grid_y = np.meshgrid(x, y)

    z = grid_y.copy()

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    flow_x, flow_y = modelo.calcular_fluxo()

    np.testing.assert_allclose(flow_x, 0.0, atol=1e-6)
    np.testing.assert_allclose(flow_y, -1.0, atol=1e-6)


def test_calcular_gradiente_superficie():
    x = np.linspace(0, 5, 6)
    y = np.linspace(0, 5, 6)
    grid_x, grid_y = np.meshgrid(x, y)

    z = grid_x + grid_y

    fx, fy = calcular_gradiente_superficie(grid_x, grid_y, z)

    np.testing.assert_allclose(fx, -1.0, atol=1e-6)
    np.testing.assert_allclose(fy, -1.0, atol=1e-6)


def test_plotar_vetores_fluxo_nao_gera_erro():
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 10, 5)
    grid_x, grid_y = np.meshgrid(x, y)

    z = grid_x + grid_y

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    flow_x, flow_y = modelo.calcular_fluxo()

    try:
        plotar_vetores_fluxo(grid_x, grid_y, flow_x, flow_y, title="Teste de Vetores")
    except Exception as e:
        assert False, f"O plot gerou uma exceção inesperada: {e}"
