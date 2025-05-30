"""
Módulo para cálculo de vetores de fluxo (modelo potenciométrico)
a partir de uma superfície interpolada.

Este módulo implementa funcionalidades para análise de fluxo em superfícies
potenciométricas, como aquelas encontradas em estudos hidrogeológicos.
Permite calcular gradientes, vetores de fluxo e visualizar os resultados.

Características principais:
- Cálculo de gradiente da superfície
- Cálculo de vetores de fluxo (gradiente negativo)
- Visualização de vetores de fluxo com opções de personalização
- Validação de dados de entrada

Classes:
    - ModeloPotenciometrico: Modelo que calcula os vetores de fluxo.

Funções:
    - plotar_vetores_fluxo: Plota os vetores de fluxo sobre a grade.

Dependências:
    - numpy: Para operações numéricas eficientes
    - matplotlib: Para visualização dos vetores de fluxo
"""

import logging
from dataclasses import dataclass, field
from typing import Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np # noqa: F401

from utils.logging_utils import InterpoladorLogger, configurar_logger


@dataclass
class ModeloPotenciometrico:
    """
    Classe para cálculo de vetores de fluxo (modelo potenciométrico)
    a partir de uma superfície interpolada.

    Em hidrogeologia e outras áreas, o fluxo ocorre na direção do gradiente
    negativo da superfície potenciométrica. Esta classe calcula esse gradiente
    e os vetores de fluxo resultantes para análise e visualização.

    A direção dos vetores de fluxo é baseada no gradiente da superfície,
    apontando de valores altos para valores baixos (gradiente negativo).

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Superfície interpolada.
        verbose (bool, optional): Se True, exibe logs detalhados. Default é False.
        arquivo_log (str, optional): Caminho para arquivo de log. Se None, não salva logs.
            Default é None.

    Methods:
        calcular_fluxo: Calcula os vetores de fluxo (gradiente negativo da superfície).
        calcular_gradiente: Calcula o gradiente da superfície.

    Example:
        >>> import numpy as np
        >>> from interpoladores.modelo_potenciometrico import ModeloPotenciometrico, plotar_vetores_fluxo
        >>>
        >>> # Criar uma grade
        >>> x = np.linspace(0, 10, 20)
        >>> y = np.linspace(0, 10, 20)
        >>> grid_x, grid_y = np.meshgrid(x, y)
        >>>
        >>> # Criar uma superfície com um ponto alto no centro
        >>> centro_x, centro_y = 5, 5
        >>> z = 10 - 0.5 * ((grid_x - centro_x)**2 + (grid_y - centro_y)**2)
        >>>
        >>> # Calcular vetores de fluxo
        >>> modelo = ModeloPotenciometrico(grid_x, grid_y, z)
        >>> flow_x, flow_y = modelo.calcular_fluxo()
        >>>
        >>> # Visualizar os vetores
        >>> plotar_vetores_fluxo(grid_x, grid_y, flow_x, flow_y, densidade=2)
    """

    grid_x: np.ndarray
    grid_y: np.ndarray
    z: np.ndarray
    verbose: bool = False
    arquivo_log: Optional[str] = None
    logger: InterpoladorLogger = field(init=False, repr=False)

    def __post_init__(self):
        """
        Validação após inicialização e configuração do logger.
        """
        # Validação de dimensões
        if self.grid_x.shape != self.grid_y.shape or self.grid_x.shape != self.z.shape:
            raise ValueError(
                f"Dimensões incompatíveis: grid_x({self.grid_x.shape}), "
                f"grid_y({self.grid_y.shape}), z({self.z.shape})"
            )

        # Configura o logger
        nivel_log = logging.DEBUG if self.verbose else logging.INFO
        self.logger = InterpoladorLogger(
            "ModeloPotenciometrico",
            nivel=nivel_log,
            arquivo_log=self.arquivo_log,
            console=self.verbose,
        )

    def calcular_gradiente(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula o gradiente da superfície z.

        O gradiente é um vetor que aponta na direção de maior aumento da função,
        com magnitude proporcional à taxa de variação. É calculado usando
        diferenças finitas centrais.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - grad_x (np.ndarray): Componente X do gradiente.
                - grad_y (np.ndarray): Componente Y do gradiente.
        """
        self.logger.iniciar_interpolacao(
            f"Calculando gradiente para grade de tamanho {self.grid_x.shape}"
        )

        try:
            # Calcula o espaçamento da grade
            dx = np.mean(np.diff(self.grid_x[0]))
            dy = np.mean(np.diff(self.grid_y[:, 0]))

            self.logger.registrar_progresso(
                30, f"Espaçamento da grade: dx={dx:.4f}, dy={dy:.4f}"
            )

            # Calcula o gradiente
            grad_y, grad_x = np.gradient(self.z, dy, dx)

            self.logger.registrar_progresso(100, "Cálculo do gradiente concluído")
            self.logger.concluir_interpolacao()

            return grad_x, grad_y

        except Exception as e:
            self.logger.registrar_erro(e)
            raise

    def calcular_fluxo(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula os vetores de fluxo (gradiente invertido) da superfície z.

        Os vetores de fluxo apontam na direção de maior diminuição da superfície
        (gradiente negativo), representando a direção natural do fluxo de um
        fluido sob a influência do campo potencial.

        Returns:
            Tuple[np.ndarray, np.ndarray]:
                - flow_x (np.ndarray): Componente X dos vetores de fluxo.
                - flow_y (np.ndarray): Componente Y dos vetores de fluxo.
        """
        self.logger.iniciar_interpolacao(
            f"Calculando vetores de fluxo para grade de tamanho {self.grid_x.shape}"
        )

        try:
            # Calcula o gradiente
            self.logger.registrar_progresso(20, "Calculando gradiente")
            grad_x, grad_y = self.calcular_gradiente()

            # Inverte o gradiente para obter o fluxo
            self.logger.registrar_progresso(80, "Invertendo gradiente para obter fluxo")
            flow_x = -grad_x
            flow_y = -grad_y

            self.logger.registrar_progresso(
                100, "Cálculo dos vetores de fluxo concluído"
            )
            self.logger.concluir_interpolacao()

            return flow_x, flow_y

        except Exception as e:
            self.logger.registrar_erro(e)
            raise


# Configura um logger global para as funções
logger_global = configurar_logger("ModeloPotenciometrico_Funcs")


def plotar_vetores_fluxo(
    grid_x: np.ndarray,
    grid_y: np.ndarray,
    fx: np.ndarray,
    fy: np.ndarray,
    title: str = "Vetores de Fluxo",
    densidade: int = 1,
    escala: float = 1.0,
    cor: str = "blue",
    salvar_como: Optional[str] = None,
) -> plt.Figure:
    """
    Plota os vetores de fluxo sobre a grade.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        fx (np.ndarray): Componente X dos vetores de fluxo.
        fy (np.ndarray): Componente Y dos vetores de fluxo.
        title (str, optional): Título do gráfico. Default é "Vetores de Fluxo".
        densidade (int, optional): Densidade de vetores a mostrar (1 = todos). Default é 1.
        escala (float, optional): Fator de escala para os vetores. Default é 1.0.
        cor (str, optional): Cor dos vetores. Default é 'blue'.
        salvar_como (str, optional): Caminho para salvar a figura. Se None, não salva. Default é None.

    Returns:
        plt.Figure: Objeto Figure do matplotlib com o gráfico gerado.
    """
    logger_global.info(
        f"Plotando vetores de fluxo para grade de tamanho {grid_x.shape} "
        f"com densidade {densidade} e escala {escala}"
    )

    try:
        # Validação de dimensões
        if (
            grid_x.shape != grid_y.shape
            or grid_x.shape != fx.shape
            or grid_x.shape != fy.shape
        ):
            erro_msg = (
                f"Dimensões incompatíveis: grid_x({grid_x.shape}), grid_y({grid_y.shape}), "
                f"fx({fx.shape}), fy({fy.shape})"
            )
            logger_global.error(erro_msg)
            raise ValueError(erro_msg)

        # Cria a figura
        fig = plt.figure(figsize=(8, 6))

        # Plota os vetores com a densidade especificada
        plt.quiver(
            grid_x[::densidade, ::densidade],
            grid_y[::densidade, ::densidade],
            fx[::densidade, ::densidade],
            fy[::densidade, ::densidade],
            angles="xy",
            scale_units="xy",
            scale=escala,
            color=cor,
        )

        plt.title(title)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis("equal")
        plt.grid(True)
        plt.tight_layout()

        # Salva a figura se um caminho for especificado
        if salvar_como:
            logger_global.info(f"Salvando figura em {salvar_como}")
            plt.savefig(salvar_como, dpi=300, bbox_inches="tight")

        logger_global.info("Plotagem de vetores de fluxo concluída")
        return fig

    except Exception as e:
        logger_global.error(f"Erro ao plotar vetores de fluxo: {str(e)}")
        raise


# Função legada mantida para compatibilidade com código existente
def calcular_gradiente_superficie(
    grid_x: np.ndarray, grid_y: np.ndarray, z: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula os gradientes da superfície z em relação aos grids dados.

    DEPRECATED: Use ModeloPotenciometrico.calcular_fluxo() em vez disso.

    Args:
        grid_x (np.ndarray): Grade de coordenadas X (meshgrid).
        grid_y (np.ndarray): Grade de coordenadas Y (meshgrid).
        z (np.ndarray): Superfície interpolada.

    Returns:
        Tuple[np.ndarray, np.ndarray]:
            - fx (np.ndarray): Gradiente no eixo X (invertido).
            - fy (np.ndarray): Gradiente no eixo Y (invertido).
    """
    import warnings

    warnings.warn(
        "calcular_gradiente_superficie() está obsoleta. "
        "Use ModeloPotenciometrico.calcular_fluxo() em vez disso.",
        DeprecationWarning,
        stacklevel=2,
    )

    logger_global.warning(
        "Usando função obsoleta calcular_gradiente_superficie(). "
        "Use ModeloPotenciometrico.calcular_fluxo() em vez disso."
    )

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    return modelo.calcular_fluxo()
