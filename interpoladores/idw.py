# interpoladores/idw.py

import numpy as np
from interpoladores.config import IDWConfig
from scipy.spatial import cKDTree

class IDW:
    def __init__(self, config: IDWConfig = IDWConfig()):
        self.config = config

    def interpolar(self, pontos, valores, grid_x, grid_y):
        # Constrói a árvore para vizinhança
        tree = cKDTree(pontos)
        xi = np.column_stack((grid_x.ravel(), grid_y.ravel()))

        # Busca vizinhos
        if self.config.n_neighbors:
            dist, idx = tree.query(xi, k=self.config.n_neighbors)
        else:
            dist, idx = tree.query(xi, k=len(pontos))

        # Evita divisão por zero
        dist = np.where(dist == 0, 1e-10, dist)

        # Peso inverso da distância
        weights = 1.0 / dist**self.config.power
        weights /= weights.sum(axis=1, keepdims=True)

        # Interpolação
        z_interp = np.sum(weights * valores[idx], axis=1)
        return z_interp.reshape(grid_x.shape)

