import os
import subprocess
import time

input = "..\param\\input.txt"
output = "..\param\\output.txt"
dataset_path = "..\param\\dataset.txt"
BASE_PATH = "param/"
result_map = dict()

def run_linloglayout():
    path = ""
    os.chdir('LinLogLayout')
    subprocess.call(['java', '-cp', 'bin', 'LinLogLayout', '2', input, output])
    os.chdir("F:/reverse_engg/processData")

def parse_output():

    while not os.path.exists(BASE_PATH + 'output.txt'):
        time.sleep(1)

    with open(BASE_PATH + 'output.txt', 'r') as csv_f:
        for row in csv_f:
            # print(row)
            myList = row.replace('\n', '').split(' ')
            #print(myList)
            source = myList[0]
            destination = myList[4]
            result_map[source] = destination
    csv_f.close()

def generateInput(alpha, beta, gamma):

    print(os.getcwd())
    fg = open("param/input.txt", "wb")
    print(os.getcwd())
    with open("param/datset.txt", 'r') as csv_f:
        for row in csv_f:
            myList = row.replace('\n', '').split('\t')
            print(myList)
            w1 = float(myList[2]) * alpha
            w2 = float(myList[3]) * beta
            w3 = float(myList[4]) * gamma
            value = w1+ w2 + w3
            src = myList[0]
            dest = myList[1]
            fg.write(bytes(src+"\t", 'utf8'))
            fg.write(bytes(dest+ "\t" , 'utf8'))
            fg.write(bytes(str.format("{0:.03f}", value) + "\r\n", 'utf8'))
    csv_f.close()
    fg.close()

#generateInput(0.5,0.25,0.25)
parse_output()
for x in range(0, 11):
    for y in range(0,11):
        if x+y >10:
            continue
        else:
            print(str(x) + "\t" + str(y)+"\t" + str(10-x-y))
            #generateInput(x * 0.1, y * 0.1, 1- 0.1*x-0.1* y)
            #run_linloglayout()
            #parse_output()