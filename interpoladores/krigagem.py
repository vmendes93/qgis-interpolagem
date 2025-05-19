from pykrige.ok import OrdinaryKriging
import numpy as np
from .base import InterpoladorBase

class Krigagem(InterpoladorBase):
    def __init__(self, x, y, z, modelo_variograma='spherical'):
        self.x = x
        self.y = y
        self.z = z
        self.modelo_variograma = modelo_variograma

    def interpolar(self, gridx, gridy):
        ok = OrdinaryKriging(
            self.x, self.y, self.z,
            variogram_model=self.modelo_variograma
        )
        z_interp, ss = ok.execute('grid', gridx, gridy)
        return z_interp
