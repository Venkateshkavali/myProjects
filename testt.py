# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:19:20 2020

@author: venka
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt



import util_mnist_reader as mnist_reader
X_train, y_train = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='train')
X_test, y_test = mnist_reader.load_mnist('E:/SUNY BUFFALO/Machine Learning/project 2/TaskB_Dataset_With_Notebook/TaskB_Dataset_With_Notebook/data/fashion', kind='t10k')


