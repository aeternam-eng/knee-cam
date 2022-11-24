import os
import time
import joblib
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from pathlib import Path
import numpy as np

from processing import *
import constants
import helpers

def get_image_descriptors(image):
    processed = filter_image(image)
    moments = calculate_image_moments(processed)

    moments = np.array([moment[0] for moment in moments], dtype=np.float32)
    moments = np.abs(moments)
    moments = np.log10(moments)

    return moments

def describe_image(image, label):
    descriptors = get_image_descriptors(image)
    return (np.array(descriptors), label)

def describe_images_in_class(images, label):
    classDescriptors = joblib.Parallel(n_jobs=5)(joblib.delayed(describe_image)(image, label) for image in images)
    classDescriptors = np.array(classDescriptors, dtype=object)

    print('class', classDescriptors.shape)

    return classDescriptors

def build_image_descriptors(imagesByLabels):
    labeledDescriptors = np.empty((0,2))

    for label in range(len(imagesByLabels)):
        labeledDescriptors = np.concatenate((labeledDescriptors, describe_images_in_class(imagesByLabels[label], label)))

    print('labeled1', labeledDescriptors.shape)

    return labeledDescriptors

def build_set(set_type):
    start_time = time.perf_counter()

    print(f'Loading {set_type} dataset...')
    labels = np.array([0,1,2,3,4])
    imagesByLabels = [helpers.get_and_enrich_all_images_from_directory(Path(constants.DATASET_DIR, set_type, str(classType))) for classType in labels]
    print(f'Loaded {sum(len(l) for l in imagesByLabels)} images (with extensions) in {time.perf_counter() - start_time} s')

    print(f'Getting image descriptors...')
    labeledDescriptors = build_image_descriptors(imagesByLabels)
    print(f'Total image loading time: {time.perf_counter() - start_time} s...')

    descriptors, labels = zip(*[(item[0], item[1]) for item in labeledDescriptors])
    descriptors = np.array(descriptors)
    labels = np.array(labels)

    print(descriptors[:4], labels)

    return labels, descriptors

def train(model_output_path):
    # Gets the histogram sets with labels
    print('Loading datasets...')
    load_time_start = time.perf_counter()

    labels = np.array([0,1,2,3,4])
    y_train, x_train = build_set('train')
    y_test, x_test = build_set('test')

    scaler = preprocessing.StandardScaler()
    scaler.fit_transform(x_train)
    x_train = preprocessing.scale(x_train)

    print(f'Loaded datasets. Time taken: {time.perf_counter() - load_time_start} s')
    print('Number of samples', x_train)
    
    clf = KNeighborsClassifier(n_neighbors=1, n_jobs=-1)
    clf.fit(x_train, y_train)

    if os.path.exists(model_output_path):
        joblib.dump(clf, model_output_path)
    else:
        print("Cannot save trained svm model to {0}.".format(model_output_path))

    y_predict=clf.predict(x_test)
    accuracy = clf.score(x_test, y_test)

    print("\nConfusion matrix:")
    print(f"Labels: {labels}\n")
    print(confusion_matrix(y_test, y_predict, labels=labels))
 
    print("\nClassification report:")
    print(classification_report(y_test, y_predict))
    print(f"Accuracy: {accuracy * 100}%")

def main():
    train('./model.xml')

if __name__ == '__main__':
    main()
