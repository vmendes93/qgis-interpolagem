#!/usr/bin/env python3
"""
Script de demonstração para os métodos de interpolação.

Este script permite testar os diferentes métodos de interpolação
disponíveis no pacote, com visualização dos resultados.

Exemplos de uso:
    # Interpolação IDW básica
    python main.py --metodo idw

    # Krigagem com modelo específico
    python main.py --metodo krigagem --modelo spherical

    # Modelo potenciométrico com visualização de vetores de fluxo
    python main.py --metodo potenciometrico --fluxo
"""

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Importações dos módulos de interpolação
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
from interpoladores.krigagem import Krigagem
from interpoladores.config import KrigagemConfig
from interpoladores.modelo_potenciometrico import ModeloPotenciometrico, plotar_vetores_fluxo

# Utilitários
from utils.grid_utils import criar_grade_regular
from utils.logging_utils import configurar_logger, InterpoladorLogger

# Configurar logger
logger = configurar_logger("main", nivel=20)  # INFO=20


def criar_dados_exemplo(n_pontos=10, seed=42):
    """
    Cria dados de exemplo para demonstração.

    Args:
        n_pontos: Número de pontos a gerar
        seed: Semente para reprodutibilidade

    Returns:
        Tupla com (pontos, valores)
    """
    np.random.seed(seed)

    # Coordenadas aleatórias entre 0 e 50
    x = np.random.rand(n_pontos) * 50
    y = np.random.rand(n_pontos) * 50

    # Valores baseados em uma função + ruído
    valores = 2 + 0.05 * x + 0.1 * np.sin(0.1 * x) * np.cos(0.1 * y) + np.random.rand(n_pontos) * 0.5

    # Combinar em array de pontos
    pontos = np.column_stack((x, y))

    return pontos, valores


def interpolar_idw(pontos, valores, grid_x, grid_y, power=2.0, n_neighbors=None, max_distance=None):
    """
    Realiza interpolação IDW.

    Args:
        pontos: Array de pontos (x, y)
        valores: Array de valores
        grid_x, grid_y: Grade para interpolação
        power: Expoente da distância
        n_neighbors: Número de vizinhos
        max_distance: Distância máxima

    Returns:
        Array 2D com valores interpolados
    """
    logger.info(f"Executando interpolação IDW (power={power}, n_neighbors={n_neighbors})")

    config = IDWConfig(
        power=power,
        n_neighbors=n_neighbors,
        max_distance=max_distance
    )

    idw = IDW(config)
    return idw.interpolar(pontos, valores, grid_x, grid_y)


def interpolar_krigagem(pontos, valores, grid_x, grid_y, modelo='spherical'):
    """
    Realiza interpolação por Krigagem.

    Args:
        pontos: Array de pontos (x, y)
        valores: Array de valores
        grid_x, grid_y: Grade para interpolação
        modelo: Modelo de variograma

    Returns:
        Array 2D com valores interpolados
    """
    logger.info(f"Executando Krigagem (modelo={modelo})")

    config = KrigagemConfig(
        modelo_variograma=modelo,
        enable_statistics=True
    )

    krig = Krigagem(pontos[:, 0], pontos[:, 1], valores, config=config)
    z_interp, ss = krig.interpolar(grid_x, grid_y)

    return z_interp, ss


def calcular_modelo_potenciometrico(grid_x, grid_y, z):
    """
    Calcula o modelo potenciométrico.

    Args:
        grid_x, grid_y: Grade para interpolação
        z: Superfície interpolada

    Returns:
        Componentes x e y dos vetores de fluxo
    """
    logger.info("Calculando modelo potenciométrico")

    modelo = ModeloPotenciometrico(grid_x, grid_y, z)
    return modelo.calcular_fluxo()


def visualizar_resultado(grid_x, grid_y, z, pontos, valores, titulo, metodo,
                         fx=None, fy=None, mostrar_fluxo=False, salvar_como=None):
    """
    Visualiza o resultado da interpolação.

    Args:
        grid_x, grid_y: Grade para interpolação
        z: Superfície interpolada
        pontos: Array de pontos (x, y)
        valores: Array de valores
        titulo: Título do gráfico
        metodo: Método de interpolação
        fx, fy: Componentes dos vetores de fluxo (opcional)
        mostrar_fluxo: Se True, mostra vetores de fluxo
        salvar_como: Caminho para salvar a figura
    """
    # Criar figura
    plt.figure(figsize=(10, 8))

    # Definir colormap personalizado
    colors = [(0.0, 'darkblue'), (0.25, 'royalblue'),
              (0.5, 'lightgreen'), (0.75, 'yellow'), (1.0, 'red')]
    cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

    # Plotar superfície interpolada
    contour = plt.contourf(grid_x, grid_y, z, levels=20, cmap=cmap, alpha=0.8)
    plt.colorbar(contour, label='Valor interpolado')

    # Adicionar contornos
    contour_lines = plt.contour(grid_x, grid_y, z, levels=10, colors='black', alpha=0.4, linewidths=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=8, fmt='%.2f')

    # Plotar pontos amostrais
    scatter = plt.scatter(pontos[:, 0], pontos[:, 1], c=valores,
                         s=50, edgecolor='black', cmap=cmap,
                         label='Pontos amostrais')

    # Adicionar vetores de fluxo se solicitado
    if mostrar_fluxo and fx is not None and fy is not None:
        # Reduzir densidade para melhor visualização
        densidade = 3
        plt.quiver(grid_x[::densidade, ::densidade],
                  grid_y[::densidade, ::densidade],
                  fx[::densidade, ::densidade],
                  fy[::densidade, ::densidade],
                  color='darkred', scale=30, width=0.002,
                  label='Vetores de fluxo')

    # Configurar gráfico
    plt.title(titulo, fontsize=14)
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')
    plt.tight_layout()

    # Salvar figura se caminho for fornecido
    if salvar_como:
        plt.savefig(salvar_como, dpi=300, bbox_inches='tight')
        logger.info(f"Figura salva em {salvar_como}")

    # Mostrar figura
    plt.show()


def main():
    """Função principal."""
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description="Demonstração de métodos de interpolação",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Argumentos gerais
    parser.add_argument('--metodo', type=str, default='idw',
                        choices=['idw', 'krigagem', 'potenciometrico'],
                        help='Método de interpolação a utilizar')
    parser.add_argument('--resolucao', type=float, default=0.5,
                        help='Resolução da grade (menor = mais detalhada)')
    parser.add_argument('--n_pontos', type=int, default=15,
                        help='Número de pontos amostrais para dados de exemplo')
    parser.add_argument('--seed', type=int, default=42,
                        help='Semente para geração de dados aleatórios')
    parser.add_argument('--salvar', type=str, default=None,
                        help='Caminho para salvar a figura (ex: resultado.png)')

    # Argumentos específicos para IDW
    idw_group = parser.add_argument_group('Parâmetros IDW')
    idw_group.add_argument('--power', type=float, default=2.0,
                          help='Expoente da distância para IDW')
    idw_group.add_argument('--vizinhos', type=int, default=None,
                          help='Número de vizinhos para IDW')
    idw_group.add_argument('--dist_max', type=float, default=None,
                          help='Distância máxima para IDW')

    # Argumentos específicos para Krigagem
    krig_group = parser.add_argument_group('Parâmetros Krigagem')
    krig_group.add_argument('--modelo', type=str, default='spherical',
                           choices=['spherical', 'exponential', 'gaussian', 'linear'],
                           help='Modelo de variograma para Krigagem')

    # Argumentos específicos para Modelo Potenciométrico
    pot_group = parser.add_argument_group('Parâmetros Modelo Potenciométrico')
    pot_group.add_argument('--fluxo', action='store_true',
                          help='Mostrar vetores de fluxo')

    # Parsear argumentos
    args = parser.parse_args()

    try:
        # Criar dados de exemplo
        pontos, valores = criar_dados_exemplo(n_pontos=args.n_pontos, seed=args.seed)

        # Criar grade regular
        grid_x, grid_y = criar_grade_regular(0, 50, 0, 50,
                                           int(50/args.resolucao),
                                           int(50/args.resolucao))

        # Variáveis para vetores de fluxo
        fx, fy = None, None

        # Executar método selecionado
        if args.metodo == 'idw':
            z = interpolar_idw(pontos, valores, grid_x, grid_y,
                              power=args.power,
                              n_neighbors=args.vizinhos,
                              max_distance=args.dist_max)
            titulo = f"Interpolação IDW (power={args.power})"

            # Calcular vetores de fluxo se solicitado
            if args.fluxo:
                modelo = ModeloPotenciometrico(grid_x, grid_y, z)
                fx, fy = modelo.calcular_fluxo()

        elif args.metodo == 'krigagem':
            z, ss = interpolar_krigagem(pontos, valores, grid_x, grid_y,
                                      modelo=args.modelo)
            titulo = f"Krigagem Ordinária (modelo={args.modelo})"

            # Calcular vetores de fluxo se solicitado
            if args.fluxo:
                modelo = ModeloPotenciometrico(grid_x, grid_y, z)
                fx, fy = modelo.calcular_fluxo()

        elif args.metodo == 'potenciometrico':
            # Para modelo potenciométrico, primeiro interpolar com IDW
            z = interpolar_idw(pontos, valores, grid_x, grid_y, power=2.0)

            # Depois calcular vetores de fluxo
            modelo = ModeloPotenciometrico(grid_x, grid_y, z)
            fx, fy = modelo.calcular_fluxo()
            titulo = "Modelo Potenciométrico"

            # Forçar exibição de vetores de fluxo
            args.fluxo = True

        # Visualizar resultado
        visualizar_resultado(grid_x, grid_y, z, pontos, valores,
                            titulo, args.metodo, fx, fy,
                            mostrar_fluxo=args.fluxo,
                            salvar_como=args.salvar)

    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
