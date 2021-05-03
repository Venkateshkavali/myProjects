# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:57:15 2020

@author: venka
"""

def extract_info_field(data):
   
    
    # YOUR CODE HERE
    f1=[]
    
    for i in range(len(data)):
        for k,v in data[i].items():
            if k.upper() == "INFO":
                f1.append(v)
    
    return f1
    
    
