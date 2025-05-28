# Kit de Interpolação para o QGIS

**Kit de ferramentas para interpolação espacial, com suporte a métodos como IDW, Krigagem e geração de modelo potenciométrico.**

> 🚧 **Em desenvolvimento. Ainda não integrado diretamente ao QGIS.** Este repositório fornece a base computacional para posterior criação de um plugin.

---

## ✨ Funcionalidades

- 📌 Interpolação IDW com configuração ajustável
- 📌 Krigagem com diferentes modelos de variograma
- 📌 Geração de modelo potenciométrico e vetores de fluxo
- 📈 Visualização vetorial de fluxos sobre o grid
- ✅ Testes automatizados com cobertura
- 🐍 Documentação gerada automaticamente com [pdoc](https://vmendes93.github.io/qgis-interpolagem)

---

## 📦 Instalação

Clone o projeto:

```bash
git clone https://github.com/vmendes93/qgis-interpolagem.git
cd qgis-interpolagem
pip install -r requirements.txt
```

---

## 🧪 Rodando os testes

```bash
make test         # Roda todos os testes
make coverage     # Gera relatório de cobertura no terminal
make coverage-log # Gera logs de cobertura com timestamp
```

---

## 📚 Documentação

A documentação está disponível em:

🔗 [https://vmendes93.github.io/qgis-interpolagem](https://vmendes93.github.io/qgis-interpolagem)

Gerada automaticamente com `pdoc`.

---

## 📂 Estrutura

```
interpoladores/
├── base.py
├── idw.py
├── krigagem.py
├── modelo_potenciometrico.py
io_utils/
├── leitor.py
├── exportador.py
utils/
├── grid_utils.py
tests/
├── test_idw.py
├── test_krigagem.py
├── test_modelo_potenciometrico.py
```

---

## 🎯 Próximos passos

- [ ] Integração com QGIS como plugin gráfico
- [ ] Interface de parâmetros via GUI
- [ ] Exportação direta para camadas vetoriais

---

## 🛠️ Contribuindo

Contribuições são bem-vindas! Abra um pull request ou entre em contato para colaborar.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
