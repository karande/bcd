__author__ = 'Vishal'
import os
import subprocess
from collections import Counter
from pprint import pprint
import time

DATASET_NAME = "D1"
START = 11
END = 22
BASE_PATH = "datasets/" + DATASET_NAME + "/"
weight_function_seq = 1
weight_call_graph = 1
input = "..\datasets\\" + DATASET_NAME + "\\drwcg.csv"
output = "..\datasets\\" + DATASET_NAME + "\\output.txt"
class_to_func_name_map = dict()
class_to_ids_map = dict()
cluster_map = dict()
file_to_group_id = dict()
data_ref_dict = dict()
file_to_func_name_map = dict()

# Init Settings
def init_settings(tDATASET_NAME, tSTART, tEND, alpha, beta):
    global DATASET_NAME
    DATASET_NAME = tDATASET_NAME
    global START
    START = tSTART
    global END
    END = tEND
    global weight_function_seq
    weight_function_seq = alpha
    global weight_call_graph
    weight_call_graph = beta
    global BASE_PATH
    BASE_PATH = "datasets/" + DATASET_NAME + "/"
    global input
    input = "..\datasets\\" + DATASET_NAME + "\\drwcg.csv"
    global output
    output = "..\datasets\\" + DATASET_NAME + "\\output.txt"
    global data_ref_dict
    data_ref_dict = dict()
    global cluster_map
    cluster_map = dict()
    global file_to_group_id
    file_to_group_id = dict()
    global class_to_func_name_map
    class_to_func_name_map = dict()
    global class_to_ids_map
    class_to_ids_map = dict()
    global cluster_map
    cluster_map = dict()
    global file_to_group_id
    file_to_group_id = dict()
    global file_to_func_name_map
    file_to_func_name_map = dict()

    #remove old files
    if os.path.isfile(BASE_PATH + "callgraph.csv"):
        os.remove(BASE_PATH + "callgraph.csv")

    if os.path.isfile(BASE_PATH + "drwcg.csv"):
        os.remove(BASE_PATH + "drwcg.csv")

    if os.path.isfile(BASE_PATH + "output.txt"):
        os.remove(BASE_PATH + "output.txt")

    if os.path.isfile(BASE_PATH + "clustermap.csv"):
        os.remove(BASE_PATH + "clustermap.csv")

#Extract features
def levenshtein(a, b):
    if (not a and not b):
        return 0
    elif (not a):
        return len(b)
    elif (not b):
        return len(a)

    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]
# s = 1-d/m     d = distance m = l1+l2  s = similarity
def compute_similarity(edit_dist, a, b):
    if (not a and not b):
        return 1.0
    elif (not a):
        return 0.0
    elif (not b):
        return 0.0

    similarity = float(1 - ((edit_dist) / (len(a) + len(b))))
    return similarity

def process_function_sequence(use_dr_weight_flag):
    # key=function_id and value=list of data references
    refmap = dict()

    #list of functions
    functions_id_map = dict()

    rowcount = 0
    start = 1
    # load data references
    with open(BASE_PATH + 'cross_ref_int.csv', 'r') as csv_f:
        for row in csv_f:
            #print(row)
            print(".", end='')
            myList = row.replace(' ', '').split(',')
            myList = [int(i) for i in myList]

            if len(myList) > 1:
                refmap[myList[0]] = myList[1:len(myList)]
            else:
                refmap[myList[0]] = 0

    list1 = list()
    list2 = list()

    fg = open(BASE_PATH + "callgraph.csv", "wb")

    print("\n Calculating data reference weights")
    for i in range(1, len(refmap) - 1):
        print(".", end=" ")
        list1 = refmap[i]
        list2 = refmap[i + 1]

        edit_dist = levenshtein(list1, list2)
        similarity = compute_similarity(edit_dist, list1, list2)

        if use_dr_weight_flag == 1:
            edge_weight = 1
        else:
            edge_weight = similarity * weight_function_seq + 1

        #dissimilarity=(edit_dist/min(len(list1), len(list2)))
        #print("f"+str(i)+":f"+str(i+1)+" = "+str(edit_dist)+" "+str(dissimilarity))

        fg.write(bytes(str.format("{0:0}", i) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}", i + 1) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}", edit_dist) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}", similarity) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}", float(edge_weight)) + ",", 'utf8'))
        fg.write(bytes(str.format("SEQ_1_STEP")+"\n", 'utf8'))

    print("\n Calculating 2 steps data references:")
    for i in range(1, len(refmap) - 2):
        print(".", end=" ")
        list1 = refmap[i]
        list2 = refmap[i + 2]

        edit_dist = levenshtein(list1, list2)
        similarity = compute_similarity(edit_dist, list1, list2)

        if use_dr_weight_flag == 1:
            edge_weight = 1
        else:
            edge_weight = similarity * weight_function_seq + 1
        #dissimilarity=(edit_dist/min(len(list1), len(list2)))
        #print("f"+str(i)+":f"+str(i+1)+" = "+str(edit_dist)+" "+str(dissimilarity))

        fg.write(bytes(str.format("{0:0}", i) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}", i + 2) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}", edit_dist) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}", similarity) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}", float(edge_weight)) + ",", 'utf8'))
        fg.write(bytes(str.format("SEQ_2_STEP")+"\n", 'utf8'))
    fg.close()
    csv_f.close()
    return refmap

def process_far_call_pattern(data_ref_dict, use_call_weight_flag):
    call_map = dict()

    fg = open(BASE_PATH + "callgraph.csv", "a")

    with open(BASE_PATH + 'edges.csv', 'r') as csv_f:
        for row in csv_f:
            print(".", end=" ")
            myList = row.replace(' ', '').split(',')
            myList = [int(i) for i in myList]

            try:
                curlist = call_map[myList[0]]
            except:
                call_map[myList[0]] = list()
            call_map[myList[0]].append(myList[1])
    csv_f.close()
    pprint(call_map)

    for f in call_map.keys():
        fun_list = call_map[f]
        for i in range(len(fun_list)):
            for j in range(len(fun_list)):
                if (fun_list[i]-fun_list[j]!= 0)and  (abs(fun_list[i]-fun_list[j])< 5):
                    print(str(f) + " "+str(fun_list[i]) +" "+ str(fun_list[j]))
                    try:
                        list1 = data_ref_dict[fun_list[i]]
                        list2 = data_ref_dict[fun_list[j]]
                    except:
                        continue

                    edit_dist = levenshtein(list1, list2)
                    similarity = compute_similarity(edit_dist, list1, list2)

                    if use_call_weight_flag == 1:
                        edge_weight = 1
                    else:
                        if abs(fun_list[i] - fun_list[j]) > 1:
                            edge_weight = (similarity * weight_call_graph)/abs(fun_list[i] - fun_list[j]) + 1
                        else:
                            edge_weight = (similarity * weight_call_graph)+  1

                    fg.write(str(fun_list[i]) + "," + str(fun_list[j]) + ",")
                    fg.write(str(edit_dist) + ",")
                    fg.write(str.format("{0:.03f}", similarity) + ",")
                    fg.write(str.format("{0:.03f}", edge_weight)+",")
                    fg.write("FAR_EDGE")
                    fg.write("\n")
    fg.close()

def process_call_graph(data_ref_dict, weight_call_graph, use_call_weight_flag, prune_flag):
    # dictionary to store key=source, value=target
    process_far_call_pattern(data_ref_dict, use_call_weight_flag)
    edges = dict()

    fg = open(BASE_PATH + "callgraph.csv", "a")

    with open(BASE_PATH + 'edges.csv', 'r') as csv_f:
        for row in csv_f:
            #print(row)
            print(".", end=" ")
            myList = row.replace(' ', '').split(',')
            myList = [int(i) for i in myList]

            if prune_flag == 1:
                if abs(myList[0] - myList[1]) > 10:
                    continue

            list1 = data_ref_dict[myList[0]]
            list2 = data_ref_dict[myList[1]]

            edit_dist = levenshtein(list1, list2)
            similarity = compute_similarity(edit_dist, list1, list2)

            if use_call_weight_flag == 1:
                edge_weight = 1
            else:
                if abs(myList[0] - myList[1]) > 1:
                    edge_weight = (similarity * weight_call_graph)/abs(myList[0] - myList[1]) + 1
                else:
                    edge_weight = (similarity * weight_call_graph)+  1

            fg.write(str(myList[0]) + "," + str(myList[1]) + ",")
            fg.write(str(edit_dist) + ",")
            fg.write(str.format("{0:.03f}", similarity) + ",")
            fg.write(str.format("{0:.03f}", edge_weight) +",")
            fg.write(str.format("CALL_EDGE"))
            fg.write("\n")
    fg.close()

def use_dr_only():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(0)
    print("\ndone..")

def use_call_graph_only():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(1)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 1, 1)

def use_dr_call_both_unpruned():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(0)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 0, 0)

def use_dr_call_both_pruned():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(0)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 0, 1)


#Combine Features

def build_drwcg():

    fg = open(BASE_PATH + "drwcg.csv", "wb")

    while not os.path.exists(BASE_PATH + 'callgraph.csv'):
        time.sleep(1)

    with open(BASE_PATH + 'callgraph.csv', 'r') as csv_f:
        for row in csv_f:
            #print(row)
            myList = row.replace(' ', '').split(',')
            source = int(myList[0])
            destination = int(myList[1])
            weight = float(myList[4])

            #print(str(source)+ "   "+ str(destination) + "   " + str(weight))
            if source < int(START) or source > int(END) or destination < int(START) or destination > int(END):
                continue
            fg.write(bytes(str.format("{0:0}", source) + " ", 'utf8'))
            fg.write(bytes(str.format("{0:0}", destination) + " ", 'utf8'))
            fg.write(bytes(str.format("{0:.03f}", weight) + "\r\n", 'utf8'))
    fg.close()
    csv_f.close()

def run_linloglayout():
    path = ""
    while not os.path.exists(BASE_PATH + "drwcg.csv"):
        time.sleep(1)

    os.chdir('LinLogLayout')
    subprocess.call(['java', '-cp', 'bin', 'LinLogLayout', '2', input, output])
    os.chdir(os.pardir)

def parse_output():
    while not os.path.exists(BASE_PATH + 'output.txt'):
        time.sleep(1)

    max = 0
    with open(BASE_PATH + 'output.txt', 'r') as csv_f:
        for row in csv_f:
            # print(row)
            myList = row.replace('\n', '').split(' ')
            #print(myList)
            source = myList[0]
            destination = myList[4]
            if int(destination) > int(max):
                max = destination
            cluster_map[source] = destination
    csv_f.close()

    # project cluster id's to partition
    cluster_id_list = []
    counter = 0
    for i in sorted(cluster_map, key=int):
        current_cluster = int(cluster_map[str(i)])
        cluster_id_list.append(current_cluster)

    cluster_count = 0
    previous = cluster_id_list[0]
    for i in range(len(cluster_id_list)):
        current = cluster_id_list[i]
        if current == previous:
            cluster_id_list[i] = cluster_count
        else:
            previous = current
            cluster_count = cluster_count +1
            cluster_id_list[i] = cluster_count

    fg = open(BASE_PATH + "clustermap.csv", "wb")

    counter = 0
    for i in sorted(cluster_map, key=int):
        # print(i)
        fg.write(bytes(str.format("{0:0}", int(i)) + " ", 'utf8'))
        fg.write(bytes(str.format("{0:0}", int(cluster_id_list[counter])) + "\r\n", 'utf8'))
        counter = counter + 1
    fg.close()

# Evaluate
def generate_file_to_functions_map():
    header_ignore_flag = 1

    with open(BASE_PATH + 'LocMetricsFunctions.csv', 'r') as csv_f:
        for row in csv_f:
            if header_ignore_flag == 1:
                header_ignore_flag = 0
                continue
            #print(row)
            row = row.replace('"', '')
            myList = row.replace('\n', '').split(',')
            #print(myList[0] + " " + myList[1])
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
    #print(file_to_func_name_map)
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
    print(DATASET_NAME +" " +str(len(class_to_func_name_map)))

def map_clustering_results():
    caseFlag = 0

    for class_name in class_to_func_name_map.keys():
        for function in class_to_func_name_map[class_name]:
            if "::" in function:
                key1 = function.split("::")[0]
                key2 = function.split("::")[1]
                #print(key1 + " & " + key2)
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

    methods_count = 0
    class_count = 0
    for class_name in class_to_ids_map.keys():
         if ".cpp" in class_name or ".cc" in class_name:
            continue
         methods_count  = methods_count + len(class_to_ids_map[class_name])
         class_count = class_count + 1

    fg = open("datasets/" + "result.csv", "a")
    fg.write("\nMethods=" + str.format("{0:.03f}", methods_count)+" classes="+ str(class_count)+ "\n")
    fg.close()
    print("METHODS:"+str(methods_count))

def get_file_group_ids():
    for value in class_to_ids_map.keys():
        list1 = class_to_ids_map[value]
        counts = Counter(list1).most_common(1)
        file_to_group_id[value] = counts[0][0]
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
    wPrecision = 0
    wRecall = 0
    for class_name in class_to_ids_map.keys():
        list = class_to_ids_map[class_name]
        gFunctions = gFunctions + len(list)

    for class_name in class_to_ids_map.keys():
        if ".cpp" in class_name or ".cc" in class_name:
            continue

        cluster_count = cluster_count + 1
        list1 = class_to_ids_map[class_name]
        cluster_id = Counter(list1).most_common(1)[0][0]
        TP = Counter(list1).most_common(1)[0][1] + 0.0
        FP = len(list1) - TP + 0.0
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
        print("Current Class:"+ class_name)
        print(str(len(list1)) + " " + str(TP) + " " + str(FP) + " " + str(FN))

        gTP = gTP + TP
        gFP = gFP + FP
        gFN = gFN + FN
        precision = TP / (TP + FP)
        print("Precision:" + str(precision))

        recall = TP / (TP + FN)
        f1 = (2 * precision * recall) / (precision + recall)

        wf1 = f1 * (len(list1) / gFunctions)
        wp = precision * (len(list1) / gFunctions)
        wr = recall * (len(list1) / gFunctions)
        if precision == 0:
            cluster_count = cluster_count - 1

        macro_avg += f1
        #print(macro_avg)
        weighted_micro_avg += wf1
        wPrecision += wp
        wRecall += wr

    gPrecision = gTP / (gTP + gFP)
    gRecall = gTP / (gTP + gFN)
    total_avg = (2 * gPrecision * gRecall) / (gPrecision + gRecall)
    print(cluster_count)
    macro_avg = macro_avg / cluster_count
    #print(str.format("{0:.03f}", total_avg) + "\t" + str.format("{0:.03f}", macro_avg) + "\t" + str.format("{0:.03f}",weighted_micro_avg))
    print(str.format("{0:.03f}", wPrecision) + "\t" + str.format("{0:.03f}", wRecall) + "\t" + str.format("{0:.03f}",weighted_micro_avg))
    fg = open("datasets/" + "result.csv", "a")
    fg.write(str.format("{0:.03f}", wPrecision) + ", " + str.format("{0:.03f}", wRecall) + ", " + str.format("{0:.03f}",
                                                                                                           weighted_micro_avg))
    fg.close()

def EGC_run_algorithm(algorithm_flag):

    fg = open("datasets/" + "result.csv", "a")
    fg.write("\n"+DATASET_NAME + ", case:"+str(algorithm_flag)+", ")
    fg.close()
    print("\nEXTRACT STEP:")
    if algorithm_flag == 1:
        use_dr_only()
    elif algorithm_flag == 2:
        use_call_graph_only()
    elif algorithm_flag == 3:
        use_dr_call_both_unpruned()
    elif algorithm_flag == 4:
        use_dr_call_both_pruned()
    print("\nEXTRACT DONE")

    print("\nCreating drwcg:")
    build_drwcg()
    print("\nDone!")

    print("\nRunning LinLogLayout..")
    run_linloglayout()
    print("LinLogLayout Done")

    print("\nEvaluate")
    generate_file_to_functions_map()
    generate_class_to_functions_map()
    parse_output()
    map_clustering_results()
    get_file_group_ids()
    generate_f1_scores()
    print("\n Evaluate Done!")

dataset = ["D1", "D2", "D3","D4", "D5", "D6", "D7", "D8-(i)", "D8-(ii)", "D8-(iii)" , "D9", "D10-(i)",
           "D10-(ii)", "D10-(iii)", "D10-(iv)" , "D12-(i)" , "D12-(ii)" , "D12-(iii)",  "D13-(i)",
            "D13-(ii)" , "D13-(iii)" , "D13-(iv)", "B1", "B2", "B3", "B4", "B5", "B6","B8", "B9", "D32", "D33", "D34"]

#0-100
#0-113
#0-115
#0-145

init_settings("D3", 788, 1361, 10, 10)
EGC_run_algorithm(3)

#init_settings("D4", 157, 837, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D5", 1065, 2051, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D6", 276, 558, 10, 10)   ------ No class
#EGC_run_algorithm(3)

#init_settings("D7", 11179, 22202, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D8", 1237, 2401, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D9", 1005, 1612, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D10", 1237, 1728, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D16", 1387, 2797, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D18", 127, 2179, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D11", 2667, 5346, 10, 10)
#EGC_run_algorithm(3)

#init_settings("D1-new", 2387, 5162, 10, 10)
#EGC_run_algorithm(4)

#init_settings("D2-new", 0, 702, 1000, 10)
#EGC_run_algorithm(1)

#init_settings("D6-new", 12257 , 24238, 10, 10)
#EGC_run_algorithm(3)








