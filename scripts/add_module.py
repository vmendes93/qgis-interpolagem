import os
import sys

def criar_arquivo(caminho, conteudo):
    with open(caminho, "w") as f:
        f.write(conteudo)
    print(f"✓ Criado: {caminho}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/add_module.py nome_modulo")
        sys.exit(1)

    nome = sys.argv[1]

    caminho_modulo = f"interpoladores/{nome}.py"
    caminho_teste = f"tests/test_{nome}.py"

    if os.path.exists(caminho_modulo) or os.path.exists(caminho_teste):
        print("❌ Arquivo já existe. Escolha outro nome.")
        sys.exit(1)

    conteudo_modulo = f"""# {nome}.py

def exemplo():
    return "Olá de {nome}!"
"""

    conteudo_teste = f"""# test_{nome}.py

from interpoladores import {nome}

def test_exemplo():
    assert {nome}.exemplo() == "Olá de {nome}!"
"""

    criar_arquivo(caminho_modulo, conteudo_modulo)
    criar_arquivo(caminho_teste, conteudo_teste)

if __name__ == "__main__":
    main()

