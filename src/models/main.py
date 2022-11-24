import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import helpers
import constants

def main():
    images = helpers.get_and_enrich_all_images_from_directory(Path(constants.DATASET_DIR, 'train', '1'))

    # image = images[20]
    # process_image(image) 

    cv2.waitKey()

    # histograms();

if __name__ == '__main__':
    main()
