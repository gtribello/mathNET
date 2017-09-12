.PHONY: all clean assets blockly modules topics resources

RESOURCE_FILES=$(wildcard Resources/*)

all: topics modules latex

html: 
	mkdir $@
	mkdir $@/worksheets
	mkdir $@/resources
	mkdir $@/Images
	python Scripts/createMainPage.py

assets: Templates/assets html
	cp -pr $^ 
	
blockly: Templates/blockly html
	cp -pr $^ 
	rm html/blockly/.git
	rm html/blockly/.gitignore

topics: html assets blockly
	make -C Topics

resources: html assets blockly
	make -C Resources

modules: html assets blockly
	make -C Modules

latex: resources
	make -C latex

clean:
	rm -rf html latex/*.tex latex/*.pdf latex/*.aux latex/*.log
