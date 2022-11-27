# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico

import cv2
import numpy as np
import tkinter as tk

import shared.constants as constants
import shared.helpers as helpers
import models.models as models

# Menu for file operations (opening image files)
class KLClassificationMenu(tk.Menu):
    def __init__(self, master, on_begin_classification) -> tk.Menu:
        super().__init__(master, tearoff=False)
        
        self.add_command(label='Binary Shallow', command=lambda: on_begin_classification(constants.ClassifierTypes.BinaryShallow))
        self.add_command(label='Multiclass Shallow', command=lambda: on_begin_classification(constants.ClassifierTypes.MulticlassShallow))
        self.add_command(label='Binary CNN', command=lambda: on_begin_classification(constants.ClassifierTypes.BinaryCnn))
        self.add_command(label='Multiclass CNN', command=lambda: on_begin_classification(constants.ClassifierTypes.MulticlassCnn))

        self.add_command(label='Run shallow model in test set', command=lambda: self._run_shallow_model())
        self.add_command(label='Run CNN model in test set', command=lambda: self._run_cnn_model())

    # Executa e avalia o modelo raso
    def _run_shallow_model(self):
        bin_labels = [0,1]
        multi_labels = [0,1,2,3,4]

        shallow_bin = models.load_shallow_model(True)
        shallow_multi = models.load_shallow_model(False)

        bin_test_labels, bin_test_set = helpers.build_set('test', binary=True, with_extensions=False, use_moments=True)
        multi_test_labels, multi_test_set = helpers.build_set('test', binary=False, with_extensions=False, use_moments=True)

        bin_test_set = helpers.scale_dataset(bin_test_set)
        multi_test_set = helpers.scale_dataset(multi_test_set)

        bin_shallow_result = models.evaluate_shallow_model(shallow_bin, bin_test_set, bin_test_labels, bin_labels)
        multi_shallow_result = models.evaluate_shallow_model(shallow_multi, multi_test_set, multi_test_labels, multi_labels)

        tk.messagebox.showinfo(f"BIN Shallow ({bin_shallow_result['time']} s)", f"{bin_shallow_result['report']}\n Confusion matrix: \n{bin_shallow_result['confusion']}")
        tk.messagebox.showinfo(f"MC Shallow ({multi_shallow_result['time']} s)", f"{multi_shallow_result['report']}\n Confusion matrix: \n{multi_shallow_result['confusion']}")

    # Executa e avalia o modelo CNN
    def _run_cnn_model(self):
        bin_labels = [0,1]
        multi_labels = [0,1,2,3,4]

        cnn_bin = models.load_cnn_model(True)
        cnn_multi = models.load_cnn_model(False)

        bin_test_labels, bin_test_set = helpers.build_set('test', binary=True, with_extensions=False, use_moments=False)
        multi_test_labels, multi_test_set = helpers.build_set('test', binary=False, with_extensions=False, use_moments=False)

        bin_test_set = np.array([cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) for image in bin_test_set])
        multi_test_set = np.array([cv2.cvtColor(image, cv2.COLOR_GRAY2BGR) for image in multi_test_set])

        print('input shape', bin_test_set.shape)

        bin_result = models.evaluate_cnn_model(cnn_bin, bin_test_set, bin_test_labels, bin_labels)
        multi_result = models.evaluate_cnn_model(cnn_multi, multi_test_set, multi_test_labels, multi_labels)

        tk.messagebox.showinfo(f"BIN CNN ({bin_result['time']} s)", f"{bin_result['report']}\n Confusion matrix: \n{bin_result['confusion']}")
        tk.messagebox.showinfo(f"MC CNN ({multi_result['time']} s)", f"{multi_result['report']}\n Confusion matrix: \n{multi_result['confusion']}")
