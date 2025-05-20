from interpoladores.config import IDWConfig
import numpy as np
from scipy.spatial import cKDTree

class IDW:
    """
    Interpolador baseado no método de Inverso da Distância (IDW).

    Permite configurar o expoente da distância, número de vizinhos e
    distância máxima de influência.
    """

    def __init__(self, config: IDWConfig = IDWConfig()):
        self.config = config

    def interpolar(self, pontos, valores, grid_x, grid_y):
        """
        Realiza interpolação IDW em uma grade regular.

        Parâmetros:
            pontos: ndarray de shape (N, 2), coordenadas XY dos pontos de amostra.
            valores: ndarray de shape (N,), valores associados aos pontos.
            grid_x, grid_y: meshgrids com as coordenadas dos nós a serem interpolados.

        Retorna:
            z_interp: ndarray 2D com os valores interpolados na grade.
        """
        tree = cKDTree(pontos)
        xi = np.column_stack((grid_x.ravel(), grid_y.ravel()))

        if self.config.n_neighbors:
            dist, idx = tree.query(xi, k=self.config.n_neighbors)
        else:
            dist, idx = tree.query(xi, k=len(pontos))

        if self.config.max_distance:
            dist = np.where(dist > self.config.max_distance, np.inf, dist)

        dist = np.where(dist == 0, 1e-10, dist)

        weights = 1.0 / dist**self.config.power
        weights /= weights.sum(axis=1, keepdims=True)

        z_interp = np.sum(weights * valores[idx], axis=1)
        return z_interp.reshape(grid_x.shape)

