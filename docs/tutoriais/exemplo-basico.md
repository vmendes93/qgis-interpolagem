# Exemplo Básico de Interpolação

Este tutorial demonstra como realizar uma interpolação básica usando o Kit de Interpolação para o QGIS.

## Preparação do Ambiente

Primeiro, vamos importar os módulos necessários e configurar o ambiente:

```python
# Importar os módulos necessários
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Importar os módulos do Kit de Interpolação
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
```
## Criação de Dados de Exemplo

Vamos criar alguns dados de exemplo para demonstrar a interpolação:

```python
# Criar pontos de amostra
np.random.seed(42)  # Para reprodutibilidade
n_pontos = 20
x = np.random.rand(n_pontos) * 100
y = np.random.rand(n_pontos) * 100

# Criar valores usando uma função conhecida (para fins de demonstração)
# z = x/10 + y/5 + sin(x/10) * cos(y/10)
z = x/10 + y/5 + np.sin(x/10) * np.cos(y/10)

# Visualizar os pontos de amostra
plt.figure(figsize=(10, 8))
scatter = plt.scatter(x, y, c=z, cmap='viridis', s=100, edgecolor='k')
plt.colorbar(scatter, label='Valor')
plt.title('Pontos de Amostra')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
```
## Criação da Grade para Interpolação

Agora, vamos criar uma grade regular para interpolar os valores:

```python
# Criar uma grade regular
grid_size = 100
grid_x = np.linspace(0, 100, grid_size)
grid_y = np.linspace(0, 100, grid_size)
grid_x, grid_y = np.meshgrid(grid_x, grid_y)
```
## Interpolação com IDW

Vamos usar o método IDW para interpolar os valores na grade:

```python
# Configurar o interpolador IDW
config = IDWConfig(
    power=2.0,           # Expoente da distância
    n_neighbors=5,       # Número de vizinhos a considerar
    max_distance=None    # Sem limite de distância
)

# Criar o interpolador
idw = IDW(config=config)

# Preparar os pontos para interpolação
pontos = np.column_stack((x, y))

# Realizar a interpolação
z_idw = idw.interpolar(pontos, z, grid_x, grid_y)

# Visualizar o resultado
plt.figure(figsize=(12, 10))
plt.contourf(grid_x, grid_y, z_idw, cmap='viridis', levels=50)
plt.scatter(x, y, c=z, cmap='viridis', edgecolor='k', s=80)
plt.colorbar(label='Valor')
plt.title('Interpolação IDW')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
```
## Visualização 3D

Para uma melhor compreensão, vamos criar uma visualização 3D da superfície interpolada:

```python
# Criar visualização 3D
fig = plt.figure(figsize=(14, 12))
ax = fig.add_subplot(111, projection='3d')

# Plotar a superfície
surf = ax.plot_surface(grid_x, grid_y, z_idw, cmap=cm.viridis,
                      linewidth=0, antialiased=True, alpha=0.8)

# Plotar os pontos originais
ax.scatter(x, y, z, c='red', s=50, label='Pontos Originais')

# Configurar o gráfico
ax.set_title('Superfície Interpolada (IDW)')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Valor')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label='Valor')
ax.legend()

plt.tight_layout()
plt.show()
```
## Comparação com Valores Reais

Para avaliar a qualidade da interpolação, vamos comparar os valores interpolados com os valores reais da função:

```python
# Calcular os valores reais na grade usando a mesma função
z_real = grid_x/10 + grid_y/5 + np.sin(grid_x/10) * np.cos(grid_y/10)

# Calcular o erro
erro = z_idw - z_real
erro_abs = np.abs(erro)
erro_medio = np.mean(erro_abs)
erro_max = np.max(erro_abs)

print(f"Erro médio absoluto: {erro_medio:.4f}")
print(f"Erro máximo absoluto: {erro_max:.4f}")

# Visualizar o erro
plt.figure(figsize=(12, 10))
plt.contourf(grid_x, grid_y, erro_abs, cmap='Reds', levels=50)
plt.scatter(x, y, c='black', s=30)
plt.colorbar(label='Erro Absoluto')
plt.title('Erro da Interpolação')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
```
## Próximos Passos

Agora que você aprendeu a realizar uma interpolação básica com o método IDW, pode experimentar:

1. Alterar os parâmetros de configuração (expoente, número de vizinhos, distância máxima)

2. Usar outros métodos de interpolação como a Krigagem

3. Aplicar o modelo potenciométrico para calcular vetores de fluxo

4. Trabalhar com dados reais importados de arquivos CSV ou shapefiles

Consulte os outros tutoriais e a documentação de referência para mais informações.
