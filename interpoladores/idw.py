import numpy as np
from .base import InterpoladorBase

class IDW(InterpoladorBase):
    def __init__(self, x, y, z, power=2):
        self.x = np.array(x)
        self.y = np.array(y)
        self.z = np.array(z)
        self.power = power

    def interpolar(self, gridx, gridy):
        xi, yi = np.meshgrid(gridx, gridy)
        zi = np.zeros_like(xi)

        for i in range(xi.shape[0]):
            for j in range(xi.shape[1]):
                dx = self.x - xi[i, j]
                dy = self.y - yi[i, j]
                dist = np.sqrt(dx**2 + dy**2)
                weights = 1.0 / np.power(dist, self.power, where=dist!=0)
                weights[dist == 0] = 1e12

                zi[i, j] = np.sum(weights * self.z) / np.sum(weights)
        return zi
