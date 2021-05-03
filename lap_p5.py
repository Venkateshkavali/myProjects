# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:55:06 2020

@author: venka
"""
def format_sample_fields(format_field, sample_field):
    
   import re
   f1= re.split('[:]',format_field)
   dict1 = dict()
   dict3 = {}
    #dict1_sorted = dict()
   dict2 = sample_field
    #dict2.clear()
    
   for k,v in sample_field.items():
        dict1.clear();
        v1=re.split('[:]',v)
        #print("v1 is ",v1)
        j=0
        for n in f1:
            dict4 = {}
            dict1[n]=v1[j]
            j+=1
            for key in sorted(dict1.keys()):
                dict4[key] = dict1[key]
        #print("dict1 is ",dict1)
        dict2[k]=dict(dict4)
        #print("dict2 is ",dict2)
        
   for key in sorted(dict2.keys()):
        dict3[key] = dict2[key]
   return dict3
def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 
    """
    import re
    f1= re.split('[\t]',line)
    f2=f1
    dict1 = dict.fromkeys(header)
    #print(f2)
    res = {} 
    res_a= {}
    for key in dict1: 
        for value in f2: 
            res[key] = value
            res_a[key] = value
            f2.remove(value)
            
            break
    res1 = res
    #print(f2)
    #print(res)
    delete = []
    
    for k,v in res1.items():
        if k == 'FORMAT':
            format_field = res[k]
            
            delete.append(k)
            break
        else:
            delete.append(k)
    #print(delete)

    for i in delete:
        del res1[i]
    
    for k in res1:
        res_a.pop(k)
    res_a.pop('FORMAT')
    sample = format_sample_fields(format_field, res1)  
    res_a.update(SAMPLE = sample)    
    return res_a
    
#    dict1 = dict(zip(header,line.split()))
#    #print(dict1)
#    dict2 = {}
#    dict3 = {}
#    dict4 = {}
#    format_field1 = dict1[header[8]]
#    for i in range(0,len(header)):
#        p = header[i]
#        if i < 8:
#            dict2[p] = dict1[p]
#        elif i > 8:
#            dict3[p] = dict1[p]
#    dict4 = format_sample_fields(format_field1, dict3)
#    dict2['SAMPLE'] = dict4
#    return dict2

def read_vcf_file(filename):
    """
    See description above
    """
    # YOUR CODE HERE
    header = []
    list1 = []
    """line_dict = {}"""
    with open(filename) as file:
        for line in file:
            if line.strip():
                dict1 = {}
                if line[0:6] == "#CHROM":
                    header = line[1:].split()
                    continue
                elif line[0] != "#":
                    line.encode('ascii','ignore')
                    dict1 = create_dict_from_line(header, line.strip())
                    list1.append(dict1)
                else:
                    continue
        
    for i in range(len(list1)):
        for k,v in sorted(list1[i].items()):
            list1[i][k] = v
        """line_dict_list[i] = sorted_line_dict"""
    return list1