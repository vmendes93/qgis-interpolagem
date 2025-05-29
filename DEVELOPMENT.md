# Guia de Desenvolvimento

Este documento fornece orientações detalhadas para o desenvolvimento e contribuição para o Kit de Interpolação para QGIS.

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Pip (gerenciador de pacotes Python)
- Conhecimento básico de interpolação espacial (para contribuições de código)

### Configuração Inicial

1. **Clone o repositório**

```bash
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem
```

2. **Crie e ative um ambiente virtual**

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências de desenvolvimento**

```bash
pip install -e ".[dev]"
```

4. **Configure os hooks de pre-commit**

```bash
pre-commit install
```

## Estrutura do Projeto

```
qgis-interpolagem/
├── .github/                    # Configurações do GitHub (workflows, templates)
├── docs/                       # Documentação
├── interpoladores/             # Módulos de interpolação
│   ├── __init__.py
│   ├── idw.py                  # Implementação do IDW
│   ├── krigagem.py             # Implementação da Krigagem
│   ├── modelo_potenciometrico.py  # Implementação do Modelo Potenciométrico
│   └── config.py               # Classes de configuração
├── io_utils/                   # Utilitários de entrada/saída
├── tests/                      # Testes automatizados
├── utils/                      # Utilitários gerais
├── .flake8                     # Configuração do Flake8
├── .gitignore                  # Arquivos ignorados pelo Git
├── .pre-commit-config.yaml     # Configuração do pre-commit
├── CHANGELOG.md                # Registro de alterações
├── CODE_OF_CONDUCT.md          # Código de conduta
├── CONTRIBUTING.md             # Guia de contribuição
├── LICENSE                     # Licença do projeto
├── Makefile                    # Automação de tarefas
├── pyproject.toml              # Configuração do projeto
├── README.md                   # Documentação principal
├── requirements.txt            # Dependências do projeto
└── setup.py                    # Script de instalação
```

## Fluxo de Trabalho de Desenvolvimento

### 1. Preparação

Antes de começar a trabalhar em uma nova funcionalidade ou correção:

1. **Atualize seu fork/branch**

```bash
git checkout main
git pull origin main
```

2. **Crie uma branch para sua contribuição**

```bash
git checkout -b feature/nome-da-feature  # Para novas funcionalidades
# ou
git checkout -b fix/nome-do-bug          # Para correções de bugs
```

### 2. Desenvolvimento

1. **Escreva testes primeiro (TDD)**

Crie testes que definam o comportamento esperado da sua funcionalidade ou correção.

```bash
# Exemplo de criação de um teste para uma nova funcionalidade no IDW
touch tests/test_nova_funcionalidade.py
```

2. **Implemente sua funcionalidade ou correção**

Siga as convenções de código e documente adequadamente.

3. **Execute os testes localmente**

```bash
# Executar todos os testes
make test

# Executar testes específicos
pytest tests/test_nova_funcionalidade.py -v
```

4. **Verifique a cobertura de código**

```bash
make coverage
```

5. **Execute o linting e formatação**

```bash
# O pre-commit fará isso automaticamente ao fazer commit
# Mas você pode executar manualmente:
pre-commit run --all-files
```

### 3. Commit e Push

1. **Faça commits pequenos e significativos**

Siga as convenções de commit semântico:

```bash
git add .
git commit -m "feat: adiciona suporte para novo modelo de variograma"
```

Prefixos comuns:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, sem alteração de código
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Atualizações de tarefas de build, etc.

2. **Envie suas alterações para o seu fork**

```bash
git push origin feature/nome-da-feature
```

### 4. Pull Request

1. Vá para o repositório no GitHub
2. Crie um novo Pull Request
3. Preencha o template com informações detalhadas
4. Aguarde a revisão e feedback

## Convenções de Código

### Estilo de Código

- Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Limite de linha: 100 caracteres
- Use docstrings no formato NumPy para documentação

### Exemplo de Docstring

```python
def interpolar(pontos, valores, grid_x, grid_y):
    """
    Realiza a interpolação IDW sobre uma grade regular.
    
    Parameters
    ----------
    pontos : numpy.ndarray
        Array de shape (N, 2) com coordenadas XY dos pontos amostrados.
    valores : numpy.ndarray
        Array de shape (N,) com os valores correspondentes aos pontos.
    grid_x : numpy.ndarray
        Meshgrid com coordenadas X da grade.
    grid_y : numpy.ndarray
        Meshgrid com coordenadas Y da grade.
        
    Returns
    -------
    numpy.ndarray
        Array 2D (mesmo shape de grid_x) com os valores interpolados.
        
    Examples
    --------
    >>> pontos = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    >>> valores = np.array([10, 20, 30, 40])
    >>> x = np.linspace(0, 1, 10)
    >>> y = np.linspace(0, 1, 10)
    >>> grid_x, grid_y = np.meshgrid(x, y)
    >>> z = interpolar(pontos, valores, grid_x, grid_y)
    """
```

### Nomenclatura

- **Classes**: CamelCase (ex: `InterpoladorIDW`)
- **Funções e métodos**: snake_case (ex: `calcular_gradiente`)
- **Variáveis**: snake_case (ex: `pontos_amostrais`)
- **Constantes**: UPPER_CASE (ex: `MAX_ITERACOES`)

## Processo de Release

1. **Atualizar a versão**

Atualize a versão em `setup.py` e `pyproject.toml` seguindo o versionamento semântico:
- MAJOR: alterações incompatíveis com versões anteriores
- MINOR: adições de funcionalidades compatíveis
- PATCH: correções de bugs compatíveis

2. **Atualizar o CHANGELOG.md**

Adicione uma nova seção para a versão, listando todas as alterações.

3. **Criar um Pull Request para a branch main**

4. **Após aprovação e merge, criar uma tag**

```bash
git checkout main
git pull origin main
git tag -a v0.2.0 -m "Versão 0.2.0"
git push origin v0.2.0
```

5. **A GitHub Action criará automaticamente um release**

## Dicas e Boas Práticas

1. **Mantenha a cobertura de testes alta**
   - Escreva testes para todos os novos recursos
   - Mantenha a cobertura acima de 80%

2. **Documente seu código**
   - Adicione docstrings a todas as funções, classes e métodos
   - Atualize a documentação quando fizer alterações

3. **Mantenha as dependências atualizadas**
   - Verifique regularmente por atualizações de segurança

4. **Comunique-se efetivamente**
   - Descreva claramente o propósito das suas alterações
   - Responda a feedback de forma construtiva

5. **Siga o princípio da responsabilidade única**
   - Cada classe ou função deve ter uma única responsabilidade
   - Mantenha o código modular e reutilizável
