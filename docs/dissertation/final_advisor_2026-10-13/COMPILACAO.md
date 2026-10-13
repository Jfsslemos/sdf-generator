# Compilação da dissertação

Esta fonte usa a classe institucional `texfurg.cls` incluída no diretório. A compilação requer uma distribuição TeX Live com `pdflatex`, `bibtex`, `babel`, `natbib`, `hyperref`, `booktabs`, `tabularx`, `longtable`, `float` e `enumitem`.

Na raiz deste diretório, execute:

```bash
make
```

O alvo equivale à sequência:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

O resultado é `main.pdf`, em papel A4. A opção `provide=*` encaminhada ao `babel` em `main.tex` permite usar a definição brasileira baseada nos arquivos de locale das distribuições TeX Live recentes, sem modificar a classe institucional.

Para remover arquivos intermediários e o PDF local:

```bash
make clean
```
