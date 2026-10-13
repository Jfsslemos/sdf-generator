LATEX = pdflatex
BIBTEX = bibtex
RM = rm -f
FILE = main

all:	
		$(LATEX) -interaction=nonstopmode -halt-on-error $(FILE).tex
		$(BIBTEX) $(FILE)
		$(LATEX) -interaction=nonstopmode -halt-on-error $(FILE).tex
		$(LATEX) -interaction=nonstopmode -halt-on-error $(FILE).tex
		@echo PDF: $(FILE).pdf

clean:	
		$(RM) $(FILE).aux $(FILE).log $(FILE).out $(FILE).pdf $(FILE).toc $(FILE).lof $(FILE).bbl $(FILE).lot $(FILE).blg *~ *backup
		@echo ---------------------------------------------------
		@echo Directory cleaned
