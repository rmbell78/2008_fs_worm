#! /usr/bin/env python3
import os 
import subprocess
import sys
conf = subprocess.run(['ifconfig'])

process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
stdout = process.communicate()[0]

stdout = str(stdout.strip())
stdout = stdout.split(' ')
stdout = [i for i in stdout if i]
elem_list = []
t = -1
while True:
    try:
        t = stdout.index('inet', t + 1)
        elem_list.append(t + 1)
    except ValueError:
        break
print('First: ' + stdout[elem_list[0]] + '\nSecond ' + stdout[elem_list[1]])


