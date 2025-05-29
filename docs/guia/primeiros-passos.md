# Primeiros Passos

Este guia apresenta os conceitos básicos para começar a usar o Kit de Interpolação para o QGIS.

## Importando os módulos necessários

Primeiro, importe os módulos necessários:

```python
# Importar algoritmos de interpolação
from interpoladores.idw import IDW
from interpoladores.krigagem import Krigagem
from interpoladores.modelo_potenciometrico import ModeloPotenciometrico

# Importar classes de configuração
from interpoladores.config import IDWConfig, KrigagemConfig

# Bibliotecas auxiliares
import numpy as np
import matplotlib.pyplot as plt
```

## Preparando os dados

Para interpolação, você precisa de:

1. Pontos com coordenadas conhecidas

2. Valores associados a esses pontos

3. Uma grade para interpolação

```python
# Pontos conhecidos (coordenadas x, y)
pontos = np.array([
    [10, 10], [20, 15], [30, 35], [40, 40], [15, 30]
])

# Valores associados aos pontos
valores = np.array([1.0, 2.0, 3.0, 3.0, 2.5])

# Criar uma grade regular para interpolação
x = np.linspace(0, 50, 50)
y = np.linspace(0, 50, 50)
grid_x, grid_y = np.meshgrid(x, y)
```
## Interpolação com IDW

O método IDW (Inverse Distance Weighting) é simples e direto:

```python
# Configurar o IDW
config_idw = IDWConfig(
    power=2.0,           # Expoente da distância
    n_neighbors=3,       # Número de vizinhos a considerar
    max_distance=None    # Sem limite de distância
)

# Criar o interpolador
idw = IDW(config=config_idw)

# Realizar a interpolação
z_idw = idw.interpolar(pontos, valores, grid_x, grid_y)

# Visualizar o resultado
plt.figure(figsize=(10, 8))
plt.contourf(grid_x, grid_y, z_idw, cmap='viridis', levels=20)
plt.scatter(pontos[:, 0], pontos[:, 1], c=valores, cmap='viridis',
            edgecolor='k', s=100)
plt.colorbar(label='Valor')
plt.title('Interpolação IDW')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
```
## Interpolação com Krigagem

A Krigagem é um método geoestatístico mais avançado:

```python
# Preparar dados para Krigagem (x, y, z separados)
x = pontos[:, 0]
y = pontos[:, 1]
z = valores

# Configurar a Krigagem
config_krig = KrigagemConfig(
    modelo_variograma='spherical',  # Modelo de variograma
    enable_statistics=True          # Retornar estatísticas de erro
)

# Criar o interpolador
krig = Krigagem(x, y, z, config=config_krig)

# Realizar a interpolação (retorna valores e variância)
z_krig, var_krig = krig.interpolar(x, y)

# Visualizar o resultado
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Valores interpolados
im1 = ax1.contourf(grid_x, grid_y, z_krig, cmap='viridis', levels=20)
ax1.scatter(x, y, c=z, cmap='viridis', edgecolor='k', s=100)
plt.colorbar(im1, ax=ax1, label='Valor')
ax1.set_title('Krigagem - Valores Interpolados')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')

# Variância (incerteza)
im2 = ax2.contourf(grid_x, grid_y, var_krig, cmap='Reds', levels=20)
ax2.scatter(x, y, c='k', s=50)
plt.colorbar(im2, ax=ax2, label='Variância')
ax2.set_title('Krigagem - Variância (Incerteza)')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')

plt.tight_layout()
plt.show()
```

## Análise de Fluxo com Modelo Potenciométrico

Após interpolar uma superfície, você pode analisar o fluxo:

```python
# Usar a superfície interpolada pelo IDW
modelo = ModeloPotenciometrico(grid_x, grid_y, z_idw)

# Calcular vetores de fluxo
flow_x, flow_y = modelo.calcular_fluxo()

# Visualizar os vetores de fluxo
from interpoladores.modelo_potenciometrico import plotar_vetores_fluxo

fig = plotar_vetores_fluxo(
    grid_x, grid_y, flow_x, flow_y,
    densidade=3,  # Densidade dos vetores
    escala=1.0,   # Escala dos vetores
    cor='blue',   # Cor dos vetores
    title='Vetores de Fluxo'
)
plt.show()
```
## Próximos passos

Para exemplos mais avançados e casos de uso específicos, consulte:

- [Exemplos Práticos]()
- [Tutoriais](exemplo-basico.md)
- [Referência](interpoladores.md)
