"""
Utilitários de logging para monitoramento de progresso dos algoritmos.

Este módulo fornece funções e classes para facilitar o logging
consistente em todos os algoritmos de interpolação, permitindo
monitorar o progresso, registrar erros e medir o tempo de execução.

Classes:
    - InterpoladorLogger: Classe para logging de operações de interpolação.

Funções:
    - configurar_logger: Configura um logger com handlers para console e/ou arquivo.
"""

import logging
import os
import sys
from datetime import datetime
from typing import List, Optional, Union


def configurar_logger(
    nome: str,
    nivel: int = logging.INFO,
    formato: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    arquivo_log: Optional[str] = None,
    console: bool = True,
) -> logging.Logger:
    """
    Configura um logger com handlers para console e/ou arquivo.

    Args:
        nome (str): Nome do logger.
        nivel (int, optional): Nível de logging. Default é logging.INFO.
        formato (str, optional): Formato das mensagens de log.
        arquivo_log (str, optional): Caminho para o arquivo de log.
            Se None, não salva logs em arquivo. Default é None.
        console (bool, optional): Se True, exibe logs no console.
            Default é True.

    Returns:
        logging.Logger: Logger configurado.
    """
    # Cria o logger
    logger = logging.getLogger(nome)
    logger.setLevel(nivel)

    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Cria o formatador
    formatter = logging.Formatter(formato)

    # Adiciona handler de console se solicitado
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Adiciona handler de arquivo se um caminho for fornecido
    if arquivo_log:
        # Garante que o diretório exista
        os.makedirs(os.path.dirname(os.path.abspath(arquivo_log)), exist_ok=True)

        file_handler = logging.FileHandler(arquivo_log)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class InterpoladorLogger:
    """
    Classe para logging de operações de interpolação.

    Fornece métodos para registrar eventos comuns em algoritmos de interpolação,
    como início, progresso e conclusão, além de medir o tempo de execução.

    Args:
        nome (str): Nome do algoritmo ou módulo.
        nivel (int, optional): Nível de logging. Default é logging.INFO.
        arquivo_log (str, optional): Caminho para o arquivo de log.
            Se None, não salva logs em arquivo. Default é None.
        console (bool, optional): Se True, exibe logs no console.
            Default é True.
    """

    def __init__(
        self,
        nome: str,
        nivel: int = logging.INFO,
        arquivo_log: Optional[str] = None,
        console: bool = True,
    ):
        """
        Inicializa o logger para o interpolador.
        """
        self.nome = nome
        self.logger = configurar_logger(
            nome, nivel, arquivo_log=arquivo_log, console=console
        )
        self.inicio = None

    def iniciar_interpolacao(self, info: Optional[str] = None) -> None:
        """
        Registra o início de uma operação de interpolação.

        Args:
            info (str, optional): Informações adicionais sobre a interpolação.
        """
        self.inicio = datetime.now()
        msg = f"Iniciando interpolação {self.nome}"
        if info:
            msg += f": {info}"
        self.logger.info(msg)

    def registrar_progresso(
        self, percentual: float, info: Optional[str] = None
    ) -> None:
        """
        Registra o progresso de uma operação de interpolação.

        Args:
            percentual (float): Percentual de conclusão (0-100).
            info (str, optional): Informações adicionais sobre o progresso.
        """
        msg = f"Progresso: {percentual:.1f}%"
        if info:
            msg += f" - {info}"
        self.logger.info(msg)

    def concluir_interpolacao(self, info: Optional[str] = None) -> None:
        """
        Registra a conclusão de uma operação de interpolação.

        Args:
            info (str, optional): Informações adicionais sobre a conclusão.
        """
        if self.inicio:
            duracao = datetime.now() - self.inicio
            msg = (
                f"Interpolação {self.nome} concluída em {duracao.total_seconds():.2f}s"
            )
        else:
            msg = f"Interpolação {self.nome} concluída"

        if info:
            msg += f": {info}"
        self.logger.info(msg)

    def registrar_erro(self, erro: Union[str, Exception]) -> None:
        """
        Registra um erro durante a interpolação.

        Args:
            erro (str or Exception): Mensagem de erro ou exceção.
        """
        if isinstance(erro, Exception):
            self.logger.error(f"Erro na interpolação {self.nome}: {str(erro)}")
        else:
            self.logger.error(f"Erro na interpolação {self.nome}: {erro}")
