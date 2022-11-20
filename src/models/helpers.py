import numpy as np
import cv2
import matplotlib.pyplot as plt
from pathlib import Path

def calculate_image_histogram(image):
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return cv2.calcHist([image], [0], None, [256], [0, 256])

def get_all_images_from_directory(directory):
    return [cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE) for image_path in Path(directory).glob("*")]

def show_image_histogram(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    histogram = cv2.calcHist([clahe.apply(image)], [0], None, [256], [0, 256])

    plt.plot(histogram, label='imagem')

def calculate_average_histogram_for_directory_images(directory):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    images = get_all_images_from_directory(directory)
    equalizedImages = [clahe.apply(image) for image in images]
    histogram = cv2.calcHist(equalizedImages, [0], None, [256], [0, 256])

    return histogram

    # plt.plot(histogram, label=directory)
    # plt.legend()

def show_histograms():
    plt.show()
