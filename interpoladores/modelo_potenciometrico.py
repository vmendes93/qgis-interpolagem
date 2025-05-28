"""
Módulo para cálculo de vetores de fluxo (modelo potenciométrico) 
a partir de uma superfície interpolada.

Este módulo permite:
- Calcular o gradiente da superfície.
- Calcular os vetores de fluxo.
- Plotar visualmente os vetores de fluxo.

Classes:
    - ModeloPotenciometrico: Modelo que calcula os vetores de fluxo.

Funções:
    - calcular_gradiente_superficie: Calcula o gradiente da superfície.
    - plotar_vetores_fluxo: Plota os vetores de fluxo sobre a grade.

Dependências:
    - numpy
    - matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple


@dataclass
class ModeloPotenciometrico:
    """
    Classe para cálculo de vetores de fluxo (modelo potenciométrico)
    a partir de uma superfície interpolada.

    A direção dos vetores de fluxo é baseada no gradiente da superfície.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Superfície interpolada.

    Methods:
        calcular_fluxo: Calcula os vetores de fluxo (gradiente negativo da superfície).
    """
    grid_x: np.ndarray
    grid_y: np.ndarray
    z: np.ndarray

    def calcular_fluxo(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula os vetores de fluxo (gradiente invertido) da superfície z.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - flow_x (np.ndarray): Componente X dos vetores de fluxo.
                - flow_y (np.ndarray): Componente Y dos vetores de fluxo.
        """
        dx = np.mean(np.diff(self.grid_x[0]))
        dy = np.mean(np.diff(self.grid_y[:, 0]))

        grad_y, grad_x = np.gradient(self.z, dy, dx)

        flow_x = -grad_x
        flow_y = -grad_y

        return flow_x, flow_y


def calcular_gradiente_superficie(
    grid_x: np.ndarray, grid_y: np.ndarray, z: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula os gradientes da superfície z em relação aos grids dados.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Superfície interpolada.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - fx (np.ndarray): Gradiente no eixo X (invertido).
            - fy (np.ndarray): Gradiente no eixo Y (invertido).
    """
    dz_dy, dz_dx = np.gradient(z, grid_y[:, 0], grid_x[0])

    fx = -dz_dx
    fy = -dz_dy

    return fx, fy


def plotar_vetores_fluxo(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    fx: np.ndarray,
    fy: np.ndarray,
    title: str = "Vetores de Fluxo",
) -> None:
    """
    Plota os vetores de fluxo sobre a grade.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        fx (np.ndarray): Componente X dos vetores de fluxo.
        fy (np.ndarray): Componente Y dos vetores de fluxo.
        title (str, optional): Título do gráfico. Default é "Vetores de Fluxo".

    Returns:
        None
    """
    plt.figure(figsize=(8, 6))
    plt.quiver(grid_x, grid_y, fx, fy, angles="xy")
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
