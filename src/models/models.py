# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico
import os
import joblib
import tensorflow as tf
from pathlib import Path

from shared.helpers import *
import shared.constants as constants

# Carrega modelo raso
def load_shallow_model(binary):
    if os.path.exists(constants.MODELS_DIR):
        return joblib.load(Path(constants.MODELS_DIR, 'shallow_bin.sav' if binary else 'shallow_multi.sav'))
    else:
        print("Failure loading shallow model")
        return None

# Carrega modelo CNN
def load_cnn_model(binary):
    if os.path.exists(constants.MODELS_DIR):
        model = tf.keras.models.load_model(Path(constants.MODELS_DIR, 'CNNBynary.h5' if binary else 'CNN.h5'))
        print(model.summary())
        return model
    else:
        print("Failure loading cnn model")
        return None

# Executa CNN binária para imagem individual
def run_binarycnn(image):
    model = load_cnn_model(True)

    result = model.predict(np.array([image]))
    result = np.argmax(result, axis=1)

    return 'Arthrosis' if result == 0 else 'Normal'

# Executa CNN multiclasse para imagem individual
def run_multiclasscnn(image):
    model = load_cnn_model(False)
    
    result = model.predict(np.array([image]))

    return np.argmax(result, axis=1)

# Executa raso binário para imagem individual
def run_binaryshallow(image):
    descriptors = get_image_descriptors(image, use_moments=True)

    model = load_shallow_model(True)
    result = model.predict([descriptors])[0]

    return 'Arthrosis' if result == 1 else 'Normal'

# Executa raso multiclasse para imagem individual
def run_multiclassshallow(image):
    descriptors = get_image_descriptors(image, use_moments=True)

    model = load_shallow_model(False)
    result = model.predict([descriptors])

    return result[0]

# Avalia modelo raso no dataset fornecido
def evaluate_shallow_model(model, dataset, dataset_answers, labels):
    start_time = time.perf_counter()

    y_predict=model.predict(dataset)

    return {
        'time': (time.perf_counter() - start_time),
        'report': classification_report(dataset_answers, y_predict),
        'confusion': confusion_matrix(dataset_answers, y_predict, labels=labels)
    }

# Avalia modelo raso no dataset fornecido
def evaluate_cnn_model(model, dataset, dataset_answers, labels):
    start_time = time.perf_counter()
    
    y_predict=model.predict(dataset)
    y_predict=np.argmax(y_predict, axis=1)

    return {
        'time': (time.perf_counter() - start_time),
        'report': classification_report(dataset_answers, y_predict),
        'confusion': confusion_matrix(dataset_answers, y_predict, labels=labels)
    }
