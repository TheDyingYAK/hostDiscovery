import ipaddress
import socket
import subprocess
import sys
from os import name


import netaddr #Install using 'pip install netaddr'


#Implement MAC Spoofer, Implement exception handling, implement input validation, Implement linux support

def main():
    objIP = netaddr.IPNetwork(subprocess.getoutput('ipconfig | findstr /i "Gateway')[39:]) #Creates the objIP Object with the default gateway as a constructor. We get the default gate way using the output of subprocess.getoutput and use string splicing to correct the output
    objIP.netmask = subprocess.getoutput('ipconfig | findstr /i "Mask')[39:] #The same thing is done here, but for the netmask.
    while 1 == 1: #This loop will keep you in the menu after each selection until either the user crashes the program somehow (Hopefully not) or exits using sys.exit(0)
        menu(objIP) #Calls the menu with objIP as a parameter


def menu(objIP: netaddr.IPNetwork): #Function declaration taking objIP as a IPNetwork for a parameter
    foo = input('\nWhat would you like to do?\n1.) Update ARP Table (May take some time)\n2.) Display ARP Table in Network\n3.) Exit\n') #Requesting input

    if foo.isdigit(): #Checking if the input is a digit
        foo = int(foo) #If it is convert from string to int
    else: #If not
        print("\nPlease enter a number") #Ask the user to select a number

    if foo == 1:
        getNetInfo(objIP) #Function call to getNetInfo with objIP as a parameter
    elif foo == 2:
        getARPTable(objIP) #Function call to getARPTable with objIP as a parameter
    elif foo == 3:
        sys.exit(0) #Exits program with error code 0


def getNetInfo(objIP: netaddr.IPNetwork): #Function declaration taking objIP as a IPNetwork for a parameter
    if name == "nt": #If user is using windows
        for bar in ipaddress.IPv4Network(objIP.cidr): #Loop through all IPS in the network
            subprocess.call(['ping', str(bar), '-a', '-n', '1', '-4']) #Ping all IPs once


def getARPTable(objIP: netaddr.IPNetwork): #Function declaration taking objIP as a IPNetwork for a parameter
    arpTable = [['IP Address', 'MAC Address', 'DHCP Status', 'Hostname']] #Set arp table as multidimensional list
    for foo in subprocess.getoutput('arp -a').splitlines(): #Split arp into different lists by line, then loop through them
        if (str(objIP.network)[0:3]) == (str(foo.lstrip())[0:3]): #If the first octet is the same
            bar = (str(foo.lstrip()).split()) #Split the list into IP, MAC, and DHCP Status
            try: #Try statement to catch error if hostname cannot be resolved due to no hostname
                ipAddy = str(bar[0:1])[2:][:-2] #Format the ip address into a readable format from the list
                socket.gethostbyaddr(ipAddy) #Attempt to resolve the hostname
                grunt = 0 #If it succeeds then grunt is set to 0
            except socket.error: #Catch error
                grunt = 1 #If there is an error grunt is set to 1
            if grunt == 0: #If grunt is 0 (So no error)
                bar.append(str(socket.gethostbyaddr(ipAddy)[0:1])[2:][:-3]) #Append the hostname to the list
            else: #If not
                bar.append("None") #Append none as the hostname to the list

            arpTable.append(bar) #Append the list to the final arpTable list

    for baz in arpTable: #For each IP in the table
        print(baz) #Print out all the info


main() #Calls main