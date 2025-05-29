# Kit de Interpolação para QGIS

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/vmendes93/qgis-interpolagem)](LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/vmendes93/qgis-interpolagem)](https://github.com/vmendes93/qgis-interpolagem/issues)
[![GitHub stars](https://img.shields.io/github/stars/vmendes93/qgis-interpolagem)](https://github.com/vmendes93/qgis-interpolagem/stargazers)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://vmendes93.github.io/qgis-interpolagem/)

![Logo](docs/assets/logo.png)

Kit de ferramentas para interpolação espacial, com suporte a métodos como IDW, Krigagem e geração de modelo potenciométrico. Desenvolvido para eventual integração como plugin do QGIS.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Exemplo Rápido](#exemplo-rápido)
- [Documentação](#documentação)
- [Requisitos](#requisitos)
- [Desenvolvimento](#desenvolvimento)
- [Como Contribuir](#como-contribuir)
- [Changelog](#changelog)
- [Licença](#licença)
- [Autor](#autor)

## ✨ Funcionalidades

- **Interpolação IDW** (Inverse Distance Weighting)
  - Configuração flexível de expoente, vizinhos e distância máxima
  - Tratamento adequado de casos extremos
  - Opção de valor padrão para células sem vizinhos válidos

- **Krigagem Ordinária**
  - Suporte a diferentes modelos de variograma (esférico, exponencial, gaussiano, linear)
  - Configuração de anisotropia
  - Cálculo de variância de estimativa

- **Modelo Potenciométrico**
  - Cálculo de gradientes e vetores de fluxo
  - Visualização de vetores de fluxo com opções de personalização
  - Análise de superfícies potenciométricas

- **Recursos Adicionais**
  - Sistema de logging para monitoramento detalhado do progresso
  - Testes automatizados com alta cobertura de código
  - Documentação completa com exemplos e tutoriais

## 🚀 Instalação

```bash
# Instalação via pip (quando disponível)
pip install qgis-interpolagem

# Instalação a partir do código fonte
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem
pip install -e .
```

## 💡 Exemplo Rápido

```python
from interpoladores.idw import IDW
from interpoladores.config import IDWConfig
import numpy as np

# Pontos conhecidos
pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]] )
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

# Visualização (opcional)
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 8))
plt.contourf(grid_x, grid_y, z, 20, cmap='viridis')
plt.colorbar(label='Valor')
plt.scatter(pontos[:, 0], pontos[:, 1], c='red', s=50)
plt.title('Interpolação IDW')
plt.show()
```

## 📚 Documentação

A documentação completa está disponível em [https://vmendes93.github.io/qgis-interpolagem/](https://vmendes93.github.io/qgis-interpolagem/)

Inclui:
- [Guia de Início Rápido](https://vmendes93.github.io/qgis-interpolagem/quickstart.html)
- [Conceitos de Interpolação](https://vmendes93.github.io/qgis-interpolagem/conceitos.html)
- [Referência do Pacote](https://vmendes93.github.io/qgis-interpolagem/pacote.html)
- [Exemplos Detalhados](https://vmendes93.github.io/qgis-interpolagem/exemplos.html)

## 📋 Requisitos

- Python 3.8 ou superior
- NumPy 1.20 ou superior
- SciPy 1.7 ou superior
- Matplotlib 3.4 ou superior
- PyKrige 1.6 ou superior (para Krigagem)

## 🛠️ Desenvolvimento

Para contribuir com o desenvolvimento:

```bash
# Clone o repositório
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale em modo de desenvolvimento
pip install -e ".[dev]"

# Configure os hooks de pre-commit
pre-commit install

# Execute os testes
make test

# Verifique a cobertura de código
make coverage

# Gere a documentação
make docs
```

## 👥 Como Contribuir

Contribuições são muito bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir com o projeto.

Resumo:
1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

Não se esqueça de dar uma ⭐️ no projeto se ele te ajudou!

## 📝 Changelog

Veja o arquivo [CHANGELOG.md](CHANGELOG.md) para detalhes sobre as mudanças em cada versão.

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✍️ Autor

Vinicius Mendes - [vmendes93](https://github.com/vmendes93)

---
