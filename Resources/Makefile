.PHONY: resources images

RESOURCE_XML=$(wildcard *.xml) 
RESOURCE_PDF=$(wildcard *.pdf)
RESOURCE_TEX=$(wildcard *.tex)
RESOURCE_HTML=$(wildcard *.html)

RESOURCE_SRC=$(RESOURCE_XML) $(RESOURCE_PDF) $(RESOURCE_TEX) $(RESOURCE_HTML) $(RESOURCE_IMG)
RESOURCE_TMP=$(RESOURCE_XML:%.xml=../html/%.html) $(RESOURCE_PDF:%.pdf=../html/resources/%.pdf) 
RESOURCE_OBJ=$(RESOURCE_TMP) $(RESOURCE_TEX:%.tex=../latex/%.pdf) $(RESOURCE_HTML:%.html=../html/%.html) 

resources: $(RESOURCE_OBJ) $(RESOURCE_SRC) images 

images: ../html
	make -C Images

../html/%.html: %.xml
	python ../Scripts/createHTMLFromXML.py $^ ../

../latex/%.pdf: %.tex
	pdflatex --output-directory=../latex $^
	pdflatex --output-directory=../latex $^

../html/resources/%.pdf: %.pdf
	echo Copying $^ 
	$(shell cp -f $^ ../html/resources/)

../html/%.html: %.html
	echo Copying $^
	$(shell cp -f $^ ../html/)
