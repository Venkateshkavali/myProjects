# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 21:16:21 2020

@author: pvini
"""
def determine_data_type(value):
    """
    The function takes a string input and determines its data type to be either a float, int, or string. 
    """
    value2 = value.replace(',', '.')
    try:
        int(value2)
        return int
    except:
        try:
            float(value2)
            return float
        except:
            return str

def determine_data_type_of_list(values):
    """
    Function takes a list of strings and determines their data type. 

    """
    str_data_type = False
    float_data_type = False
    int_data_type = False
    
    for value in values:
        if determine_data_type(value) == str:
            str_data_type = True
        elif determine_data_type(value) == float:
            float_data_type = True
        else:
            int_data_type = True
            
    if str_data_type == True:
        return str
    elif float_data_type == True:
        return float
    elif int_data_type == True:
        return int
    else:
        return None
    
format_field = "GT:AD:DP:GQ:PGT:PID:PL"
sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG104': '0/1:34,38:72:99:.:.:938,0,796',
             'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG204': '0/1:34,38:72:99:.:.:938,0,796',
             'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG304': '0/1:34,38:72:99:.:.:938,0,796',
             'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
             'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
             'XG404': '0/1:34,38:72:99:.:.:938,0,796'}

def format_sample_fields(format_field, sample_field):
    """
    Format the sample fields given the description above. Data is already provided.
    """
    
    changed_format = {}
    sorted_changed_format = {}
    sample_value = []
    
    sorted_format = format_field.split(":")
    for key,value in sample_field.items():
        sample_value = value.split(":")
        changed_format[key] = {}
        for i in range(len(sorted_format)):
            changed_format[key][sorted_format[i]] = sample_value[i]
        
    for key,value in changed_format.items():
        sorted_changed_format[key] = {}
        for value_key,value_value in sorted(value.items()):
            sorted_changed_format[key][value_key] = value_value
            
    return sorted_changed_format

def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 
    """
    
    
    header_split = []
    line_dict = {}
    sample_field = {}
    format_dict = {1:1,2:2,3:3}
    format_data = []
    format_field = ''
    flag = False
    
    line_list = line.split()
    
    for ele_header in header:
        if flag == False:
            if ele_header.upper() == "FORMAT":
                ele_header = "SAMPLE"
                flag = True
            header_split.append(ele_header)
        else:
            format_data.append(ele_header)
            
    for i in range(len(format_data)):
        sample_field[format_data[i]] = line_list[len(header_split)+i]
        
    format_field = line_list[len(header_split)-1]
    
    format_dict = format_sample_fields(format_field, sample_field)
    
    for i in range(len(header_split)):
        if header_split[i] == "SAMPLE":
            line_dict[header_split[i]] = {}
            line_dict[header_split[i]] = format_dict
        else:
            line_dict[header_split[i]] = line_list[i]
            
    return line_dict

def read_vcf_file(filename):
    """
    See description above
    """
    header = []
    line_dict_list = []
    """line_dict = {}"""
    with open(filename) as file:
        for line in file:
            if line.strip():
                line_dict = {}
                if line[0:6] == "#CHROM":
                    header = line[1:].split()
                    continue
                elif line[0] != "#":
                    line.encode('ascii','ignore')
                    line_dict = create_dict_from_line(header, line.strip())
                    line_dict_list.append(line_dict)
                else:
                    continue
        
    for i in range(len(line_dict_list)):
        for key,value in sorted(line_dict_list[i].items()):
            line_dict_list[i][key] = value
        """line_dict_list[i] = sorted_line_dict"""
    return line_dict_list

            
def extract_info_field(data):
    """
    See description in part 6
    """
    info_list = []
    for i in range(len(data)):
        for key,value in data[i].items():
            if key.upper() == "INFO":
                info_list.append(v)
    
    return info_list

def create_dictionary_of_info_field_values(data):
    """
    See description of part 7
    """
    info_field_dict = {}
    info_split = []
    key_list = []
    for ele in data:
        ele = ele.replace("\\x3b",",")
        ele = ele.replace("\\x3d","=")
        info_split = ele.split(";")    
        for info in info_split:
            key_parser = ''
            value_parser = ''
            flag = False
            key_flag = False
            for char in info:
                if char == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key_parser += char
                else:
                    value_parser += char
            if value_parser != '':
                if len(key_list) == 0:
                    info_field_dict = {}
                    info_field_dict[key_parser] = []
                    if value_parser != '.':
                        info_field_dict[key_parser].append(value_parser)
                else:
                    for ele in key_list:
                        if ele == key_parser:
                            if value_parser != '.':
                                info_field_dict[key_parser].append(value_parser)
                            key_flag = True
                            break
                            
                if key_flag == False:
                    info_field_dict[key_parser] = []
                    if value_parser != '.':
                        info_field_dict[key_parser].append(value_parser)
                    
                key_list.append(key_parser)
                #print(info_field_dict)
    return info_field_dict

def determine_data_type_of_info_fields(data):
    """
    See desription in part 8
    """
    data_type_dict = {}
    data_type = ''
    for key,value in data.items():
        data_type = determine_data_type_of_list(value)
        data_type_dict[key] = data_type
    return data_type_dict

def format_data(data, info_field_data_type):
      
    info_field_list = []
    data_type = None
    info_str = ''
    info_split = []
    for i in range(len(data)):
        #info_field_dict_fn = create_dictionary_of_info_field_values([data[i]['INFO']])
        info_field_dict_fn = {}
        info_field_dict = {}
        info_str = data[i]['INFO']
        info_str = info_str.replace("\\x3b",",")
        info_str = info_str.replace("\\x3d","=")
        info_split = info_str.split(";")
        for info in info_split:
            key_parser = ''
            value_parser = ''
            flag = False
            for char in info:
                if char == "=" and flag == False:
                    flag = True
                    continue
                if flag == False:
                    key_parser += char
                else:
                    value_parser += char
            if value_parser != '':
                if value_parser != '.':
                    info_field_dict_fn[key_parser] = value_parser
                
        for key,value in info_field_dict_fn.items():
            data_type = info_field_data_type[key]
            if data_type == int:
                info_field_dict[key] = int(value)
            elif data_type == float:
                info_field_dict[key] = float(value)
            elif data_type == str:
                info_field_dict[key] = str(value)
            else:
                info_field_dict[key] = ''
            
        info_field_list.append(info_field_dict)
        data[i]['POS'] = int(data[i]['POS'])
        data[i]['QUAL'] = float(data[i]['QUAL'])
        
    for i in range(len(info_field_list)):
        data[i]['INFO'] = info_field_list[i]
        
    return data

def save_data_as_json(data, filename):
    import json
    
    with open(filename, 'w') as outfile:
        json.dump(data, outfile,sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
        
def load_data_from_json(filename):
    import json
    
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def find_variant(CHROM, REF, ALT, POS, filename):
    variant_list = []

    data_loaded = load_data_from_json(filename)
    
    for i in range(len(data_loaded)):
        if data_loaded[i]['CHROM'] == CHROM and data_loaded[i]['REF'] == REF and data_loaded[i]['ALT'] == ALT and data_loaded[i]['POS'] == POS:
            variant_list.append(data_loaded[i])
    
    return(variant_list)