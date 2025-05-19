# Caminhos
TESTS_DIR = tests

# Comandos padrão
.PHONY: test run clean install

# Roda os testes
test:
	@echo "🔍 Rodando testes com pytest..."
	pytest $(TESTS_DIR)

# Executa o script principal
run:
	@echo "🚀 Rodando o main.py..."
	python3 main.py

# Instala dependências
install:
	@echo "📦 Instalando dependências..."
	pip install -r requirements.txt

# Remove arquivos gerados
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -name '*.pyc' -delete
	rm -f interpolador.log

