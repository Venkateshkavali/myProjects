# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 12:15:31 2020

@author: venka
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv("E:/SUNY BUFFALO/Machine Learning/project 2/TaskA_Dataset.CSV") #reading the csv file


df1 = df.copy()
train_data = df1.sample(frac=0.8)
test_data = df1.drop(train_data.index)

df.iloc[:, 0:2]

X = train_data.iloc[:,2:]
Y = train_data['M']


X = np.array(X)
Y = np.array(Y)
y_train=[]
for i in range(len(Y)):
    if Y[i] == 'M':
        y_train.append(1)
    else:
        y_train.append(0)
w = np.random.uniform(0,1)
c = 0


learning_rate = 0.0000001  # The learning Rate
iterations = 1000  # The number of iterations to perform gradient descent
n = float(len(X))  # Number of elements in X

los = []
epochs = []
W=np.zeros((1,30))
# Performing Gradient Descent
for i in range(iterations):
    epochs.append(i)
    z = np.dot(W,X.T) + c
    Predicted_Y = 1/(1+np.exp(-z))
    for i in range(30):# finding weigts for 30 attributes
        w_derivative = (-2 / n) * np.sum(np.multiply(((X[:,i]).T), (y_train - Predicted_Y)))
        W[:,i] = W[:,i] - learning_rate * w_derivative
    c_derivative = (-2 / n) * np.sum(y_train - Predicted_Y)
    c = c - learning_rate* c_derivative
    loss = (np.sum((y_train - Predicted_Y)**2))/(2*n)# finding loss for the training data values
    los.append(loss)
    
print(W,c)

plt.plot(epochs,los) # plotting epochs vs loss 
plt.title('Epochs Vs Loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.show()
X_test = test_data.iloc[:,2:] # data for testing 
Y_test = test_data['M']

X_test = np.array(X_test)
Y_test = np.array(Y_test)
# taking 1 and 0 for malignant and Benign tumors respectively
y_test=[]
for i in range(len(Y)):
    if Y[i] == 'M':
        y_test.append(1)
    else:
        y_test.append(0)
# Predicting for testing data 
for i in range(len(X_test)):
    z= np.dot(W,X.T) + c
    Predicted_Y = 1/(1+np.exp(-z))
print('testing data loss')
loss = (np.sum((y_train - Predicted_Y)**2))/(2*n)
print(loss)


# finding the accuracy 
training_accuracy=[]
list1=Predicted_Y.tolist()
list1= list1[0]
for i in range(len(list1)):
    if list1[i]>=0.5:
        training_accuracy.append(1)
    else:
        training_accuracy.append(0)
tp=0 # true positive
tn=0 # true negative
fp=0 #false positive

fn=0# false negative
for i in range(len(training_accuracy)):
    if y_train[i] == 1 & training_accuracy[i] == 1:
        tp=tp+1
    if y_train[i] == 0 & training_accuracy[i] == 0:
        tn=tn+1
    if y_train[i] == 1 & training_accuracy[i] == 0:
        fn=fn+1
    if y_train[i] == 0 & training_accuracy[i] == 1:
        fp=fp+1
        
accuracy = (tp+tn)/(tp+tn+fn+fp)
precision= tp/(tp+fp)
recall= tp/(tp+fn)


print(accuracy,precision,recall)


