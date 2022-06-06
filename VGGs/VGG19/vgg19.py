# -*- coding: utf-8 -*-
"""VGG19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10MyxfQK-Iph_mzMCKJL1ONS2Xhx5X1Ru
"""

import cv2
import os
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras.models import Model
import cv2
import os
from google.colab import drive

drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/Code-5000

from keras.applications import vgg19
img_rows, img_cols = 224, 224

model = vgg19.VGG19(weights='imagenet',
                    include_top = False,
                    input_shape = (img_rows, img_cols, 3))

for layer in model.layers:
    layer.trainable = False

def layer_adder(bottom_model, num_classes):
    top_model = bottom_model.output
    top_model = GlobalAveragePooling2D()(top_model)
    top_model = Dense(1024,activation='relu')(top_model)
    top_model = Dense(512,activation='relu')(top_model)
    top_model= Dropout(0.5)(top_model)
    top_model = Dense(num_classes,activation='relu')(top_model)
    return top_model

num_classes = 2
FC_Head = layer_adder(model, num_classes)

model = Model(inputs = model.input, outputs = FC_Head)

print(model.summary())

from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping

from keras.preprocessing.image import ImageDataGenerator

trdata = ImageDataGenerator()
traindata = trdata.flow_from_directory(directory="train",target_size=(224,224),batch_size=16)
tsdata = ImageDataGenerator()
testdata = tsdata.flow_from_directory(directory="validation", target_size=(224,224),batch_size=16)


#model 20

checkpoint1 = ModelCheckpoint(
    "./vgg19_20.h5",
    monitor='val_accuracy',
    verbose=1,
    save_best_only=True,
    mode='auto',
    period=1)

early1 = EarlyStopping(
    monitor='val_accuracy',
    min_delta=0,
    patience=20,
    verbose=1,
    mode='auto',
    restore_best_weights = True)

model.compile(Adam(lr=0.001),
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

hist = model.fit_generator(
    #steps_per_epoch=100,
    generator=traindata,
    validation_data= testdata,
    #validation_steps=100,
    epochs=10,
    callbacks=[checkpoint1,early1])

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/test

# Accuracy/ Sensivity / Specificity
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
import matplotlib.pyplot as plt
import shutil, os 
import random

model20 = load_model('/content/drive/My Drive/Code-5000/vgg19_20.h5')

files = os.listdir()
pos=0
neg=0

for i in range (0,len(files)):
    
    test_image = image.load_img(files[i], target_size=(224,224))
    images = image.img_to_array(test_image)
    images = np.expand_dims(images, axis=0)
    prediction = model20.predict(images)

    if prediction[0][0] > prediction[0][1] and files[i][0]=='N':
        neg+=1

    if prediction[0][0] < prediction[0][1] and files[i][0]=='D':
        pos+=1

print("Accuracy :",((neg+pos)/len(files))*100,"% \n")
print("SENSIVITY:",(pos/30)*100,"%\n")
print("SPECIFICITY:",(neg/40)*100,"%\n")


##EXAMPLE of PREDICTION 
#in case to show to Dr. Markus 

##normal
test_image = image.load_img("./N_1_2.png", target_size=(224,224))
##showing image
img1 = np.asarray(test_image)
plt.imshow(img1)

images = image.img_to_array(test_image)
images = np.expand_dims(images, axis=0)
prediction = model20.predict(images)

if prediction[0][0] > prediction[0][1]:
    print("IS a NORMAL CASE")

if prediction[0][0] < prediction[0][1]:
    print("IS a ABNORMAL CASE")

##abnormal
test_image = image.load_img("./D_1_3.png", target_size=(224,224))
##showing image
img2 = np.asarray(test_image)
plt.imshow(img2)

images = image.img_to_array(test_image)
images = np.expand_dims(images, axis=0)
prediction = model20.predict(images)

if prediction[0][0] > prediction[0][1]:
    print("IS a NORMAL CASE")

if prediction[0][0] < prediction[0][1]:
    print("IS a ABNORMAL CASE")
