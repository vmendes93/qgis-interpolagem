import importlib
import inspect
import os

MODULES = {
    "interpoladores": "Interpoladores espaciais como IDW e Krigagem.",
    "io_utils": "Funções auxiliares para entrada e saída de dados.",
    "utils": "Funções utilitárias diversas para apoio ao projeto.",
}

OUTPUT_DIR = "docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for module_name, description in MODULES.items():
    try:
        mod = importlib.import_module(module_name)
    except ImportError:
        print(f"⚠️ Módulo {module_name} não pôde ser importado.")
        continue

    filename = os.path.join(OUTPUT_DIR, f"{module_name}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {module_name}\n\n")
        f.write(f"{description}\n\n")

        for name, obj in inspect.getmembers(mod):
            if inspect.isfunction(obj) or inspect.isclass(obj):
                doc = inspect.getdoc(obj)
                if doc:
                    f.write(f"## {name}\n\n{doc}\n\n")
    print(f"✅ Gerado: {filename}")
