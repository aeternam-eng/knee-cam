import cv2
from pathlib import Path
import numpy as np

import constants
import helpers

def build_train_set():
    labels = np.array([0, 1, 2, 3, 4])

    imagesByLabels = [helpers.get_all_images_from_directory(Path(constants.DATASET_DIR, 'train', str(classType))) for classType in labels]

    label_set = []
    image_set = []
    for i in range(len(imagesByLabels)):
        for labeledImage in imagesByLabels[i]:
            image_set.append(helpers.calculate_image_histogram(labeledImage))
            simplified_label = 0 if i < 2 else 1
            label_set.append(simplified_label)

    return np.array(label_set), np.array(image_set, dtype=np.float32)

def main():
    labels, samples = build_train_set()

    model = cv2.ml.SVM_create()
    model.setType(cv2.ml.SVM_C_SVC)
    model.setKernel(cv2.ml.SVM_RBF)
    model.setDegree(1)
    model.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 1000, 1e-6))

    model.trainAuto(samples, cv2.ml.ROW_SAMPLE, labels)

    model.save('./model.xml')

if __name__ == '__main__':
    main()
