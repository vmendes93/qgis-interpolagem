# Módulo: interpoladores

Este pacote contém os algoritmos de interpolação utilizados no plugin Kit de Interpolação para o QGIS.

## IDW

Interpolação por Inverso da Distância Ponderada (IDW), que atribui valores com base na distância de pontos amostrados.

**Parâmetros:**
- `power` (float): potência do decaimento da distância. Default é 2.0.
- `n_neighbors` (int): número de vizinhos considerados.
- `max_distance` (float | None): distância máxima para considerar pontos vizinhos.

## Krigagem

Interpolação geoestatística baseada em variogramas teóricos.

**Parâmetros:**
- `modelo_variograma` (str): modelo a ser utilizado ('spherical', 'exponential', 'gaussian').
- `enable_plot` (bool): se `True`, plota o ajuste do variograma.

## Modelo Potenciométrico

Modelo para calcular fluxo com base em gradientes hidráulicos.

**Principais métodos:**
- `calcular_fluxo`: retorna componentes do fluxo baseado no gradiente.
- `plotar_vetores_fluxo`: plota vetores de fluxo em um gráfico.
