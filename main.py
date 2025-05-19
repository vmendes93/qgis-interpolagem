import numpy as np
import matplotlib.pyplot as plt

from interpoladores.idw import IDW
from utils.grid_utils import criar_grade

# Dados amostrados (x, y, z)
x = [10, 20, 30, 40]
y = [10, 15, 35, 40]
z = [2.0, 2.5, 1.0, 3.0]

# Criar grade
gridx, gridy = criar_grade(0, 50, 0, 50, resolucao=1)

# Instancia IDW e interpola
idw = IDW(x, y, z, power=2)
zi = idw.interpolar(gridx, gridy)

# Visualiza resultado
plt.figure(figsize=(6, 5))
plt.contourf(gridx, gridy, zi, levels=20, cmap='viridis')
plt.scatter(x, y, c=z, edgecolor='black', cmap='viridis', label='Amostras')
plt.colorbar(label='Valor interpolado')
plt.title("Interpolação IDW (demo)")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.tight_layout()
plt.show()
