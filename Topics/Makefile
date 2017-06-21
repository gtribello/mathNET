TOPIC_SRC=$(wildcard *.xml)
TOPIC_OBJ=$(TOPIC_SRC:%.xml=../html/%.html)

all: $(TOPIC_OBJ) $(TOPIC_SRC) ../html

../html/%.html: %.xml
	python ../Scripts/createTopicPage.py $^ ../
