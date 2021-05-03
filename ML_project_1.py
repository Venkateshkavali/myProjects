# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 03:50:20 2020

@author: venka
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
#names=['Precip','MaxTemp','MeanTemp','Snowfall']
df = pd.read_excel("E:/SUNY BUFFALO/Machine Learning/Weather.xlsx")
print(df)
df.plot(x='MaxTemp',y='MinTemp',kind='scatter')
plt.show()
df.plot(x='Precip',y='MinTemp',kind='scatter')
plt.show()
df.plot(x='MeanTemp',y='MinTemp',kind='scatter')
plt.show()
df.plot(x='Snowfall',y='MinTemp',kind='scatter')
plt.show()

#plt.scatter(df.iloc[:,0],df.iloc[:,4])
#plt.show()
#plt.scatter(df.iloc[:,1],df.iloc[:,4])
#plt.show()
#plt.scatter(df.iloc[:,2],df.iloc[:,4])
#plt.show()
#plt.scatter(df.iloc[:,3],df.iloc[:,4])
#plt.show()

df1 = df.copy()
train_data = df1.sample(frac=0.8)
test_data = df1.drop(train_data.index)


X_test = test_data[['MaxTemp', 'Precip', 'MeanTemp', 'Snowfall']]
Y_test = test_data['MinTemp']

X_test = np.array(X_test)
Y_test = np.array(Y_test)

X = train_data[['MaxTemp', 'Precip', 'MeanTemp', 'Snowfall']]
Y = train_data['MinTemp']
# plt.scatter(X, Y)
# plt.show()

X = np.array(X)
Y = np.array(Y)
w = np.zeros((1, 4))
c = 0
learning_rate = 0.0001  # The learning Rate
iterations = 1000  # The number of iterations to perform gradient descent
n = float(len(X))  # Number of elements in X

costs = []
epochs = []

# Performing Gradient Descent
for i in range(iterations):
    epochs.append(i)
    # Predicted_Y = m1*X['Precip']+m2*X['MaxTemp']+m3*X['MeanTemp']+m4*X['Snowfall'] + c  # The current predicted value of Y
    Predicted_Y = np.dot(w, X.T) + c
#    w_derivate = (-2 / n) * np.sum(np.multiply(X.T, (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w1_derivate = (-2 / n) * np.sum(np.multiply(((X[:,0]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w2_derivate = (-2 / n) * np.sum(np.multiply(((X[:,1]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w3_derivate = (-2 / n) * np.sum(np.multiply(((X[:,2]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w4_derivate = (-2 / n) * np.sum(np.multiply(((X[:,3]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m

    c_derivative = (-2 / n) * np.sum(Y - Predicted_Y)  # Derivative wrt c
    w[:,0] = w[:,0] - learning_rate * w1_derivate
    w[:,1] = w[:,1] - learning_rate * w2_derivate
    w[:,2] = w[:,2] - learning_rate * w3_derivate
    w[:,3] = w[:,3] - learning_rate * w4_derivate
    #    m2 = m2 - learning_rate * m_derivate
    #    m3 = m4 - learning_rate * m_derivate
    #    m4 = m4 - learning_rate * m_derivate# Update m
    c = c - (learning_rate * c_derivative)

    # Update c

    #cost function
    cost = (np.sum((Y - Predicted_Y)**2))/(2*n)

    costs.append(cost)

print(w, c)
#print(costs[0])
print(costs[-1])

#print('costssssss')
#print(costs)

plt.plot(epochs,costs)
plt.show()



Predicted_Y_test = np.dot(w, X_test.T) + c
cost_test = (np.sum((Y_test - Predicted_Y_test) ** 2)) / (2 * n)
print('test error')
print(cost_test)



#########################################################################
X_test = test_data[['MaxTemp', 'Precip', 'MeanTemp', 'Snowfall']]
Y_test = test_data['MinTemp']

X_test = np.array(X_test)
Y_test = np.array(Y_test)

X = train_data[['MaxTemp', 'Precip', 'MeanTemp', 'Snowfall']]
Y = train_data['MinTemp']
# plt.scatter(X, Y)
# plt.show()

X = np.array(X)
Y = np.array(Y)
w = np.zeros((1, 4))
c = 0
learning_rate = 0.0000001 # The learning Rate
iterations = 5000  # The number of iterations to perform gradient descent
n = float(len(X))  # Number of elements in X

costs = []
epochs = []

# Performing Gradient Descent
for i in range(iterations):
    epochs.append(i)
    # Predicted_Y = m1*X['Precip']+m2*X['MaxTemp']+m3*X['MeanTemp']+m4*X['Snowfall'] + c  # The current predicted value of Y
    Predicted_Y = np.dot(w, (np.square(X)).T) + c
    w1_derivate = (-2 / n) * np.sum(np.multiply((np.square(X[:,0]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w2_derivate = (-2 / n) * np.sum(np.multiply((np.square(X[:,1]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w3_derivate = (-2 / n) * np.sum(np.multiply((np.square(X[:,2]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m
    w4_derivate = (-2 / n) * np.sum(np.multiply((np.square(X[:,3]).T), (np.array(Y) - Predicted_Y)))  # Derivative wrt m

    c_derivative = (-2 / n) * np.sum(Y - Predicted_Y)  # Derivative wrt c
    w[:,0] = w[:,0] - learning_rate * w1_derivate
    w[:,1] = w[:,1] - learning_rate * w2_derivate
    w[:,2] = w[:,2] - learning_rate * w3_derivate
    w[:,3] = w[:,3] - learning_rate * w4_derivate

    #    m2 = m2 - learning_rate * m_derivate
    #    m3 = m4 - learning_rate * m_derivate
    #    m4 = m4 - learning_rate * m_derivate# Update m
    c = c - (learning_rate * c_derivative)

    # Update c

    #cost function
    cost = (np.sum(np.square(Y - Predicted_Y)))/(2*n)

    costs.append(cost)

print(w, c)
print(costs[-1])

#print('costssssss')
#print(costs)

plt.plot(epochs,costs)

plt.show()



Predicted_Y_test = np.dot(w, (np.square(X_test)).T) + c
cost_test = ((np.sum((Y_test - Predicted_Y_test) ** 2)) / (2*n))
print('test error (Polynmial)')
print(cost_test)


# Making predictions