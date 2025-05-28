"""
Módulo de interpolação por Krigagem Ordinária utilizando PyKrige.

Este módulo fornece a classe Krigagem para realizar interpolação
geoestatística sobre uma grade regular, com diferentes modelos de variograma.

Classes:
    - Krigagem: Interpolador por Krigagem Ordinária.

Dependências:
    - numpy
    - pykrige
"""

from pykrige.ok import OrdinaryKriging
import numpy as np
from interpoladores.config import KrigagemConfig
from .base import InterpoladorBase


class Krigagem(InterpoladorBase):
    """
    Interpolador via Krigagem Ordinária utilizando PyKrige.

    Permite interpolação geoestatística configurando o modelo de variograma.

    Args:
        x (list or np.ndarray): Coordenadas X dos pontos amostrados.
        y (list or np.ndarray): Coordenadas Y dos pontos amostrados.
        z (list or np.ndarray): Valores associados aos pontos.
        modelo_variograma (str, optional): Modelo de variograma a ser usado.
            Padrão é 'spherical'. Outros modelos suportados incluem
            'linear', 'gaussian', 'exponential' e 'power'.

    Example:
        >>> krig = Krigagem(x, y, z, modelo_variograma='exponential')
        >>> z_interp = krig.interpolar(grid_x, grid_y)
    """

    def __init__(self, x: list, y: list, z: list, *, modelo_variograma: str = 'spherical'):
        self.x = x
        self.y = y
        self.z = z
        self.modelo_variograma = modelo_variograma

    def interpolar(self, gridx: np.ndarray, gridy: np.ndarray) -> np.ndarray:
        """
        Executa a Krigagem Ordinária sobre a grade fornecida.

        Args:
            gridx (np.ndarray): Meshgrid das coordenadas X da grade.
            gridy (np.ndarray): Meshgrid das coordenadas Y da grade.

        Returns:
            np.ndarray: Grade 2D com os valores interpolados.

        Raises:
            ValueError: Se houver problema na execução da Krigagem (e.g. pontos insuficientes).
        """
        ok = OrdinaryKriging(
            self.x, self.y, self.z,
            variogram_model=self.modelo_variograma,
        )
        z_interp, ss = ok.execute("grid", gridx, gridy)
        return z_interp
