import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple

@dataclass
class ModeloPotenciometrico:
    grid_x: np.ndarray
    grid_y: np.ndarray
    z: np.ndarray

    def calcular_fluxo(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula os vetores de fluxo (gradiente invertido) com base na superfície z.

        Retorna:
            flow_x, flow_y: Arrays 2D representando os vetores de fluxo em cada direção.
        """
        # Calcula espaçamentos uniformes
        dx = np.mean(np.diff(self.grid_x[0]))
        dy = np.mean(np.diff(self.grid_y[:, 0]))

        # Gradiente da superfície
        grad_y, grad_x = np.gradient(self.z, dy, dx)

        # Vetores de fluxo (direção oposta ao gradiente)
        flow_x = -grad_x
        flow_y = -grad_y

        return flow_x, flow_y
    
    def calcular_gradiente_superficie(z: np.ndarray, grid_x: np.ndarray, grid_y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    	"""
    	Calcula os gradientes (vetores de fluxo) da superfície z sobre os grids dados.

    	Retorna:
        	fx, fy: componentes do gradiente (vetores de fluxo) ao longo de x e y
    	"""
    	dz_dy, dz_dx = np.gradient(z, grid_y[:, 0], grid_x[0])  # respeita o shape meshgrid
   	fx = -dz_dx
    	fy = -dz_dy
    	return fx, fy
    	
    def plotar_vetores_fluxo(grid_x: np.ndarray, grid_y: np.ndarray, fx: np.ndarray, fy: np.ndarray, title: str = "Vetores de Fluxo"):
    	"""
    	Plota os vetores de fluxo sobre a grade.

    	Args:
		grid_x, grid_y: arrays meshgrid (saída de np.meshgrid)
		fx, fy: componentes dos vetores de fluxo
		title: título opcional para o gráfico
    	"""
    	plt.figure(figsize=(8, 6))
    	plt.quiver(grid_x, grid_y, fx, fy, angles='xy')
    	plt.title(title)
    	plt.xlabel("X")
    	plt.ylabel("Y")
    	plt.axis("equal")
    	plt.grid(True)
    	plt.tight_layout()
    	plt.show()
