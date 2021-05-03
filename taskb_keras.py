# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 20:19:03 2020

@author: venka
"""

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K


batch_size = 128
num_classes = 10
epochs = 12

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
import util_mnist_reader as mnist_reader
X_train, y_train = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='train')
X_test, y_test = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='t10k')


print('x_train Shape:', X_train.shape)
print('y_train Shape:', y_train.shape)
print('x_test  Shape:', X_test.shape)
print('y_test  Shape:', y_test.shape)


#matplotlib inline
from matplotlib import pyplot as plt
print('Truth Label:', y_train[0])
#plt.imshow(X_train[0])
#plt.title('Sample input image')



X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
print('x_train shape:', X_train.shape)
print(X_train.shape[0], 'train samples')
print(X_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


model = Sequential()


model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

#model.summary()

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(),
              metrics=['accuracy'])

model.fit(X_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_test, y_test))
score = model.evaluate(X_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])