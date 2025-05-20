from pykrige.ok import OrdinaryKriging
import numpy as np
from interpoladores.config import KrigagemConfig
from .base import InterpoladorBase

class Krigagem(InterpoladorBase):
    """
    Interpolador via Krigagem Ordinária utilizando PyKrige.
    """
    def __init__(self, x: list, y: list, z: list, *, modelo_variograma: str = 'spherical'):
        self.x = x
        self.y = y
        self.z = z
        self.modelo_variograma = modelo_variograma

    def interpolar(self, gridx, gridy):
        ok = OrdinaryKriging(
            self.x, self.y, self.z,
            variogram_model=self.modelo_variograma,
        )
        z_interp, ss = ok.execute("grid", gridx, gridy)
        return z_interp

