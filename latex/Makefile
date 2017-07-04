.PHONY: latex

LATEX_SRC=$(wildcard *.pdf)
LATEX_OBJ=$(LATEX_SRC:%.pdf=../html/resources/%.pdf)

latex: $(LATEX_OBJ) $(LATEX_SRC) ../html

../html/resources/%.pdf: %.pdf
	$(shell cp -f $^ ../html/resources/)
