"""
Módulo de interpolação por Krigagem Ordinária utilizando PyKrige.

Este módulo implementa o método de interpolação geoestatística conhecido como
Krigagem Ordinária, que estima valores em pontos desconhecidos considerando
a estrutura espacial de correlação dos dados através de variogramas.

Características principais:
- Suporte a diferentes modelos de variograma
- Configuração de anisotropia
- Cálculo de variância de estimativa
- Personalização avançada de parâmetros

Classes:
    - Krigagem: Interpolador por Krigagem Ordinária.

Dependências:
    - numpy: Para operações numéricas eficientes
    - pykrige: Implementação de algoritmos de Krigagem
"""

import logging
from typing import Any, Dict, Optional, Tuple, Union

import numpy as np # noqa: F401
from pykrige.ok import OrdinaryKriging

from interpoladores.config import KrigagemConfig
from utils.logging_utils import InterpoladorLogger

from .base import InterpoladorBase


class Krigagem(InterpoladorBase):
    """
    Interpolador via Krigagem Ordinária utilizando PyKrige.

    A Krigagem Ordinária é um método geoestatístico que interpola valores
    desconhecidos com base na correlação espacial entre pontos conhecidos,
    modelada através de variogramas. Este método fornece não apenas estimativas
    dos valores, mas também a variância associada a cada estimativa.

    Permite interpolação geoestatística configurando:
    - Modelo de variograma
    - Parâmetros de anisotropia
    - Configurações avançadas do variograma
    - Opção de retornar estatísticas de erro

    Args:
        x (list or np.ndarray): Coordenadas X dos pontos amostrados.
        y (list or np.ndarray): Coordenadas Y dos pontos amostrados.
        z (list or np.ndarray): Valores associados aos pontos.
        config (KrigagemConfig, optional): Configuração da Krigagem.
            Default usa parâmetros padrões.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Example:
        >>> from interpoladores.krigagem import Krigagem
        >>> from interpoladores.config import KrigagemConfig
        >>> import numpy as np
        >>>
        >>> # Pontos conhecidos
        >>> x = [0, 5, 10, 8, 3, 5]
        >>> y = [0, 5, 10, 8, 3, 10]
        >>> z = [10, 15, 20, 18, 12, 16]
        >>>
        >>> # Grade para interpolação
        >>> gridx = np.linspace(0, 10, 20)
        >>> gridy = np.linspace(0, 10, 20)
        >>>
        >>> # Configuração personalizada
        >>> config = KrigagemConfig(
        ...     modelo_variograma='exponential',
        ...     anisotropy_angle=45.0,
        ...     enable_statistics=True
        ... )
        >>>
        >>> # Interpolação
        >>> krig = Krigagem(x, y, z, config=config)
        >>> z_interp, variancia = krig.interpolar(gridx, gridy)
    """

    def __init__(
        self,
        x: Union[list, np.ndarray],
        y: Union[list, np.ndarray],
        z: Union[list, np.ndarray],
        *,
        config: KrigagemConfig = None,
        verbose: bool = False,
        arquivo_log: Optional[str] = None,
    ):
        """
        Inicializa o interpolador de Krigagem.

        Args:
            x (list or np.ndarray): Coordenadas X dos pontos amostrados.
            y (list or np.ndarray): Coordenadas Y dos pontos amostrados.
            z (list or np.ndarray): Valores associados aos pontos.
            config (KrigagemConfig, optional): Configuração da Krigagem.
                Se None, usa configuração padrão. Default é None.
            verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
            arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
                Default é None.
        """
        # Validação de entrada
        if len(x) != len(y) or len(x) != len(z):
            raise ValueError(
                f"Dimensões incompatíveis: x({len(x)}), y({len(y)}), z({len(z)})"
            )

        if len(x) < 3:
            raise ValueError(
                f"Krigagem requer pelo menos 3 pontos, mas recebeu {len(x)}"
            )

        self.x = np.asarray(x)
        self.y = np.asarray(y)
        self.z = np.asarray(z)
        self.config = config if config is not None else KrigagemConfig()

        # Configura o logger
        nivel_log = logging.DEBUG if verbose else logging.INFO
        self.logger = InterpoladorLogger(
            "Krigagem", nivel=nivel_log, arquivo_log=arquivo_log, console=verbose
        )

    def interpolar(
        self, gridx: np.ndarray, gridy: np.ndarray
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Executa a Krigagem Ordinária sobre a grade fornecida.

        Args:
            gridx (np.ndarray): Meshgrid das coordenadas X da grade.
            gridy (np.ndarray): Meshgrid das coordenadas Y da grade.

        Returns:
            Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
                Se enable_statistics=False (padrão): Grade 2D com os valores interpolados.
                Se enable_statistics=True: Tupla com (grade interpolada, variância de estimativa).

        Raises:
            ValueError: Se houver problema na execução da Krigagem (e.g. pontos insuficientes).
        """
        # Inicia o logging
        self.logger.iniciar_interpolacao(
            f"Pontos: {len(self.x)}, Grade: {gridx.shape}, "
            f"Modelo: {self.config.modelo_variograma}"
        )

        try:
            # Validação da grade
            if gridx.shape != gridy.shape:
                raise ValueError(
                    f"Grades X e Y devem ter o mesmo formato, mas têm formatos {gridx.shape} e {gridy.shape}"
                )

            self.logger.registrar_progresso(10, "Validação concluída")

            # Preparação dos parâmetros para o PyKrige
            kwargs = {
                "variogram_model": self.config.modelo_variograma,
                "verbose": self.config.verbose,
                "anisotropy_angle": self.config.anisotropy_angle,
                "anisotropy_scaling": self.config.anisotropy_ratio,
            }

            # Adiciona parâmetros opcionais se fornecidos
            if self.config.nlags is not None:
                kwargs["nlags"] = self.config.nlags

            if self.config.variogram_model_parameters is not None:
                kwargs["variogram_model_parameters"] = (
                    self.config.variogram_model_parameters
                )

            self.logger.registrar_progresso(
                20, f"Parâmetros configurados: {self.config.modelo_variograma}"
            )

            # Executa a Krigagem
            try:
                self.logger.registrar_progresso(30, "Iniciando cálculo do variograma")
                ok = OrdinaryKriging(self.x, self.y, self.z, **kwargs)
                self.logger.registrar_progresso(
                    60, "Variograma calculado, iniciando interpolação"
                )

                z_interp, ss = ok.execute("grid", gridx, gridy)

                self.logger.registrar_progresso(90, "Interpolação concluída")

                # Retorna com ou sem estatísticas conforme configuração
                if self.config.enable_statistics:
                    self.logger.concluir_interpolacao(
                        f"Grade interpolada: {z_interp.shape}, com estatísticas"
                    )
                    return z_interp, ss
                else:
                    self.logger.concluir_interpolacao(
                        f"Grade interpolada: {z_interp.shape}"
                    )
                    return z_interp

            except Exception as e:
                raise ValueError(f"Erro na execução da Krigagem: {str(e)}")

        except Exception as e:
            self.logger.registrar_erro(e)
            raise
