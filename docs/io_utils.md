# Módulo: io_utils

Este pacote contém utilitários para entrada e saída de dados no Kit de Interpolação para o QGIS.

## leitor.py

Funções para ler dados de pontos espaciais a partir de arquivos CSV e retornar arrays NumPy.

**Funções:**
- `ler_pontos_csv`: lê um arquivo CSV com colunas X, Y e valor.

## exportador.py

Funções para exportar resultados de interpolação para arquivos GeoTIFF.

**Funções:**
- `exportar_raster_tiff`: exporta um raster NumPy com extensão georreferenciada.
