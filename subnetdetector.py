#! /usr/bin/env python3
import os 
import subprocess
import sys
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
newelem_list = []
for i in elem_list:
    newelem_list.append(stdout[i])
newelem_list.remove('127.0.0.1')
f_list = []
for i in newelem_list:
    o = i.split('.')
    o.pop()
    f_list.append(str(o[0] + '.' + o[1] + '.' + o[2] + '.' + '1' + '/24'))
print(f_list)


