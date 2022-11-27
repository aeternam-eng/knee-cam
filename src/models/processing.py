# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico
import cv2
import numpy as np

def blur_image(image):
    blurred = image.copy()
    blurred = cv2.GaussianBlur(blurred, (5,5), 0)
    blurred = cv2.bilateralFilter(blurred, 27, 20, 20)

    return blurred

def filter_image(image):
    filtered = image.copy()
    filtered = blur_image(filtered)

    return np.uint8(filtered)

def calculate_image_moments(image):
    moments = cv2.moments(image)
    return cv2.HuMoments(moments)

def threshold_image(image):
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 245, 3)
    return thresholded
