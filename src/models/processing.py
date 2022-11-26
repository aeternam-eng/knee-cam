import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def fill_holes(image):
    des = image.copy()
    contours, _ = cv2.findContours(des, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

    for contour in contours:
        cv2.drawContours(des, [contour], None, 255, -1)

    holes_filled = des.copy()

    return holes_filled

def blur_image(image):
    blurred = image.copy()
    blurred = cv2.GaussianBlur(blurred, (5,5), 0)
    blurred = cv2.bilateralFilter(blurred, 27, 20, 20)

    return blurred

def apply_laplacian_filter(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64FC1, ksize=3)
    filtered = np.float32(image) - laplacian
    filtered = np.uint8(filtered)

    return filtered

def filter_image(image):
    filtered = image.copy()
    # filtered = blur_image(filtered)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10,20))
    # filtered = clahe.apply(filtered)

    return np.uint8(filtered)

def calculate_image_moments(image):
    moments = cv2.moments(image)
    return cv2.HuMoments(moments)

def morph_image(image):
    kernel = np.ones((3,3))

    morphed = image.copy()
    morphed = cv2.morphologyEx(morphed, cv2.MORPH_CLOSE,kernel, iterations=1)
    morphed = cv2.erode(morphed, kernel, iterations=2)
    

    return morphed

def threshold_image(image):
    thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 245, 3)
    # _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)    

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
    
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(outputImage, markers)
    outputImage[markers == -1] = [0, 0, 255]

    return outputImage

def addToStack(original, image):
    # coloredOriginal = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    # coloredImage = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    try:
        newStack = np.hstack((original, image))
    except:
        newStack = np.hstack((cv2.cvtColor(original, cv2.COLOR_GRAY2BGR), image))

    return newStack

def calculateGaborFilter(image):
    gaborKernel = cv2.getGaborKernel((21,21), 8, np.pi/4, 10, 0.5, 0, cv2.CV_32F)
    return cv2.filter2D(image, cv2.CV_32F, gaborKernel)

def calculate_image_histogram(image):
    return cv2.calcHist([image], [0], None, [256], [0, 256])

def process_image(image):
    processed = image.copy()
    processed = filter_image(processed)
    moments = calculate_image_moments(processed)
    print('image moments', np.log10(moments))

    out = addToStack(image, processed)

    processed = threshold_image(processed)

    out = addToStack(out, processed)

    processed = morph_image(processed)

    out = addToStack(out, processed)

    processed = fill_holes(processed)

    out = addToStack(out, processed)

    processed = watershed_image(processed, processed)

    out = addToStack(out, processed)

    return processed
