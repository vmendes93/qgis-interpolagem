from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
import numpy as np

def test_idw_parametros_customizados():
    pontos = np.array([[0, 0], [0, 10], [10, 0], [10, 10]])
    valores = np.array([1, 2, 3, 4])
    grid_x, grid_y = np.meshgrid(np.linspace(0, 10, 5), np.linspace(0, 10, 5))

    config = IDWConfig(power=3, n_neighbors=2)
    idw = IDW(config=config)
    resultado = idw.interpolar(pontos, valores, grid_x, grid_y)

    assert resultado.shape == grid_x.shape
