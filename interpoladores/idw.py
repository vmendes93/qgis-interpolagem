"""
Módulo de interpolação IDW (Inverse Distance Weighting).

Este módulo implementa o método de interpolação IDW, que estima valores em pontos
desconhecidos usando uma média ponderada dos valores de pontos conhecidos, onde
o peso diminui com a distância.

Características principais:
- Configuração flexível do expoente de distância
- Controle do número de vizinhos considerados
- Definição de distância máxima de influência
- Tratamento de casos extremos com valores padrão

Classes:
    - IDW: Classe responsável pela interpolação IDW.

Dependências:
    - numpy: Para operações numéricas eficientes
    - scipy.spatial.cKDTree: Para busca eficiente de vizinhos próximos
"""

import logging
from typing import Optional

import numpy as np  # noqa: F401

from interpoladores.config import IDWConfig
from utils.logging_utils import InterpoladorLogger

from scipy.spatial import cKDTree # noqa: F401



class IDW:
    """
    Interpolador baseado no método de Inverso da Distância (IDW).

    O IDW estima valores em pontos desconhecidos calculando uma média ponderada
    dos valores em pontos conhecidos, onde o peso é inversamente proporcional à
    distância elevada a uma potência. Pontos mais próximos têm maior influência
    que pontos mais distantes.

    Permite configurar:
    - Expoente da distância (`power`): Controla a taxa de diminuição da influência com a distância
    - Número de vizinhos (`n_neighbors`): Limita quantos pontos próximos são considerados
    - Distância máxima de influência (`max_distance`): Define um raio máximo de busca
    - Valor padrão (`default_value`): Valor a usar quando não há vizinhos válidos

    Args:
        config (IDWConfig): Configuração do IDW. Default usa parâmetros padrões.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Example:
        >>> from interpoladores.idw import IDW
        >>> from interpoladores.config import IDWConfig
        >>> import numpy as np
        >>>
        >>> # Pontos conhecidos
        >>> pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        >>> valores = np.array([10, 20, 30, 40])
        >>>
        >>> # Grade para interpolação
        >>> x = np.linspace(0, 1, 10)
        >>> y = np.linspace(0, 1, 10)
        >>> grid_x, grid_y = np.meshgrid(x, y)
        >>>
        >>> # Configuração personalizada
        >>> config = IDWConfig(power=2.0, n_neighbors=3)
        >>>
        >>> # Interpolação
        >>> idw = IDW(config)
        >>> z = idw.interpolar(pontos, valores, grid_x, grid_y)
    """

    def __init__(
        self,
        config: IDWConfig = IDWConfig(),
        verbose: bool = False,
        arquivo_log: Optional[str] = None,
    ):
        """
        Inicializa o interpolador IDW.

        Args:
            config (IDWConfig): Objeto de configuração contendo os parâmetros
                                do interpolador (expoente, vizinhos, distância máxima).
            verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
            arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
                Default é None.
        """
        self.config = config

        # Configura o logger
        nivel_log = logging.DEBUG if verbose else logging.INFO
        self.logger = InterpoladorLogger(
            "IDW", nivel=nivel_log, arquivo_log=arquivo_log, console=verbose
        )

    def interpolar(self, pontos, valores, grid_x, grid_y):
        """
        Realiza interpolação IDW sobre uma grade regular.

        O algoritmo:
        1. Valida as dimensões dos dados de entrada
        2. Constrói uma árvore KD para busca eficiente de vizinhos
        3. Para cada ponto da grade, encontra os vizinhos mais próximos
        4. Aplica a distância máxima se configurada
        5. Calcula os pesos baseados no inverso da distância elevada à potência
        6. Calcula a média ponderada dos valores dos vizinhos

        Args:
            pontos (np.ndarray): Array de shape (N, 2) com coordenadas XY dos pontos amostrados.
            valores (np.ndarray): Array de shape (N,) com os valores correspondentes aos pontos.
            grid_x (np.ndarray): Meshgrid com coordenadas X da grade.
            grid_y (np.ndarray): Meshgrid com coordenadas Y da grade.

        Returns:
            np.ndarray: Array 2D (mesmo shape de grid_x) com os valores interpolados.
                Se não houver vizinhos válidos para alguns pontos e default_value
                não estiver configurado, esses pontos terão valor NaN.

        Raises:
            ValueError: Se o número de pontos não for compatível com os valores.
            ValueError: Se os pontos não tiverem formato (N, 2).
            ValueError: Se as grades X e Y tiverem formatos diferentes.
            ValueError: Se não houver pontos válidos para interpolação.
        """
        # Inicia o logging
        self.logger.iniciar_interpolacao(f"Pontos: {pontos.shape[0]}, Grade: {grid_x.shape}")

        try:
            # Validação de entrada
            if pontos.shape[0] != valores.shape[0]:
                raise ValueError(
                    f"Número de pontos ({pontos.shape[0]}) não corresponde ao número de valores ({valores.shape[0]})"
                )

            if pontos.shape[1] != 2:
                raise ValueError(f"Pontos devem ter formato (N, 2), mas têm formato {pontos.shape}")

            if grid_x.shape != grid_y.shape:
                raise ValueError(
                    f"Grades X e Y devem ter o mesmo formato, mas têm formatos {grid_x.shape} e {grid_y.shape}"
                )

            self.logger.registrar_progresso(10, "Validação concluída")

            # Construção da árvore KD para busca eficiente de vizinhos
            tree = cKDTree(pontos)
            xi = np.column_stack((grid_x.ravel(), grid_y.ravel()))

            self.logger.registrar_progresso(20, "Árvore KD construída")

            # Busca de vizinhos
            if self.config.n_neighbors:
                # Limita ao número de vizinhos especificado
                n_neighbors = min(self.config.n_neighbors, len(pontos))
                self.logger.registrar_progresso(
                    30, f"Buscando {n_neighbors} vizinhos para cada ponto da grade"
                )
                dist, idx = tree.query(xi, k=n_neighbors)
            else:
                # Usa todos os pontos disponíveis
                self.logger.registrar_progresso(
                    30,
                    f"Buscando todos os {len(pontos)} pontos para cada ponto da grade",
                )
                dist, idx = tree.query(xi, k=len(pontos))

            self.logger.registrar_progresso(50, "Busca de vizinhos concluída")

            # Aplicação da distância máxima, se configurada
            if self.config.max_distance:
                self.logger.registrar_progresso(
                    60, f"Aplicando distância máxima: {self.config.max_distance}"
                )
                dist = np.where(dist > self.config.max_distance, np.inf, dist)

                # Verifica se há pontos sem vizinhos válidos
                no_valid_neighbors = np.all(np.isinf(dist), axis=1)
                if np.any(no_valid_neighbors):
                    n_invalid = np.sum(no_valid_neighbors)
                    self.logger.registrar_progresso(
                        70, f"{n_invalid} pontos da grade sem vizinhos válidos"
                    )

                    if (
                        hasattr(self.config, "default_value")
                        and self.config.default_value is not None
                    ):
                        # Se um valor padrão foi configurado, usa-o para pontos sem vizinhos
                        z_interp = np.full(xi.shape[0], self.config.default_value, dtype=float)
                        self.logger.registrar_progresso(
                            75,
                            f"Usando valor padrão {self.config.default_value} para pontos sem vizinhos",
                        )
                    else:
                        # Caso contrário, usa NaN para pontos sem vizinhos
                        z_interp = np.full(xi.shape[0], np.nan, dtype=float)
                        self.logger.registrar_progresso(75, "Usando NaN para pontos sem vizinhos")

                    # Processa apenas pontos com vizinhos válidos
                    has_valid_neighbors = ~no_valid_neighbors
                    if not np.any(has_valid_neighbors):
                        raise ValueError(
                            "Nenhum ponto tem vizinhos dentro da distância máxima configurada"
                        )

                    # Continua o processamento apenas para pontos com vizinhos válidos
                    xi_valid = xi[has_valid_neighbors]
                    dist_valid = dist[has_valid_neighbors]
                    idx_valid = idx[has_valid_neighbors]

                    # Recalcula para pontos válidos
                    dist = dist_valid
                    idx = idx_valid

                    # Evita divisão por zero substituindo zeros por valor muito pequeno
                    dist = np.where(dist == 0, 1e-10, dist)

                    # Calcula pesos e interpolação
                    self.logger.registrar_progresso(
                        80, f"Calculando pesos com expoente {self.config.power}"
                    )
                    weights = 1.0 / dist**self.config.power
                    weights /= weights.sum(axis=1, keepdims=True)

                    z_valid = np.sum(weights * valores[idx], axis=1)
                    z_interp[has_valid_neighbors] = z_valid

                    self.logger.registrar_progresso(90, "Interpolação concluída")
                    result = z_interp.reshape(grid_x.shape)

                    self.logger.concluir_interpolacao(
                        f"Grade interpolada: {result.shape}, "
                        f"Valores NaN: {np.sum(np.isnan(result))}"
                    )
                    return result

            # Evita divisão por zero substituindo zeros por valor muito pequeno
            dist = np.where(dist == 0, 1e-10, dist)

            # Calcula pesos e interpolação
            self.logger.registrar_progresso(
                80, f"Calculando pesos com expoente {self.config.power}"
            )
            weights = 1.0 / dist**self.config.power
            weights /= weights.sum(axis=1, keepdims=True)

            z_interp = np.sum(weights * valores[idx], axis=1)
            result = z_interp.reshape(grid_x.shape)

            self.logger.registrar_progresso(100, "Interpolação concluída")

            self.logger.concluir_interpolacao(f"Grade interpolada: {result.shape}")
            return result

        except Exception as e:
            self.logger.registrar_erro(e)
            raise
