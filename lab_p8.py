# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 23:17:24 2020

@author: venka
"""
def determine_data_type_of_list(values):
    """
    Function takes a list of strings and determines their data type. 

    """
    # YOUR CODE HERE
    from ast import literal_eval
    my_list=[]
    for element in values:
        try:
             my_list.append(type(literal_eval(element)))
        except (ValueError, SyntaxError):
            my_list.append(str)
    #print(my_list)
    #element = element.strip('\'')
    if str in my_list :
        return str
    elif float in my_list:
        return float
    elif int in my_list:
        return int

def determine_data_type_of_info_fields(data):
    """
    See desription in part 8
    """
    dict1 = {}
    data1 = ''
    for key,value in data.items():
        data1 = determine_data_type_of_list(value)
        dict1[key] = data1
    return dict1

def format_data(data, info_field_data_type):
      
    list1 = []
    str1 = None
    str2 = ''
    f2 = []
    for i in range(len(data)):
        f1 = {}
        dict1 = {}
        str2 = data[i]['INFO']
        str2 = str2.replace("\\x3b",",")
        str2 = str2.replace("\\x3d","=")
        f2 = str2.split(";")
        for info in f2:
            key1 = ''
            value1 = ''
            flag = False
            for char in info:
                if char == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key1 += char
                else:
                    value1 += char
            if value1 != '':
                if value1 != '.':
                    f1[key1] = value1
                
        for key,value in f1.items():
            str1 = info_field_data_type[key]
            if str1 == int:
                dict1[key] = int(value)
            elif str1 == float:
                dict1[key] = float(value)
            elif str1 == str:
                dict1[key] = str(value)
            else:
                dict1[key] = ''
            
        list1.append(dict1)
        data[i]['POS'] = int(data[i]['POS'])
        data[i]['QUAL'] = float(data[i]['QUAL'])
        
    for i in range(len(list1)):
        data[i]['INFO'] = list1[i]
        
    return data

def save_data_as_json(data, filename):
    # YOUR CODE HERE
    import json
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        
def load_data_from_json(filename):
    import json
    
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def find_variant(CHROM, REF, ALT, POS, filename):
    list1 = []

    data = load_data_from_json(filename)
    #print(data)
    
    for i in range(len(data)):
        if data[i]['CHROM'] == CHROM and data[i]['REF'] == REF and data[i]['ALT'] == ALT and data[i]['POS'] == POS:
            list1.append(data[i])
    
    return(list1)