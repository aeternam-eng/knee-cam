# Hugo Brandão de Oliveira | 640727 | Engenharia de Computação | Coração Eucarístico
# Gabriell Murta de Paula Nunes | 636042 | Engenharia de Computação | Coração Eucarístico
# Joao Antônio Ferreira Neto | 640846 | Engenharia de Computação | Coração Eucarístico
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG19
from tensorflow.keras import layers
from tensorflow.keras import models
from keras.optimizers import Adam

import time
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix , classification_report
start_time = time.time()

dataset_train_directory = r"./src/databinary/kneeKL224/train/"
dataset_test_directory = r"./src/databinary/kneeKL224/val/"
dataset_val_directory = r"./src/databinary/kneeKL224/test/"

batch_size   = 25
input_shape  = (224, 224, 3)
random_state = 42
alpha        = 1e-5
epoch        = 70
image_size = [224,224]

train_datagen = ImageDataGenerator(
    horizontal_flip=True,
    rotation_range=30,
    fill_mode='nearest',
)

train_generator = train_datagen.flow_from_directory( 
    dataset_train_directory, 
    target_size=image_size, 
    color_mode="rgb", 
    batch_size=batch_size, 
    class_mode="categorical", 
    shuffle=True
)

teste_datagen = ImageDataGenerator()
test_generator = teste_datagen.flow_from_directory(
    dataset_test_directory,
    target_size=image_size,
    color_mode="rgb",
    batch_size=1,
    class_mode=None,
    shuffle=False,
)

val_datagen = ImageDataGenerator()
validation_generator = val_datagen.flow_from_directory(
    dataset_val_directory,
    target_size = image_size,
    batch_size = batch_size,
    color_mode="rgb",
    class_mode="categorical",
    shuffle = True
)

filepath="transferlearning_weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')

lr_reduce = ReduceLROnPlateau(monitor='val_acc', factor=0.1, min_delta=alpha, patience=5, verbose=1)

callbacks = [checkpoint, lr_reduce]
conv_base = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)
conv_base.summary()

conv_base.trainable = True
set_trainable = False

for layer in conv_base.layers:
  if layer.name == 'block5_conv1':
    set_trainable = True
  if set_trainable:
    layer.trainable = True
  else:
    layer.trainable = False
    
conv_base.summary()

model = models.Sequential()
model.add(conv_base)
model.add(layers.GlobalAveragePooling2D())
model.add(layers.BatchNormalization())
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2, activation='softmax'))

model.summary()

model.compile(loss='binary_crossentropy',
                  optimizer=Adam(lr=0.00005),
                  metrics=['acc'])

STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=validation_generator.n//validation_generator.batch_size

history = model.fit(train_generator,
                      steps_per_epoch=STEP_SIZE_TRAIN,
                      validation_data=validation_generator,
                      validation_steps=STEP_SIZE_VALID,
                      callbacks=callbacks,
                      epochs=epoch)
model.save('./CNNBinary/CNNBynary.h5')

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig("./CNNBinary/Info/binaryModelAccuracy.png")
plt.clf()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig("./CNNBinary/Info//binaryModelLoss.png")
plt.clf()

STEP_SIZE_TEST = test_generator.n//test_generator.batch_size
test_generator.reset()
pred=model.predict_generator(test_generator,
                              steps=STEP_SIZE_TEST,
                              verbose=1)
pred = np.argmax(pred,axis = 1) 
y_true = test_generator.classes
cm = confusion_matrix(y_true, pred)
fig, ax = plot_confusion_matrix(conf_mat=cm ,  figsize=(5, 5))
plt.savefig("./CNNBinary/Info/binaryConfusionMatrix.png")
plt.clf()

with open("./CNNBinary/Info/binaryCNNClassificationReport.txt", "w") as file:
    file.write(classification_report(y_true,pred))

with open("./CNNBinary/Info/runTime.txt ", "w") as file:
    file.write("Time Execution " + str((time.time() - start_time)))
