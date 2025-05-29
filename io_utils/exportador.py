"""
Módulo para exportação de dados raster.

Este módulo irá fornecer funções para exportar matrizes de dados
(interpoladas, por exemplo) para formatos raster, como GeoTIFF, utilizando GDAL ou QGIS.

Funções:
    - exportar_raster: Exporta uma matriz como raster para o disco.

Status:
    - Ainda não implementado.

Dependências esperadas:
    - GDAL
    - QGIS (opcional)

"""


def exportar_raster(matriz, path):
    """
    Exporta uma matriz como arquivo raster.

    Args:
        matriz (np.ndarray): Matriz 2D com os valores a serem exportados.
        path (str): Caminho de saída para salvar o arquivo raster (ex.: 'output.tif').

    Raises:
        NotImplementedError: Função ainda não implementada. A implementação
        futura deve usar GDAL, rasterio ou APIs do QGIS.
    """
    raise NotImplementedError("Implementar exportação com GDAL, rasterio ou QGIS.")
