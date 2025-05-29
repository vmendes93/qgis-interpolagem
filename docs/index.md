# Kit de Interpolação para QGIS

Ferramentas de interpolação espacial para QGIS, incluindo métodos IDW, Krigagem e modelo potenciométrico.

![Logo do Projeto](assets/logo.png)

## Visão Geral

Este projeto fornece algoritmos de interpolação espacial otimizados para uso com QGIS:

- **IDW (Inverse Distance Weighting)**: Interpolação baseada na distância inversa ponderada
- **Krigagem**: Método geoestatístico avançado com diferentes modelos de variograma
- **Modelo Potenciométrico**: Cálculo de gradientes e vetores de fluxo

## Instalação

```bash
# Clone o repositório
git clone https://github.com/vmendes93/qgis-interpolagem.git

# Entre no diretório
cd qgis-interpolagem

# Instale as dependências
pip install -r requirements.txt

# Instale em modo de desenvolvimento
pip install -e .
```

## Exemplo Rápido

```python
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
import numpy as np

# Pontos conhecidos
pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
valores = np.array([10, 20, 30, 40])

# Grade para interpolação
x = np.linspace(0, 1, 10)
y = np.linspace(0, 1, 10)
grid_x, grid_y = np.meshgrid(x, y)

# Configuração personalizada
config = IDWConfig(power=2.0, n_neighbors=3)

# Interpolação
idw = IDW(config)
z = idw.interpolar(pontos, valores, grid_x, grid_y)
```

## Documentação

- [Guia de Início Rápido](quickstart.md)
- [Conceitos de Interpolação](conceitos.md)
- [Referência da API](api.md)
- [Exemplos](exemplos.md)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](https://github.com/vmendes93/qgis-interpolagem/blob/main/LICENSE) para detalhes.
