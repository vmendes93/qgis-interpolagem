import numpy as np

def criar_grade(xmin, xmax, ymin, ymax, resolucao):
    gridx = np.arange(xmin, xmax, resolucao)
    gridy = np.arange(ymin, ymax, resolucao)
    return gridx, gridy
