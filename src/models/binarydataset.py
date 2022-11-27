# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico
import cv2
import numpy as np
from pathlib import Path

import helpers

directories = [r"./src/data/kneeKL224/train/", r"./src/data/kneeKL224/val/", r"./src/data/kneeKL224/test/"]
folder = ["train", "val", "test"]

# Constrói o dataset binário para a CNN
def build_train_set(path, folder):
    labels = np.array([0, 1, 2, 3, 4])

    imagesByLabels = [helpers.get_all_images_from_directory(Path(path, str(classType))) for classType in labels]
    for i in range(len(imagesByLabels)):
        if (i <= 1):
            finalPath = r"./src/databinary/kneeKL224/"+folder+"/"+"normal"+"/"
            print(finalPath)
            for index, labeledImage in enumerate(imagesByLabels[i]):
                image = labeledImage.copy()
                cv2.imwrite(finalPath+str(index)+".png", image)
        else:
            finalPath = r"./src/databinary/kneeKL224/"+folder+"/"+"arthrosis"+"/"
            print(finalPath)
            for index, labeledImage in enumerate(imagesByLabels[i]):
                image = labeledImage.copy()
                cv2.imwrite(finalPath+str(index)+".png", image)
        
def main():
    for i in range(3):
        print(directories[i], folder[i])
        build_train_set(directories[i], folder[i])

if __name__ == '__main__':
    main()
