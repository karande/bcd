__author__ = 'Vishal'
# !/usr/bin/env python

#import numpy
import settings

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

print(levenshtein([1],[1,4]))


def process_function_sequence(weight_function_seq, flag):
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
            print("." ,end='')
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
    for i in range(1, len(refmap)-1):
        print("." ,end=" ")
        list1 = refmap[i]
        list2 = refmap[i + 1]

        edit_dist = levenshtein(list1, list2)
        similarity = compute_similarity(edit_dist, list1, list2)

        if flag == 1:
            edge_weight = 1
        else:
            edge_weight = similarity * weight_function_seq + 1

        #dissimilarity=(edit_dist/min(len(list1), len(list2)))
        #print("f"+str(i)+":f"+str(i+1)+" = "+str(edit_dist)+" "+str(dissimilarity))

        fg.write(bytes(str.format("{0:0}", i) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}", i + 1) + ",", 'utf8'))
        fg.write(bytes(str.format("{0:0}",edit_dist)+",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}",similarity)+",", 'utf8'))
        fg.write(bytes(str.format("{0:.03f}", float(edge_weight)) + "\n", 'utf8'))

    fg.close()
    csv_f.close()
    return refmap


def process_call_graph(data_ref_dict, weight_call_graph, flag, prune):
    # dictionary to store key=source, value=target
    edges = dict()

    fg = open(BASE_PATH + "callgraph.csv", "a")

    with open(BASE_PATH + 'edges.csv', 'r') as csv_f:
        for row in csv_f:
            #print(row)
            print("." ,end=" ")
            myList = row.replace(' ', '').split(',')
            myList = [int(i) for i in myList]

            if prune == 1:
                if abs(myList[0]-myList[1]) > 15:
                    continue

            list1 = data_ref_dict[myList[0]]
            list2 = data_ref_dict[myList[1]]

            edit_dist = levenshtein(list1, list2)
            similarity = compute_similarity(edit_dist, list1, list2)

            if flag == 1:
                edge_weight = 1
            else:
                edge_weight = similarity * weight_call_graph + 1

            fg.write(str(myList[0]) + "," + str(myList[1]) + ",")
            fg.write(str(edit_dist) + ",")
            fg.write(str.format("{0:.03f}", similarity)+ ",")
            fg.write(str.format("{0:.03f}", edge_weight))
            fg.write("\n")
    fg.close()


def use_dr_only():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(weight_function_seq, 0)
    print("\ndone..")


def use_call_graph_only():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(weight_function_seq, 1)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 1, 1)


def use_dr_call_both_unpruned():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(weight_function_seq, 0)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 0, 0)


def use_dr_call_both_pruned():
    print("\nProcessing function sequence")
    data_ref_dict = process_function_sequence(weight_function_seq, 0)

    print("\nCalculating call graph edge weights")
    process_call_graph(data_ref_dict, weight_call_graph, 0, 1)


DATASET_NAME = settings.DATASET_NAME
BASE_PATH = settings.BASE_PATH

# data reference dictionary with key=function id, value=list of data references for the function
data_ref_dict = settings.data_ref_dict

# assign function sequence weight 1 to 100
weight_function_seq = settings.weight_function_seq

# assign call sequence weight 1 to 100
weight_call_graph = settings.weight_call_graph

#use_dr_only()
#use_call_graph_only()
#use_dr_call_both_unpruned()
#use_dr_call_both_pruned()

print("\nDone!")

