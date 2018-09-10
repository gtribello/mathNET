
.PHONY: images

IMAGE_SRC=$(wildcard *.png) sor3012-exercise-1.ipynb
IMAGE_OBJ=$(IMAGE_SRC:%.png=../../html/Images/%.png) ../../html/Images/sor3012-exercise-1.ipynb

images: $(IMAGE_SRC) $(IMAGE_OBJ) 

../../html/Images/%.png: %.png
	$(shell cp -f $^ ../../html/Images/)

../../html/Images/sor3012-exercise-1.ipynb: sor3012-exercise-1.ipynb
	$(shell cp -f $^ ../../html/Images/)
