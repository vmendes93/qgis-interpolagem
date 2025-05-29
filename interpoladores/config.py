"""
Configurações para os algoritmos de interpolação.

Este módulo contém classes de configuração para os diferentes
algoritmos de interpolação implementados, permitindo personalização
flexível dos parâmetros sem complicar as interfaces das classes principais.

Classes:
    - IDWConfig: Configuração para interpolação IDW
    - KrigagemConfig: Configuração para interpolação por Krigagem
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class IDWConfig:
    """
    Configuração para o algoritmo IDW (Inverse Distance Weighting).

    Esta classe encapsula todos os parâmetros configuráveis do algoritmo IDW,
    permitindo personalização flexível sem complicar a interface da classe IDW.

    Attributes:
        power (float): Expoente da distância. Valores maiores aumentam a
                      influência de pontos próximos e diminuem a de pontos distantes.
                      Valores típicos estão entre 1 e 3. Default é 2.0.
        n_neighbors (int, optional): Número de vizinhos a considerar na interpolação.
                                    Se None, usa todos os pontos disponíveis. Default é None.
        max_distance (float, optional): Distância máxima para considerar pontos na interpolação.
                                       Pontos além desta distância são ignorados.
                                       Se None, não há limite. Default é None.
        default_value (float, optional): Valor padrão para células sem vizinhos válidos.
                                        Se None, usa NaN. Default é None.
    """

    power: float = 2.0
    n_neighbors: Optional[int] = None
    max_distance: Optional[float] = None
    default_value: Optional[float] = None


@dataclass
class KrigagemConfig:
    """
    Configuração para o algoritmo de Krigagem Ordinária.

    Esta classe encapsula todos os parâmetros configuráveis do algoritmo de Krigagem,
    permitindo personalização avançada sem complicar a interface da classe Krigagem.

    Attributes:
        modelo_variograma (str): Modelo de variograma a ser usado.
            Opções: 'linear', 'power', 'gaussian', 'spherical', 'exponential'.
            Cada modelo representa uma forma diferente de correlação espacial.
            Default é 'spherical'.
        nlags (int, optional): Número de lags para cálculo do variograma experimental.
            Controla a resolução do variograma. Se None, usa o valor padrão do PyKrige.
            Default é None.
        variogram_model_parameters (dict, optional): Parâmetros específicos do modelo de variograma.
            Permite ajuste fino do comportamento do variograma.
            Se None, PyKrige estima automaticamente. Default é None.
        anisotropy_angle (float, optional): Ângulo de anisotropia em graus (0-180).
            Usado quando a correlação espacial varia com a direção.
            Se 0, assume isotropia. Default é 0.
        anisotropy_ratio (float, optional): Razão de anisotropia.
            Representa a proporção entre os eixos maior e menor da elipse de anisotropia.
            Deve ser >= 1.0. Default é 1.0 (isotropia).
        verbose (bool, optional): Se True, exibe informações durante o processamento.
            Útil para depuração. Default é False.
        enable_statistics (bool, optional): Se True, calcula e retorna estatísticas de erro.
            Permite avaliar a incerteza da interpolação. Default é False.
    """

    modelo_variograma: str = "spherical"
    nlags: Optional[int] = None
    variogram_model_parameters: Optional[Dict[str, Any]] = None
    anisotropy_angle: float = 0.0
    anisotropy_ratio: float = 1.0
    verbose: bool = False
    enable_statistics: bool = False
