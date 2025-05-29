# Referência do Pacote

Esta página documenta as principais classes e métodos disponíveis no Kit de Interpolação.

## Módulo `interpoladores`

### Classe `IDW`

```python
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
```

**Descrição**: Implementa o método de interpolação Inverse Distance Weighting.

**Construtor**:
- `IDW(config: IDWConfig = IDWConfig())`: Inicializa o interpolador IDW com a configuração especificada.

**Métodos**:
- `interpolar(pontos, valores, grid_x, grid_y)`: Realiza a interpolação IDW sobre uma grade regular.
  - `pontos`: Array de shape (N, 2) com coordenadas XY dos pontos amostrados.
  - `valores`: Array de shape (N,) com os valores correspondentes aos pontos.
  - `grid_x`: Meshgrid com coordenadas X da grade.
  - `grid_y`: Meshgrid com coordenadas Y da grade.
  - **Retorno**: Array 2D (mesmo shape de grid_x) com os valores interpolados.

### Classe `IDWConfig`

```python
from interpoladores.config import IDWConfig
```

**Descrição**: Configuração para o algoritmo IDW.

**Atributos**:
- `power`: Expoente da distância. Valores maiores aumentam a influência de pontos próximos. Default é 2.0.
- `n_neighbors`: Número de vizinhos a considerar. Se None, usa todos os pontos. Default é None.
- `max_distance`: Distância máxima para considerar pontos. Se None, não há limite. Default é None.
- `default_value`: Valor padrão para células sem vizinhos válidos. Se None, usa NaN. Default é None.

### Classe `Krigagem`

```python
from interpoladores.krigagem import Krigagem
from interpoladores.config import KrigagemConfig
```

**Descrição**: Implementa o método de interpolação por Krigagem Ordinária.

**Construtor**:
- `Krigagem(x, y, z, *, config=None)`: Inicializa o interpolador de Krigagem.
  - `x`: Coordenadas X dos pontos amostrados.
  - `y`: Coordenadas Y dos pontos amostrados.
  - `z`: Valores associados aos pontos.
  - `config`: Configuração da Krigagem. Se None, usa configuração padrão.

**Métodos**:
- `interpolar(gridx, gridy)`: Executa a Krigagem Ordinária sobre a grade fornecida.
  - `gridx`: Meshgrid das coordenadas X da grade.
  - `gridy`: Meshgrid das coordenadas Y da grade.
  - **Retorno**: Se enable_statistics=False (padrão): Grade 2D com os valores interpolados.
                Se enable_statistics=True: Tupla com (grade interpolada, variância de estimativa).

### Classe `KrigagemConfig`

```python
from interpoladores.config import KrigagemConfig
```

**Descrição**: Configuração para o algoritmo de Krigagem Ordinária.

**Atributos**:
- `modelo_variograma`: Modelo de variograma a ser usado. Opções: 'linear', 'power', 'gaussian', 'spherical', 'exponential'. Default é 'spherical'.
- `nlags`: Número de lags para cálculo do variograma experimental. Se None, usa o valor padrão do PyKrige. Default é None.
- `variogram_model_parameters`: Parâmetros específicos do modelo de variograma. Se None, PyKrige estima automaticamente. Default é None.
- `anisotropy_angle`: Ângulo de anisotropia em graus (0-180). Se 0, assume isotropia. Default é 0.
- `anisotropy_ratio`: Razão de anisotropia. Deve ser >= 1.0. Default é 1.0 (isotropia).
- `verbose`: Se True, exibe informações durante o processamento. Default é False.
- `enable_statistics`: Se True, calcula e retorna estatísticas de erro. Default é False.

### Classe `ModeloPotenciometrico`

```python
from interpoladores.modelo_potenciometrico import ModeloPotenciometrico
```

**Descrição**: Classe para cálculo de vetores de fluxo (modelo potenciométrico) a partir de uma superfície interpolada.

**Construtor**:
- `ModeloPotenciometrico(grid_x, grid_y, z)`: Inicializa o modelo potenciométrico.
  - `grid_x`: Grade de coordenadas X (meshgrid).
  - `grid_y`: Grade de coordenadas Y (meshgrid).
  - `z`: Superfície interpolada.

**Métodos**:
- `calcular_gradiente()`: Calcula o gradiente da superfície z.
  - **Retorno**: Tupla com (grad_x, grad_y) - componentes X e Y do gradiente.
- `calcular_fluxo()`: Calcula os vetores de fluxo (gradiente invertido) da superfície z.
  - **Retorno**: Tupla com (flow_x, flow_y) - componentes X e Y dos vetores de fluxo.

### Função `plotar_vetores_fluxo`

```python
from interpoladores.modelo_potenciometrico import plotar_vetores_fluxo
```

**Descrição**: Plota os vetores de fluxo sobre a grade.

**Parâmetros**:
- `grid_x`: Grade de coordenadas X (meshgrid).
- `grid_y`: Grade de coordenadas Y (meshgrid).
- `fx`: Componente X dos vetores de fluxo.
- `fy`: Componente Y dos vetores de fluxo.
- `title`: Título do gráfico. Default é "Vetores de Fluxo".
- `densidade`: Densidade de vetores a mostrar (1 = todos). Default é 1.
- `escala`: Fator de escala para os vetores. Default é 1.0.
- `cor`: Cor dos vetores. Default é 'blue'.
- `salvar_como`: Caminho para salvar a figura. Se None, não salva. Default é None.

**Retorno**: Objeto Figure do matplotlib com o gráfico gerado.

## Módulo `utils`

### Módulo `grid_utils`

```python
from utils.grid_utils import criar_grade_regular
```

**Descrição**: Utilitários para criação e manipulação de grades.

**Funções**:
- `criar_grade_regular(x_min, x_max, y_min, y_max, nx, ny)`: Cria uma grade regular para interpolação.
  - `x_min`, `x_max`: Limites horizontais da grade.
  - `y_min`, `y_max`: Limites verticais da grade.
  - `nx`, `ny`: Número de pontos nas direções X e Y.
  - **Retorno**: Tupla com (grid_x, grid_y) - meshgrids das coordenadas X e Y.

### Módulo `logging_utils`

```python
from utils.logging_utils import configurar_logger, InterpoladorLogger
```

**Descrição**: Utilitários de logging para monitoramento de progresso dos algoritmos.

**Funções**:
- `configurar_logger(nome, nivel, formato, arquivo_log, console)`: Configura um logger com handlers para console e/ou arquivo.

**Classes**:
- `InterpoladorLogger`: Classe para logging de operações de interpolação.

## Módulo `io_utils`

### Módulo `leitor`

```python
from io_utils.leitor import ler_pontos_csv, ler_pontos_shapefile
```

**Descrição**: Funções para leitura de dados de diferentes formatos.

**Funções**:
- `ler_pontos_csv(arquivo, delimitador, colunas)`: Lê pontos e valores de um arquivo CSV.
- `ler_pontos_shapefile(arquivo, campo_valor)`: Lê pontos e valores de um arquivo Shapefile.

### Módulo `exportador`

```python
from io_utils.exportador import exportar_raster, exportar_vetores
```

**Descrição**: Funções para exportação de resultados em diferentes formatos.

**Funções**:
- `exportar_raster(grid_x, grid_y, z, arquivo_saida, sistema_coord)`: Exporta uma grade interpolada como arquivo raster.
- `exportar_vetores(grid_x, grid_y, fx, fy, arquivo_saida, sistema_coord)`: Exporta vetores de fluxo como arquivo shapefile.
