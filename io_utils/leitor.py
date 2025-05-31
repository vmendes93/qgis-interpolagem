"""
Módulo para leitura de dados vetoriais.

Este módulo irá fornecer funções para ler arquivos vetoriais como shapefiles,
GeoJSON, ou camadas diretamente do QGIS.

Funções:
    - ler_pontos: Lê pontos de um arquivo ou camada vetorial e retorna coordenadas e valores.

Status:
    - Ainda não implementado.

Dependências esperadas:
    - geopandas
    - fiona
    - QGIS (opcional)

"""


def ler_pontos(path):
    """
    Lê pontos de um arquivo vetorial (ex.: shapefile, GeoJSON) ou camada QGIS.

    Args:
        path (str): Caminho do arquivo vetorial ou referência da camada no QGIS.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray]:
            - x (np.ndarray): Coordenadas X dos pontos.
            - y (np.ndarray): Coordenadas Y dos pontos.
            - valores (np.ndarray): Valores associados aos pontos.

    Raises:
        NotImplementedError: Função ainda não implementada.
        A implementação futura deve utilizar geopandas, fiona ou APIs do QGIS.
    """
    raise NotImplementedError("Implementar leitura de shapefile, GeoJSON ou camada QGIS.")
