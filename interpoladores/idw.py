"""
Módulo de interpolação IDW (Inverse Distance Weighting).

Este módulo contém a implementação do método de interpolação IDW,
permitindo ajustes no expoente da distância, número de vizinhos e 
distância máxima de influência.

Classes:
    - IDW: Classe responsável pela interpolação IDW.

Dependências:
    - numpy
    - scipy.spatial.cKDTree
"""

from interpoladores.config import IDWConfig
import numpy as np
from scipy.spatial import cKDTree


class IDW:
    """
    Interpolador baseado no método de Inverso da Distância (IDW).

    Permite configurar:
    - Expoente da distância (`power`)
    - Número de vizinhos (`n_neighbors`)
    - Distância máxima de influência (`max_distance`)

    Args:
        config (IDWConfig): Configuração do IDW. Default usa parâmetros padrões.

    Example:
        >>> idw = IDW()
        >>> z = idw.interpolar(pontos, valores, grid_x, grid_y)
    """

    def __init__(self, config: IDWConfig = IDWConfig()):
        """
        Inicializa o interpolador IDW.

        Args:
            config (IDWConfig): Objeto de configuração contendo os parâmetros
                                do interpolador (expoente, vizinhos, distância máxima).
        """
        self.config = config

    def interpolar(self, pontos, valores, grid_x, grid_y):
        """
        Realiza interpolação IDW sobre uma grade regular.

        Args:
            pontos (np.ndarray): Array de shape (N, 2) com coordenadas XY dos pontos amostrados.
            valores (np.ndarray): Array de shape (N,) com os valores correspondentes aos pontos.
            grid_x (np.ndarray): Meshgrid com coordenadas X da grade.
            grid_y (np.ndarray): Meshgrid com coordenadas Y da grade.

        Returns:
            np.ndarray: Array 2D (mesmo shape de grid_x) com os valores interpolados.

        Raises:
            ValueError: Se o número de pontos não for compatível com os valores.
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
