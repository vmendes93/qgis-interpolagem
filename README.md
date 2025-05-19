# QGIS Interpolador

![Documentação](https://img.shields.io/badge/docs-pdoc-green)](https://vmendes93.github.io/qgis-interpolagem/)
![Deploy Docs](https://github.com/vmendes93/qgis-interpolagem/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/vmendes93/qgis-interpolagem/actions/workflows/deploy-docs.yml)
![Testes Automatizados](https://github.com/vmendes93/qgis-interpolagem/actions/workflows/tests.yml/badge.svg)
![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

Ferramenta de interpolação espacial com foco em uso no QGIS ou Python puro.  
Atualmente suporta:

- IDW (Inverse Distance Weighting)
- Krigagem (Ordinary, Universal – com `PyKrige`)

---

## Instalação

```bash
git clone git@github.com:vmendes93/qgis-interpolagem.git
cd qgis_interpolador
pip install -e .
```
## Testes

```bash
make test
```
Ou manualmente

```bash
pytest tests
```
## Estrutura do projeto

<pre> 
qgis_interpolador/ 
├── interpoladores/ 
├── io/ 
├── utils/ 
├── tests/ 
├── main.py 
├── Makefile 
├── requirements.txt 
├── setup.py 
└── CHANGELOG.md 
</pre>

## Licença

Distribuído sob os termos da licença MIT.
Consulte o arquivo (LICENSE)[./LICENSE] para mais informações.

## Histórico de versões

Histórico de versões

Veja o (CHANGELOG.md)[./CHANGELOG.md] para detalhes sobre o desenvolvimento.
