# Variáveis de configuração
PYTHON = python3
PYTEST = pytest
PYTEST_ARGS = -v
COVERAGE = coverage
MKDOCS = mkdocs
PIP = pip

# Diretórios do projeto
SRC_DIR = .
TEST_DIR = tests
DOC_DIR = docs
SITE_DIR = site

# Alvos principais
.PHONY: all test coverage clean docs lint install help

# Alvo padrão
all: test coverage docs

# Instalação de dependências
install:
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt

# Execução de testes
test:
	@echo "Executando testes..."
	$(PYTEST) $(PYTEST_ARGS)

# Cobertura de testes
coverage:
	@echo "Gerando relatório de cobertura..."
	$(COVERAGE) run -m pytest
	$(COVERAGE) report -m

# Cobertura com relatório HTML
coverage-html:
	@echo "Gerando relatório de cobertura HTML..."
	$(COVERAGE) run -m pytest
	$(COVERAGE) html
	@echo "Relatório HTML gerado em htmlcov/index.html"

# Cobertura com log
coverage-log:
	@echo "Gerando log de cobertura..."
	$(COVERAGE) run -m pytest
	$(COVERAGE) report -m > logs/coverage-$(shell date +%Y%m%d-%H%M%S).log
	@echo "Log de cobertura gerado em logs/"

# Limpeza de arquivos temporários
clean:
	@echo "Limpando arquivos temporários..."
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf htmlcov
	@echo "Limpeza concluída!"

# Limpeza profunda (inclui site gerado)
clean-all: clean
	@echo "Realizando limpeza completa..."
	rm -rf $(SITE_DIR)
	@echo "Limpeza completa concluída!"

# Gerar documentação
docs:
	@echo "Gerando documentação..."
	$(MKDOCS) build

# Servir documentação localmente
docs-serve:
	@echo "Iniciando servidor de documentação..."
	$(MKDOCS) serve

# Verificação de estilo de código
lint:
	@echo "Verificando estilo de código..."
	flake8 $(SRC_DIR)
	black --check $(SRC_DIR)

# Formatação automática de código
format:
	@echo "Formatando código..."
	black $(SRC_DIR)
	isort $(SRC_DIR)

# Criar diretório de logs se não existir
logs:
	@mkdir -p logs

# Ajuda
help:
	@echo "Alvos disponíveis:"
	@echo "  all          : Executa testes, cobertura e gera documentação"
	@echo "  install      : Instala dependências do projeto"
	@echo "  test         : Executa testes"
	@echo "  coverage     : Gera relatório de cobertura no terminal"
	@echo "  coverage-html: Gera relatório de cobertura em HTML"
	@echo "  coverage-log : Gera log de cobertura com timestamp"
	@echo "  clean        : Remove arquivos temporários"
	@echo "  clean-all    : Remove arquivos temporários e site gerado"
	@echo "  docs         : Gera documentação"
	@echo "  docs-serve   : Inicia servidor local de documentação"
	@echo "  lint         : Verifica estilo de código"
	@echo "  format       : Formata código automaticamente"
	@echo "  help         : Exibe esta ajuda"

# Garantir que o diretório de logs exista antes de gerar logs
coverage-log: logs
