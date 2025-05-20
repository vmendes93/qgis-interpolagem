import numpy as np
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig

def gerar_grid():
    x = np.linspace(0, 50, 10)
    y = np.linspace(0, 50, 10)
    return np.meshgrid(x, y)

def gerar_amostras():
    pontos = np.array([[10, 10], [20, 15], [30, 35], [40, 40]])
    valores = np.array([1.0, 2.0, 3.0, 3.0])
    return pontos, valores

def test_idw_padrao():
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    idw = IDW()
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert z.shape == grid_x.shape
    assert not np.any(np.isnan(z))

def test_idw_com_n_neighbors():
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config = IDWConfig(n_neighbors=2)
    idw = IDW(config)
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert z.shape == grid_x.shape
    assert not np.any(np.isnan(z))

def test_idw_com_max_distance():
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config = IDWConfig(max_distance=10.0)
    idw = IDW(config)
    z = idw.interpolar(pontos, valores, grid_x, grid_y)

    # Verifica se o shape está correto
    assert z.shape == grid_x.shape

    # Verifica que existem NaNs (porque com max_distance alguns pontos podem não ter vizinhos)
    assert np.isnan(z).any()

    # Verifica que os valores não NaN são válidos (ou seja, interpolação ocorreu onde possível)
    assert np.isfinite(z[~np.isnan(z)]).all()

def test_idw_com_power_diferente():
    pontos, valores = gerar_amostras()
    grid_x, grid_y = gerar_grid()

    config1 = IDWConfig(power=1.0)
    config2 = IDWConfig(power=4.0)

    idw1 = IDW(config1)
    idw2 = IDW(config2)

    z1 = idw1.interpolar(pontos, valores, grid_x, grid_y)
    z2 = idw2.interpolar(pontos, valores, grid_x, grid_y)

    assert not np.allclose(z1, z2)

