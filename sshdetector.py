#! /usr/bin/env python3

def main():
    import nmap
    ssh_list = []                                    #Define a list to contain ip's open on port 22
    nm = nmap.PortScanner()                          #Instantiate portscanner object
    nm.scan('10.0.2.0/24','22')                      #Scan ports 10.0.2.0 - 10.0.2.256 on port 22
    for host in nm.all_hosts():                      #Create a for loop to iterate over the scanned host
        if nm[host]['tcp'][22]['state'] == 'open':   #Validate port 22 is open
            ssh_list.append(host)                    #Add validate hosts to ssh_list
    return(ssh_list)                                 #End the program and return a list of ips
if __name__ == "__main__":
    main()