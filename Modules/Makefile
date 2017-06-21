MODULE_SRC=$(wildcard *.xml)
MODULE_OBJ=$(MODULE_SRC:%.xml=../html/%.html)

module: $(MODULE_OBJ) $(MODULE_SRC) ../html

../html/%.html: %.xml
	python ../Scripts/createModulePages.py $^ ../
