# Instalação

Este guia explica como instalar o Kit de Interpolação para o QGIS em seu ambiente de desenvolvimento.

## Requisitos

Antes de instalar, certifique-se de que seu sistema atende aos seguintes requisitos:

- Python 3.8 ou superior
- NumPy 1.20 ou superior
- SciPy 1.7 ou superior
- Matplotlib 3.4 ou superior
- PyKrige 1.6 ou superior (para Krigagem)

## Instalação via pip

A maneira mais simples de instalar o Kit de Interpolação é usando pip:

```bash
pip install qgis-interpolagem
```

## Instalação a partir do código fonte

Para instalar a versão mais recente do código fonte:

1. Clone o repositório:
```bash
git clone https://github.com/vmendes93/qgis-interpolagem.git
```

2. Entre no diretório do projeto
```bash
cd qgis-interpolagem
```

3. Instale o pacote em modo de desenvolvimento:
```bash
pip install -e .
```

## Verificando a Instalação

Para verificar se a instalação foi bem-sucedida, execute o seguinte código Python:

```python
from interpoladores.idw import IDW
from interpoladores.krigagem import Krigagem
from interpoladores.modelo_potenciometrico import ModeloPotenciometrico

print("Instalação bem-sucedida!" )
```
## Instalação como plugin do QGIS

> **Nota:** A versão do plugin para QGIS ainda está em desenvolvimento.

Quando disponível, o plugin poderá ser instalado diretamente do Gerenciador de Plugins do QGIS:

1. Abra o QGIS
2. Vá para Plugins > Gerenciar e Instalar Plugins
3. Pesquise por "Kit de Interpolação"
4. Clique em "Instalar Plugin"

## Próximos passos

Após a instalação, consulte o [Guia de Primeiros](primeiros-passos.md) Passos para começar a usar o Kit de Interpolação.
