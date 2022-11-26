import numpy as np
import cv2
import time
import joblib
import tensorflow as tf
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

import models.processing as processing
import shared.constants as constants

def get_all_images_from_directory(directory):
    return [cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE) for image_path in Path(directory).glob("*")]

def get_and_enrich_all_images_from_directory(directory):
    allImages = get_all_images_from_directory(directory)
    # Flip horizontally for extending dataset
    mirrored = [cv2.flip(image, 1) for image in allImages]
    # Equalize histograms to extend dataset
    histogramEqualized = [cv2.equalizeHist(image) for image in allImages]

    return np.concatenate((allImages, histogramEqualized, mirrored))

def get_image_descriptors(image, use_moments=False):
    processed = image.copy()

    if use_moments:
        processed = processing.filter_image(image)
        processed = processing.threshold_image(processed)
        moments = processing.calculate_image_moments(processed)

        moments = np.array([moment[0] for moment in moments], dtype=np.float32)
        moments = np.abs(moments)
        moments = np.log10(moments)

        return moments
    
    return processed

def describe_image(image, label, use_moments=False):
    descriptors = get_image_descriptors(image, use_moments)
    return (np.array(descriptors), label)

def describe_images_in_class(images, label, use_moments=False):
    classDescriptors = joblib.Parallel(n_jobs=5)(joblib.delayed(describe_image)(image, label, use_moments) for image in images)
    classDescriptors = np.array(classDescriptors, dtype=object)

    print(f"Loaded descriptors for label {label}: ", classDescriptors.shape)

    return classDescriptors

def build_image_descriptors(imagesByLabels, use_moments=False):
    labeledDescriptors = np.empty((0,2))

    for label in range(len(imagesByLabels)):
        labeledDescriptors = np.concatenate((labeledDescriptors, describe_images_in_class(imagesByLabels[label], label, use_moments)))

    return labeledDescriptors

def build_set(set_type, binary=False, with_extensions=False, use_moments=False):
    start_time = time.perf_counter()

    print(f'Loading {set_type} dataset...')
    labels = np.array([0,1,2,3,4])
    imagesByLabels = [get_and_enrich_all_images_from_directory(Path(constants.DATASET_DIR, set_type, str(classType))) for classType in labels] if with_extensions else [get_all_images_from_directory(Path(constants.DATASET_DIR, set_type, str(classType))) for classType in labels]
    print(f'Loaded {sum(len(l) for l in imagesByLabels)} images (with extensions) in {time.perf_counter() - start_time} s')

    print(f'Getting image descriptors...')
    labeledDescriptors = build_image_descriptors(imagesByLabels, use_moments)
    print(f'Total image loading time: {time.perf_counter() - start_time} s...')

    descriptors, labels = zip(*[(item[0], item[1]) for item in labeledDescriptors])
    descriptors = np.array(descriptors)
    labels = np.array(labels)

    # Truncates labels into 0 - No Arthrosis | 1 - Arthrosis
    if binary:
        labels = (labels > 1.0).astype(np.uint8)

    return labels, descriptors

def scale_dataset(dataset):
    print('Scaling and fitting dataset...')

    scaler = StandardScaler()
    scaled = scaler.fit(dataset)
    scaled = scaler.transform(dataset)
    # scaled = scale(scaled)
    
    return scaled
