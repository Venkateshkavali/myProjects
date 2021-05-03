# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:13:39 2020

@author: venka
"""

def create_dictionary_of_info_field_values(data):
    """
    See description of part 7
    """
    # YOUR CODE HERE
    dict1 = {}
    f1 = []
    list1 = []
    for i in data:
        i = i.replace("\\x3b",",")
        i = i.replace("\\x3d","=")
        f1 = i.split(";")    
        for info in f1:
            key1 = ''
            value1 = ''
            flag = False
            key_flag = False
            for char in info:
                if char == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key1 += char
                else:
                    value1 += char
            if value1 != '':
                if len(list1) == 0:
                    dict1 = {}
                    dict1[key1] = []
                    if value1 != '.':
                        dict1[key1].append(value1)
                else:
                    for j in list1:
                        if j == key1:
                            if value1 != '.':
                                dict1[key1].append(value1)
                            key_flag = True
                            break
                            
                if key_flag == False:
                    dict1[key1] = []
                    if value1 != '.':
                        dict1[key1].append(value1)
                    
                list1.append(key1)
                #print(info_field_dict)
    return dict1