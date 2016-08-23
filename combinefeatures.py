__author__ = 'Vishal'
# !/usr/bin/env python
import settings

def build_drwcg(BASE_PATH, START, end):

    fg = open(BASE_PATH + "drwcg.csv", "wb")

    with open(BASE_PATH + 'callgraph.csv', 'r') as csv_f:
        for row in csv_f:
            #print(row)
            myList = row.replace(' ', '').split(',')
            source = int(myList[0])
            destination = int(myList[1])
            weight = float(myList[4])

            #print(str(source)+ "   "+ str(destination) + "   " + str(weight))
            if source < int(START) or source > int(end) or destination < int(START) or destination > int(end):
                continue
            fg.write(bytes(str.format("{0:0}", source) + " ", 'utf8'))
            fg.write(bytes(str.format("{0:0}", destination) + " ", 'utf8'))
            fg.write(bytes(str.format("{0:.03f}",weight)+"\r\n", 'utf8'))
    fg.close()
    csv_f.close()

DATASET_NAME = settings.DATASET_NAME
BASE_PATH = settings.BASE_PATH
START = settings.START
END = settings.END

print("\nCreating drwcg:")
build_drwcg(BASE_PATH, START, END)
print("\nDone!")


import subprocess
import os
import settings


input = settings.input
out = settings.output

def run_linloglayout():
    path = ""
    os.chdir('LinLogLayout')
    subprocess.call(['java', '-cp', 'bin', 'LinLogLayout', '2', input, out])

print("Running LinLogLayout..")
run_linloglayout()
print("Done!")