# Guia de Início Rápido

Este guia fornece instruções básicas para começar a usar o Kit de Interpolação.

## Pré-requisitos

- Python 3.8 ou superior
- NumPy
- SciPy
- Matplotlib
- PyKrige (para Krigagem)

## Instalação

```bash
# Instale via pip (quando disponível)
pip install qgis-interpolagem

# Ou instale a partir do código fonte
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem
pip install -e .
```

## Uso Básico

### Interpolação IDW

```python
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
import numpy as np
import matplotlib.pyplot as plt

# Dados de exemplo
pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5]])
valores = np.array([10, 20, 30, 40, 50])

# Criar grade para interpolação
x = np.linspace(0, 1, 50)
y = np.linspace(0, 1, 50)
grid_x, grid_y = np.meshgrid(x, y)

# Configurar e executar interpolação
config = IDWConfig(power=2.0, n_neighbors=3)
idw = IDW(config)
z = idw.interpolar(pontos, valores, grid_x, grid_y)

# Visualizar resultado
plt.figure(figsize=(10, 8))
plt.contourf(grid_x, grid_y, z, 20, cmap='viridis')
plt.colorbar(label='Valor')
plt.scatter(pontos[:, 0], pontos[:, 1], c='red', s=50, label='Pontos Amostrais')
plt.title('Interpolação IDW')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
```

### Krigagem

```python
from interpoladores.krigagem import Krigagem
from interpoladores.config import KrigagemConfig
import numpy as np
import matplotlib.pyplot as plt

# Dados de exemplo
x = np.array([0, 1, 0, 1, 0.5])
y = np.array([0, 0, 1, 1, 0.5])
z = np.array([10, 20, 30, 40, 50])

# Criar grade para interpolação
grid_x, grid_y = np.meshgrid(np.linspace(0, 1, 50), np.linspace(0, 1, 50))

# Configurar e executar krigagem
config = KrigagemConfig(modelo_variograma='spherical', enable_statistics=True)
krig = Krigagem(x, y, z, config=config)
z_interp, ss = krig.interpolar(grid_x, grid_y)

# Visualizar resultado
plt.figure(figsize=(10, 8))
plt.contourf(grid_x, grid_y, z_interp, 20, cmap='viridis')
plt.colorbar(label='Valor')
plt.scatter(x, y, c='red', s=50, label='Pontos Amostrais')
plt.title('Krigagem Ordinária')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
```

### Modelo Potenciométrico

```python
from interpoladores.modelo_potenciometrico import ModeloPotenciometrico, plotar_vetores_fluxo
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
import numpy as np

# Dados de exemplo
pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1], [0.5, 0.5]])
valores = np.array([10, 20, 30, 40, 50])

# Criar grade para interpolação
x = np.linspace(0, 1, 20)
y = np.linspace(0, 1, 20)
grid_x, grid_y = np.meshgrid(x, y)

# Interpolar superfície
idw = IDW(IDWConfig(power=2.0))
z = idw.interpolar(pontos, valores, grid_x, grid_y)

# Calcular vetores de fluxo
modelo = ModeloPotenciometrico(grid_x, grid_y, z)
fx, fy = modelo.calcular_fluxo()

# Visualizar vetores de fluxo
fig = plotar_vetores_fluxo(grid_x, grid_y, fx, fy, 
                          title="Vetores de Fluxo", 
                          densidade=2, 
                          escala=20.0)
plt.show()
```

## Próximos Passos

- Explore a [documentação de conceitos](conceitos.md) para entender melhor os métodos de interpolação
- Veja a [referência da API](api.md) para detalhes completos sobre as classes e métodos
- Confira os [exemplos](exemplos.md) para casos de uso mais avançados
