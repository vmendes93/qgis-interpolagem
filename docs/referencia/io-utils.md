# Utilitários de E/S

Esta página documenta as funções e classes disponíveis para entrada e saída de dados no Kit de Interpolação.

## Leitura de Dados

### Função `ler_pontos_csv`

```python
def ler_pontos_csv(arquivo, delimitador=',', colunas_xyz=None):
    """
    Lê pontos de um arquivo CSV.

    Args:
        arquivo (str): Caminho para o arquivo CSV.
        delimitador (str, opcional): Delimitador usado no arquivo. Padrão é ','.
        colunas_xyz (list, opcional): Índices das colunas [x, y, z].
                                     Se None, usa as três primeiras colunas.

    Returns:
        tuple: Tupla contendo (x, y, z) como arrays NumPy.
    """
```
### Função `ler_pontos_shapefile`

```python
def ler_pontos_shapefile(arquivo, campo_z=None):
    """
    Lê pontos de um arquivo Shapefile.

    Args:
        arquivo (str): Caminho para o arquivo Shapefile.
        campo_z (str, opcional): Nome do campo que contém os valores Z.
                               Se None, tenta usar 'Z', 'ELEVATION', 'VALUE'.

    Returns:
        tuple: Tupla contendo (x, y, z) como arrays NumPy.
    """
```
## Exportação de Resultados

### Função `exportar_grid_geotiff`

```python
def exportar_grid_geotiff(grid_x, grid_y, z, arquivo_saida,
                         sistema_referencia=None, transformacao=None):
    """
    Exporta uma grade interpolada como arquivo GeoTIFF.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Valores interpolados na grade.
        arquivo_saida (str): Caminho para o arquivo de saída.
        sistema_referencia (str, opcional): Sistema de referência (EPSG, WKT).
        transformacao (list, opcional): Parâmetros de transformação geoespacial.

    Returns:
        bool: True se a exportação foi bem-sucedida.
    """
```
### Função `exportar_grid_ascii`

```python
def exportar_grid_ascii(grid_x, grid_y, z, arquivo_saida):
    """
    Exporta uma grade interpolada como arquivo ASCII Grid.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Valores interpolados na grade.
        arquivo_saida (str): Caminho para o arquivo de saída.

    Returns:
        bool: True se a exportação foi bem-sucedida.
    """
```
## Conversão de Dados

### Função `converter_grade_para_pontos`

```python
def converter_grade_para_pontos(grid_x, grid_y, z):
    """
    Converte uma grade regular em uma lista de pontos.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Valores na grade.

    Returns:
        tuple: Tupla contendo (x, y, z) como arrays 1D.
    """
```
### Função `converter_pontos_para_grade`

```python
def converter_pontos_para_grade(x, y, z, nx, ny,
                              x_min=None, x_max=None,
                              y_min=None, y_max=None):
    """
    Converte pontos irregulares em uma grade regular.

    Args:
        x (np.ndarray): Coordenadas X dos pontos.
        y (np.ndarray): Coordenadas Y dos pontos.
        z (np.ndarray): Valores nos pontos.
        nx (int): Número de células na direção X.
        ny (int): Número de células na direção Y.
        x_min, x_max, y_min, y_max (float, opcional): Limites da grade.
                                                    Se None, usa min/max dos dados.

    Returns:
        tuple: Tupla contendo (grid_x, grid_y, grid_z).
    """
```
