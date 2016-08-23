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