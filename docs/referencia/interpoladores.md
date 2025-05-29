# Referência dos Interpoladores

Esta página documenta em detalhes as classes e métodos disponíveis no módulo de interpoladores.

## Classe IDW

```python
class IDW:
    def __init__(self, config: IDWConfig = IDWConfig()):
        """
        Inicializa o interpolador IDW.

        Args:
            config (IDWConfig): Objeto de configuração contendo os parâmetros
                                do interpolador (expoente, vizinhos, distância máxima).
        """

    def interpolar(self, pontos, valores, grid_x, grid_y):
        """
        Realiza a interpolação IDW.

        Args:
            pontos (np.ndarray): Array de pontos conhecidos com formato (n, 2),
                                onde n é o número de pontos.
            valores (np.ndarray): Array de valores conhecidos com formato (n,).
            grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
            grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).

        Returns:
            np.ndarray: Grade interpolada com o mesmo formato de grid_x e grid_y.

        Raises:
            ValueError: Se os dados de entrada forem incompatíveis ou inválidos.
        """
```
## Classe Krigagem

```python
class Krigagem:
    def __init__(self, x, y, z, config: KrigagemConfig = KrigagemConfig()):
        """
        Inicializa o interpolador de Krigagem.

        Args:
            x (list or np.ndarray): Coordenadas X dos pontos amostrados.
            y (list or np.ndarray): Coordenadas Y dos pontos amostrados.
            z (list or np.ndarray): Valores associados aos pontos.
            config (KrigagemConfig): Configuração da Krigagem.
        """

    def interpolar(self, gridx, gridy):
        """
        Realiza a interpolação por Krigagem Ordinária.

        Args:
            gridx (np.ndarray): Coordenadas X da grade (1D ou meshgrid).
            gridy (np.ndarray): Coordenadas Y da grade (1D ou meshgrid).

        Returns:
            np.ndarray ou tuple:
                - Se enable_statistics=False: Apenas a grade interpolada.
                - Se enable_statistics=True: Tupla (grade_interpolada, variancia).

        Raises:
            ValueError: Se os dados de entrada forem incompatíveis ou inválidos.
        """
```
## Classe ModeloPotenciometrico

```python
class ModeloPotenciometrico:
    def __init__(self, grid_x, grid_y, z):
        """
        Inicializa o modelo potenciométrico.

        Args:
            grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
            grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
            z (np.ndarray): Superfície interpolada.
        """

    def calcular_gradiente(self):
        """
        Calcula o gradiente da superfície.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - grad_x (np.ndarray): Gradiente no eixo X.
                - grad_y (np.ndarray): Gradiente no eixo Y.
        """

    def calcular_fluxo(self):
        """
        Calcula os vetores de fluxo (gradiente negativo da superfície).

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - flow_x (np.ndarray): Componente X do fluxo.
                - flow_y (np.ndarray): Componente Y do fluxo.
        """
```
## Funções Auxiliares

```python
def plotar_vetores_fluxo(grid_x, grid_y, flow_x, flow_y, densidade=1, escala=1.0,
                         cor='blue', title='Vetores de Fluxo'):
    """
    Plota os vetores de fluxo sobre a grade.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        flow_x (np.ndarray): Componente X do fluxo.
        flow_y (np.ndarray): Componente Y do fluxo.
        densidade (int): Densidade dos vetores (1 = todos os pontos).
        escala (float): Fator de escala para os vetores.
        cor (str): Cor dos vetores.
        title (str): Título do gráfico.

    Returns:
        matplotlib.figure.Figure: Figura com o gráfico.
    """
```
## Classes de Configuração

Para detalhes sobre as classes de configuração, consulte a [página de configurações](primeiros-passos.md).
