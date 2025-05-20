# Caminhos
SRC_DIR = interpoladores
TEST_DIR = tests

# Busca automaticamente os módulos e gera os arquivos de teste correspondentes
PYTHON_MODULES := $(basename $(notdir $(wildcard $(SRC_DIR)/*.py)))
TEST_FILES := $(addprefix $(TEST_DIR)/test_,$(addsuffix .py,$(PYTHON_MODULES)))

.PHONY: test coverage run install clean log

# Roda os testes e salva log
log:
	@echo "🧪 Rodando testes e salvando em interpolador.log..."
	pytest $(TEST_FILES) | tee interpolador.log

# Roda os testes
test:
	@echo "🔍 Rodando testes para: $(PYTHON_MODULES)"
	pytest $(TEST_FILES)

# Gera cobertura de testes
coverage:
	coverage run -m pytest $(TEST_FILES)
	coverage report -m | tee coverage.log
	coverage html
	@echo "📂 HTML gerado em htmlcov/index.html"
	@echo "📊 Gerando relatório de cobertura com coverage..."
	coverage run -m pytest $(TESTS_DIR)
	coverage report -m
	coverage html

# Executa o script principal
run:
	@echo "🚀 Rodando main.py..."
	python3 main.py

# Instala dependências
install:
	@echo "📦 Instalando dependências..."
	pip install -r requirements.txt

# Limpa arquivos temporários
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov coverage.log interpolador.log


coverage-log:
	@echo "📋 Gerando log de cobertura com timestamp..."
	@mkdir -p logs
	@timestamp=$$(date +'%Y%m%d-%H%M%S'); \
	PYTHONPATH=. coverage run -m pytest $(TESTS_DIR) && \
	PYTHONPATH=. coverage report > logs/coverage-$$timestamp.log

