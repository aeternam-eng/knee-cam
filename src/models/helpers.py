import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def get_and_enrich_all_images_from_directory(directory):
    allImages = [cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE) for image_path in Path(directory).glob("*")]
    # Flip horizontally for extending dataset
    mirrored = [cv2.flip(image, 1) for image in allImages]
    # Equalize histograms to extend dataset
    histogramEqualized = [cv2.equalizeHist(image) for image in allImages]
    return np.concatenate((allImages, histogramEqualized, mirrored))
