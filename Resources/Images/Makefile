
.PHONY: images

IMAGE_SRC=$(wildcard *.png)
IMAGE_OBJ=$(IMAGE_SRC:%.png=../../html/Images/%.png)

images: $(IMAGE_SRC) $(IMAGE_OBJ) 

../../html/Images/%.png: %.png
	$(shell cp -f $^ ../../html/Images/)

