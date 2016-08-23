__author__ = 'Vishal'

import settings
import csv
from pprint import pprint

def generate_file_to_functions_map():
    header_ignore_flag = 1

    with open(BASE_PATH + 'LocMetricsFunctions.csv', 'r') as csv_f:
        for row in csv_f:
            if header_ignore_flag == 1:
                header_ignore_flag = 0
                continue
            #print(row)
            row = row.replace('"','')
            myList = row.replace('\n', '').split(',')
            print(myList[0]+" "+myList[1])
            function_name = myList[1].split('(')[0]
            try:
                function_list = file_to_func_name_map[myList[0]]
            except:
                file_to_func_name_map[myList[0]] = list()
                file_to_func_name_map[myList[0]].append(function_name)
                continue
            file_to_func_name_map[myList[0]].append(function_name)
    csv_f.close()


def generate_class_to_functions_map():
    class_id = "class_1"
    print(file_to_func_name_map)
    file_list = file_to_func_name_map.keys()

    for file in file_list:
        function_list = file_to_func_name_map[file]
        for function in function_list:
            if '::' in function:
                class_name = function.split(':')[0]
            else:
                class_name = file

            try:
                curlist = class_to_func_name_map[class_name]
            except:
                class_to_func_name_map[class_name] = list()
            class_to_func_name_map[class_name].append(function)

    pprint(class_to_func_name_map)



DATASET_NAME = settings.DATASET_NAME
BASE_PATH = settings.BASE_PATH
START = settings.START
END = settings.END
file_to_func_name_map = dict()
class_to_func_name_map = settings.class_to_func_name_map

generate_file_to_functions_map()
generate_class_to_functions_map()
