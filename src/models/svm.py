import cv2
from pathlib import Path
import numpy as np

import constants
import helpers

def main():
    model = cv2.ml.SVM_load('./model.xml')

    labels = [0, 1, 2, 3, 4]

    for label in labels:
        actualLabel = 0 if label < 2 else 1
        testImages = helpers.get_all_images_from_directory(Path(constants.DATASET_DIR, 'train', str(label)))

        total = len(testImages)
        successes = 0
        for testImage in testImages:
            preparedImage = helpers.calculate_image_histogram(testImage)
            response = model.predict(np.float32([preparedImage]))
            predictedLabel = response[1][0]

            # print(f"Result: {predictedLabel}")
            
            if predictedLabel == actualLabel:
                successes = successes + 1

        print(f"Label: {label} - Successes/Total ({successes}/{total}) - {successes/total}")

if __name__ == '__main__':
    main()
