1. Clone o repositório:

```bash
git clone https://github.com/evandroviero/Streamlit
cd STREAMLIT
```

2. Criando nosso ambiente virtual
Ambientes virtuais são uma ferramenta para manter as dependências necessárias para diferentes projetos em locais separados, evitando problemas de compatibilidade.

```bash
poetry init
```

3. Ativando nosso ambiente virtual

```bash
poetry shell
```

4. Instalando o Streamlit
Streamlit é uma biblioteca em Python que permite aos desenvolvedores criar aplicativos da web interativos para análise de dados e visualização com facilidade, usando apenas código Python.


```bash
poetry add streamlit
```

5. Executando o projeto
```bash
poetry run streamlit run app.py
```
ou 

```bash
poetry run streamlit run imc.py
```

ou
```bash
poetry run streamlit run analise_financeira.py
```