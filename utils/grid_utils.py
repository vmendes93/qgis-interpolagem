"""
Módulo utilitário para geração de grades espaciais.

Fornece funções auxiliares para criar grades regulares de coordenadas,
úteis para interpolação e visualização de superfícies.

Funções:
    - criar_grade: Cria uma grade regular 2D a partir dos limites e resolução.

Dependências:
    - numpy
"""

import numpy as np # noqa: F401


def criar_grade(xmin: float, xmax: float, ymin: float, ymax: float, resolucao: float):
    """
    Cria uma grade regular de coordenadas a partir dos limites definidos.

    Args:
        xmin (float): Valor mínimo no eixo X.
        xmax (float): Valor máximo no eixo X.
        ymin (float): Valor mínimo no eixo Y.
        ymax (float): Valor máximo no eixo Y.
        resolucao (float): Espaçamento entre os pontos da grade (resolução).

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - gridx (np.ndarray): Vetor de coordenadas X.
            - gridy (np.ndarray): Vetor de coordenadas Y.

    Example:
        >>> gridx, gridy = criar_grade(0, 100, 0, 100, 10)
        >>> print(gridx)
        [ 0 10 20 30 40 50 60 70 80 90]
    """
    gridx = np.arange(xmin, xmax, resolucao)
    gridy = np.arange(ymin, ymax, resolucao)
    return gridx, gridy
