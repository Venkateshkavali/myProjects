# -*- coding: utf-8 -*-
"""

@author: venka
"""
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn import preprocessing





import util_mnist_reader as mnist_reader
X_train, y_train = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='train')
X_test, y_test = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='t10k')


X_train = preprocessing.scale(X_train)
X_test = preprocessing.scale(X_test)



nb_classes = 10
targets = np.array(y_train).reshape(-1)
one_hot_targets = np.eye(nb_classes)[targets]

# Your code goes here . . .
#n_x = X_train.shape[0] # size of input layer`
#n_h = 10
#n_y = y_train.shape[0] 
#m1 = np.random.randn(n_h,n_x) * 0.01
#c1 = np.zeros(shape=(n_h, 1))
#m2 = np.random.randn(n_y,n_h) * 0.01
#c2 = np.zeros(shape=(n_y, 1))
## size of output layer`
# initializing the variables,
epoch=500 # number of training iterations
learning_rate1=0.001
learning_rate2=0.00001
 # learning rate
m = float(len(X_train)) 
# initializing weight and bias
m1=np.random.rand(784,10)
c1=np.random.rand(10)
m2=np.random.rand(10,10)
c2=np.random.rand(10)
#m1=np.ones((784,10))
#c1=np.ones((10))
#m2=np.ones((10,10))
#c2=np.ones((10))
los =[]
epochs=[]
b = np.zeros((y_train.size, y_train.max()+1))
b[np.arange(y_train.size),y_train] = 1
    
b_test = np.zeros((y_test.size, y_test.max()+1))
b_test[np.arange(y_test.size),y_test] = 1
    
# training the model
for i in range(epoch):
    epochs.append(i)
#
#    z=np.dot(X_train,w) + c
#    
#    pred_Y = 1/(1 + np.exp(-z))
#    z_out=np.dot(pred_Y,w_out) + c_out
#    
#    op = 1/(1 + np.exp(-z_out))
    z1=np.dot(X_train,m1) + c1
    a1 = 1/(1 + np.exp(-z1))
    z2=np.dot(a1,m2) + c2
    
    
    
    a2 = ((np.exp(z2).T)/(np.sum((np.exp(z2)).T,axis=0))).T
    loss = np.sum(-np.multiply(b, np.log(a2)))
    print(loss)
    los.append(loss)
    
    
    
    dm2= np.dot(a1.T,(a2-b))
    dc2=np.sum((a2-b),axis=0)
    dm1 = np.dot(np.multiply(np.multiply(np.dot((a2 - b),m2.T),a1),(1-a1)).T,X_train).T #calculating derivative of loss function with respect to hidden layer weights.
    dc1 = np.sum(np.multiply(np.multiply(np.dot((a2 - b),m2.T),a1),(1-a1)),axis = 0) #calculating derivative o
    
    m1 = m1 - learning_rate1 * dm1
    m2= m2- learning_rate2 * dm2
    c1= c1- learning_rate1 * dc1
    c2 = c2-learning_rate2 * dc2

plt.plot(epochs,los)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show


z1=np.dot(X_test,m1) + c1
a1 = 1/(1 + np.exp(-z1))
z2=np.dot(a1,m2) + c2
a2 = ((np.exp(z2).T)/(np.sum((np.exp(z2)).T,axis=0))).T
print(a2)
y_pred= np.argmax(a2,axis=1)
    

    
print(y_pred)
print(y_test)

c=0
for i in range(len(y_pred)):
    if y_pred[i] == y_test[i]:
        c+=1
print("accuracy", c/len(y_test))



from sklearn import metrics


#confusion matrix
# columns ----predictions for each label,
# rows will------actual # of instances for each label.
print(metrics.confusion_matrix(y_test,y_pred))
# Printing the precision and recall, among other metrics
print(metrics.classification_report(y_test,y_pred))