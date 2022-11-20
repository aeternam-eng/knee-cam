import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import helpers
import constants

def histograms():
    images = helpers.get_all_images_from_directory(Path(constants.DATASET_DIR, 'train', '1'))
    helpers.show_image_histogram(images[40])

    cv2.imshow('hist', images[40])
    helpers.show_histograms()

def fill_holes(image):
    des = image.copy()
    contours, _ = cv2.findContours(des, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        cv2.drawContours(des, [contour], None, 255, -1)

    holes_filled = des.copy()

    cv2.imshow('holes filled', holes_filled)

    return holes_filled

def blur_image(image):
    blurred = image.copy()
    blurred = cv2.GaussianBlur(blurred, (5,5), 0)
    blurred = cv2.bilateralFilter(blurred, 27, 3, 3)

    cv2.imshow('blurred', blurred)

    return blurred

def apply_laplacian_filter(image):
    # laplacianKernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
    # laplacian = cv2.filter2D(image, cv2.CV_32F, laplacianKernel)

    laplacian = cv2.Laplacian(image, cv2.CV_64FC1, ksize=3)
    filtered = np.float32(image) - laplacian
    filtered = np.uint8(filtered)

    cv2.imshow('laplacian', filtered)

    return filtered

def filter_image(image):
    filtered = image.copy()
    filtered = cv2.equalizeHist(filtered)
    filtered = blur_image(filtered)
    filtered = apply_laplacian_filter(filtered)

    return filtered

def morph_image(image):
    kernel = np.ones((3,3))

    morphed = image.copy()
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE,kernel, iterations=1)
    morphed = cv2.erode(morphed, kernel, iterations=2)
    cv2.imshow('morph1', morphed)

    return morphed

def threshold_image(image):
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 127, 2)
    # _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow('thresholded', np.array(thresholded))

    return thresholded

def watershed_image(image, thresholdedImage):
    outputImage = cv2.cvtColor(thresholdedImage, cv2.COLOR_GRAY2BGR)

    kernel = np.ones((3,3),np.uint8)
    sure_background = cv2.dilate(image, kernel, iterations=3)

    dist = cv2.distanceTransform(image, cv2.DIST_L2, 3)
    cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)

    ret, sure_foreground = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
    sure_foreground = np.uint8(sure_foreground)
    unknown = cv2.subtract(sure_background, sure_foreground)

    ret, markers = cv2.connectedComponents(sure_foreground)
    cv2.imshow('markers', np.uint8(markers))

    markers = markers + 1
    markers[unknown == 255] = 0

    cv2.imshow('sure bg', sure_background)
    cv2.imshow('distancetransform', dist)
    cv2.imshow('sure_fg', sure_foreground)

    markers = cv2.watershed(outputImage, markers)
    outputImage[markers == -1] = [0, 0, 255]

    return outputImage

def process_image(image):
    cv2.imshow('original', image)

    processed = image.copy()
    processed = filter_image(processed)
    processed = threshold_image(processed)
    processed = morph_image(processed)
    processed = fill_holes(processed)
    processed = watershed_image(processed, processed)

    cv2.imshow('final', processed)

    return processed

def main():
    # images = helpers.get_all_images_from_directory(Path(constants.DATASET_DIR, 'train', '2'))

    # image = images[15]
    # process_image(image) 

    cv2.waitKey()

    # histograms();

if __name__ == '__main__':
    main()
