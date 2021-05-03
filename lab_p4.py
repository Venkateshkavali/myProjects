def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 
    """
     YOUR CODE HERE
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
        
    
 
