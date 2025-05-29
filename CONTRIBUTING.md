# Contribuindo para o Kit de Interpolação para QGIS

Obrigado pelo seu interesse em contribuir para o Kit de Interpolação para QGIS! Este documento fornece diretrizes para contribuir com o projeto.

## Código de Conduta

Este projeto segue o [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você respeite este código.

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor crie uma issue usando o template de bug report. Inclua:

1. Uma descrição clara do bug
2. Passos detalhados para reproduzir o problema
3. O comportamento esperado e o que aconteceu
4. Capturas de tela, se aplicável
5. Informações do ambiente (sistema operacional, versão do Python, versão do QGIS)

### Sugerindo Melhorias

Para sugerir melhorias, crie uma issue usando o template de feature request. Inclua:

1. Uma descrição clara da melhoria proposta
2. Justificativa (por que esta melhoria seria útil)
3. Possíveis implementações, se você tiver ideias

### Pull Requests

1. Faça um fork do repositório
2. Clone seu fork: `git clone https://github.com/seu-usuario/qgis-interpolagem.git`
3. Crie um branch para sua contribuição: `git checkout -b feature/sua-feature`
4. Faça suas alterações
5. Execute os testes: `make test`
6. Atualize a documentação, se necessário
7. Commit suas alterações seguindo as [convenções de commit](#convenções-de-commit)
8. Push para seu fork: `git push origin feature/sua-feature`
9. Abra um Pull Request usando o template fornecido

## Ambiente de Desenvolvimento

### Configuração

```bash
# Clone o repositório
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências de desenvolvimento
pip install -e ".[dev]"

# Configure os hooks de pre-commit
pre-commit install
```

### Executando Testes

```bash
# Executar todos os testes
make test

# Executar testes com cobertura
make coverage

# Executar linting
make lint
```

## Convenções de Código

- Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/) para estilo de código
- Use docstrings no formato NumPy para documentação
- Mantenha a cobertura de testes acima de 80%
- Use tipagem estática quando possível

## Convenções de Commit

Usamos mensagens de commit semânticas para facilitar a geração automática de changelogs:

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, ponto e vírgula faltando, etc; sem alteração de código
- `refactor`: Refatoração de código
- `test`: Adição ou correção de testes
- `chore`: Atualizações de tarefas de build, configurações, etc; sem alteração de código

Exemplo: `feat: adiciona suporte para modelo de variograma exponencial`

## Processo de Release

1. Atualize a versão em `setup.py` e `pyproject.toml`
2. Atualize o `CHANGELOG.md`
3. Crie um Pull Request para a branch main
4. Após aprovação e merge, crie uma tag com a nova versão
5. A GitHub Action criará automaticamente um release

## Dúvidas?

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para abrir uma issue com a tag "question".

Agradecemos sua contribuição para tornar este projeto melhor!
