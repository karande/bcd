__author__ = 'Vishal'
# !/usr/bin/env python
from itertools import groupby
from collections import Counter
import settings
from pprint import pprint

def parse_output():
    with open(BASE_PATH + 'output.txt', 'r') as csv_f:
        for row in csv_f:
            # print(row)
            myList = row.replace('\n', '').split(' ')
            #print(myList)
            source = myList[0]
            destination = myList[4]
            cluster_map[source] = destination
    csv_f.close()

    fg = open(BASE_PATH + "clustermap.csv", "wb")

    for i in sorted(cluster_map, key=int):
        # print(i)
        fg.write(bytes(str.format("{0:0}", int(i)) + " ", 'utf8'))
        fg.write(bytes(str.format("{0:0}", int(cluster_map[str(i)])) + "\r\n", 'utf8'))
    fg.close()

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

    print("CLASS TO FUNCTION MAP:")
    pprint(class_to_func_name_map)

def map_clustering_results():
    caseFlag = 0

    for class_name in class_to_func_name_map.keys():
        for function in class_to_func_name_map[class_name]:
            if "::" in function:
                key1 = function.split("::")[0]
                key2 = function.split("::")[1]
                print(key1 + " & " + key2)
                caseFlag = 2
            else:
                key1 = function
                #print(key1)
                caseFlag = 1

            with open(BASE_PATH + 'nodes.csv', 'r') as f2:
                lineCount = 0
                for line in f2:
                    lineCount = lineCount + 1
                    tokens = line.replace('\n', '').split(',')

                    if caseFlag == 1:
                        if lineCount > START and lineCount < END and key1 in tokens[1]:
                            if tokens[0] == '0':
                                    break
                            try:
                                curList = class_to_ids_map[class_name]
                            except:
                                class_to_ids_map[class_name] = list()
                            class_to_ids_map[class_name].append(cluster_map[tokens[0]])
                            break

                    if caseFlag == 2:
                        if lineCount > START and lineCount < END and key1 in tokens[1] and key2 in tokens[1]:
                            if tokens[0] == '0':
                                    break
                            try:
                                curList = class_to_ids_map[class_name]
                            except:
                                class_to_ids_map[class_name] = list()
                            class_to_ids_map[class_name].append(cluster_map[tokens[0]])
                            break
            f2.close()
    pprint(class_to_ids_map)

def get_file_group_ids():
    for value in class_to_ids_map.keys():
        list1 = class_to_ids_map[value]
        counts = Counter(list1).most_common(1)
        file_to_group_id[value]=counts[0][0]
    print(file_to_group_id)

def generate_f1_scores():

    gTP = 0.0
    gFP = 0.0
    gFN = 0.0
    macro_avg = 0.0
    micro_avg = 0.0
    weighted_micro_avg = 0.0
    cluster_count = 0
    gFunctions = 0
    for class_name in class_to_ids_map.keys():
        list = class_to_ids_map[class_name]
        gFunctions = gFunctions + len(list)

    for class_name in class_to_ids_map.keys():

        cluster_count = cluster_count + 1
        list1 = class_to_ids_map[class_name]
        cluster_id = Counter(list1).most_common(1)[0][0]
        TP = Counter(list1).most_common(1)[0][1] + 0.0
        FP = len(list1)- TP + 0.0
        FN = 0.0
        for t_file in class_to_ids_map.keys():
            c = 0
            if class_name != t_file:
                list2 = class_to_ids_map[t_file]
                b_cluster_id = Counter(list2).most_common(1)[0][0]
                if cluster_id == b_cluster_id:
                    continue
                try:
                    c = Counter(list2)[cluster_id]
                except:
                    continue
                FN = FN + c
        print(str(len(list1))+" "+str(TP)+" "+str(FP)+" "+ str(FN))

        gTP = gTP + TP
        gFP = gFP + FP
        gFN = gFN + FN
        precision = TP / (TP + FP)
        print("Precision:"+ str(precision))

        recall = TP / (TP + FN)
        f1 = (2 * precision * recall) / (precision + recall)

        wf1 = f1 * (len(list1) / gFunctions)
        if precision == 0:
            cluster_count = cluster_count - 1

        macro_avg += f1
        #print(macro_avg)
        weighted_micro_avg += wf1

    gPrecision = gTP / (gTP + gFP)
    gRecall = gTP / (gTP + gFN)
    total_avg = (2 * gPrecision * gRecall)/ (gPrecision + gRecall)
    print(cluster_count)
    macro_avg = macro_avg/cluster_count

    print(str(macro_avg) + "\t" + str(weighted_micro_avg)+"\t"+str(total_avg))
    print(str.format("{0:.03f}", total_avg)+ "\t" + str.format("{0:.03f}", macro_avg)+ "\t" + str.format("{0:.03f}", weighted_micro_avg))


DATASET_NAME = settings.DATASET_NAME
BASE_PATH = settings.BASE_PATH
START = settings.START
END = settings.END
print("\nParsing output:")
cluster_map = settings.cluster_map
class_to_ids_map = settings.class_to_ids_map
file_to_group_id = settings.file_to_group_id
file_to_func_name_map = dict()
class_to_func_name_map = settings.class_to_func_name_map

generate_file_to_functions_map()

generate_class_to_functions_map()

parse_output()

map_clustering_results()

get_file_group_ids()

generate_f1_scores()

print("\nDone!")